from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.utils import timezone

from .serializers import (
    HackathonSerializer,
    ImageSubmissionSerializer,
    LinkSubmissionSerializer,
    FileSubmissionSerializer,
    EnrollmentSerializer,
)
from .forms import CustomUserCreationForm
from .models import Hackathon, Submission, Enrollment
from .permissions import CanCreateHackathon, CanEnrolHackathon

# Login View for the users
@api_view(['GET','POST'])
def userLogin(request):
    if request.method == "POST":
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username= username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(request, 'index.html', {"error":"Bad Request/Invalid Credentials"})
    elif request.method == "GET":
        return render(request, 'index.html')

# Signup/Register View
@api_view(['GET', 'POST'])
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.data)
        if form.is_valid():
            user = form.save()
            user_role = form.cleaned_data.get('user_role')
            if user_role == 'enrol_hackathon':
                enrol_hackathon_group = Group.objects.get(name='Enrol_hackathon')
                user.groups.add(enrol_hackathon_group)
            elif user_role == 'list_hackathon':
                list_hackathon_group = Group.objects.get(name='List_hackathon')
                user.groups.add(list_hackathon_group)
            return redirect("home")
        error = form.errors
        return render(request, 'signup.html', {"error": error})
    elif request.method == 'GET':
        form = CustomUserCreationForm()
        return render(request, 'signup.html', {'form': form})

# Logout View for the customusers
@login_required(login_url='/login')
def logoutUser(request):
    logout(request)
    return redirect('index')

# Hackathon Viewing and Creation
class HackathonListCreateView(ListCreateAPIView):
    queryset = Hackathon.objects.all()
    serializer_class = HackathonSerializer
    permission_classes = [IsAuthenticated]
        
    # Overriding Post request to handle permissions for users.
    def post(self, request, *args, **kwargs):
        if not CanCreateHackathon().has_permission(request, self):
            return Response({"message":"You do not have permissions to perform this request"})
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
# Single Hackathon list view
class HackathonDetailView(RetrieveAPIView):
    serializer_class = HackathonSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        hackathon_id = self.kwargs['pk']
        return Hackathon.objects.filter(pk=hackathon_id)

# Enrolling for a hackathon view (Limited to users within enrol_hackathon group)
class HackathonRegistrationView(ListCreateAPIView):
    permission_classes = [IsAuthenticated, CanEnrolHackathon]
    serializer_class = EnrollmentSerializer
    
    def get_queryset(self):
        return Enrollment.objects.filter(user = self.request.user)
    
    # Overriding create method to check for edge cases
    def create(self, request, *args, **kwargs):
        hackathon_id = request.data.get('hackathon')
        try:
            hackathon = Hackathon.objects.get(pk = hackathon_id)
            if hackathon.end <= timezone.now():
                return Response({"message":"The hackathon has ended. You can not enroll for this anymore."}, status=status.HTTP_400_BAD_REQUEST)
            existing_enrollment = Enrollment.objects.filter(user=request.user, hackathon=hackathon).exists()
            if existing_enrollment:
                return Response({"message": "You are already registered for this hackathon."}, status=status.HTTP_400_BAD_REQUEST)
            enrollment = Enrollment.objects.create(user=request.user, hackathon=hackathon)
            return Response({"message":"Registration Successful!"}, status=status.HTTP_201_CREATED)
        except Hackathon.DoesNotExist:
            return Response({"message":"Hackathon not found."}, status=status.HTTP_404_BAD_REQUEST)
        except ValidationError as e:
            return Response({"message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
# Submission View where users can send a post request to submit their responses
class SubmissionView(CreateAPIView):
    permission_classes = [IsAuthenticated, CanEnrolHackathon]
    
    def get_queryset(self):
        return Submission.objects.filter(user=self.request.user)
    
    # Overriding get_serializer method to choose appropriate serializer for the hackathon
    def get_serializer(self, *args, **kwargs):
        hackathon_id = self.kwargs.get('pk')
        hackathon = get_object_or_404(Hackathon, pk=hackathon_id)
        submission_type = hackathon.submission_type

        if submission_type == 'image':
            return ImageSubmissionSerializer(*args, **kwargs)
        elif submission_type == 'file':
            return FileSubmissionSerializer(*args, **kwargs)
        elif submission_type == 'link':
            return LinkSubmissionSerializer(*args, **kwargs)

        return super().get_serializer(*args, **kwargs)
    
    # Utility function to perform validation checks    
    def _check_submission(self, user, hackathon):
        existing_submission = Submission.objects.filter(user=user, hackathon=hackathon).exists()
        enrolled_in = Enrollment.objects.filter(user=user, hackathon=hackathon).exists()
        if existing_submission:
            raise serializers.ValidationError("You have already submitted your response for this hackathon")
        elif not enrolled_in:
            raise serializers.ValidationError("You are not enrolled in the hackathon to submit your response!")

        if hackathon.end <= timezone.now():
            raise serializers.ValidationError("The hackathon has ended. You can not submit.")
    
    
    # Overriding create method to perform validation checks before creating an object
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        hackathon_id = self.kwargs.get('pk')
        hackathon = get_object_or_404(Hackathon, pk=hackathon_id)
        self._check_submission(user, hackathon)
        serializer.save(user=user, hackathon=hackathon)
        headers = self.get_success_headers(serializer.data)
        return Response({"message": "You have successfully submitted your response for this hackathon!"}, status=status.HTTP_201_CREATED, headers=headers)
        
# Submission listing view where users can view their submissions
class SubmissionListView(ListAPIView):
    permission_classes = [IsAuthenticated, CanEnrolHackathon]

    def get_serializer(self, submission_type, *args, **kwargs):
        if submission_type == 'image':
            return ImageSubmissionSerializer(*args, **kwargs)
        elif submission_type == 'file':
            return FileSubmissionSerializer(*args, **kwargs)
        elif submission_type == 'link':
            return LinkSubmissionSerializer(*args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        return Submission.objects.filter(user=user)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serialized_submissions = []
        for submission in queryset:
            hackathon = submission.hackathon
            serializer = self.get_serializer(hackathon.submission_type, submission, many=False)
            serialized_submissions.append(serializer.data)

        return Response(serialized_submissions)


@login_required(login_url='/login')
def home(request):
    return render(request, "home.html")

def index(request):
    return render(request, "index.html")