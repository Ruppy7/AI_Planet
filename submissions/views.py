from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout

from .serializers import HackathonSerializer, SubmissionSerializer, EnrollmentSerializer
from .forms import CustomUserCreationForm
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, CreateAPIView
from rest_framework.views import APIView

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import CanCreateHackathon, CanEnrolHackathon
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User, Group
from .models import Hackathon, Submission, Enrollment

# Create your views here.

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

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response(f"Passed for {request.user.email}")

@login_required(login_url='/login')
def logoutUser(request):
    logout(request)
    return redirect('index')

def index(request):
    return render(request, "index.html")

@login_required(login_url='/login')
def home(request):
    return render(request, "home.html")

class HackathonListCreateView(ListCreateAPIView):
    queryset = Hackathon.objects.all()
    serializer_class = HackathonSerializer
    permission_classes = [IsAuthenticated]
        
    def post(self, request, *args, **kwargs):
        if not CanCreateHackathon().has_permission(request, self):
            return Response({"message":"You do not have permissions to perform this request"})
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        

class HackathonRegistrationView(ListCreateAPIView):
    permission_classes = [IsAuthenticated, CanEnrolHackathon]
    serializer_class = EnrollmentSerializer
    
    def get_queryset(self):
        return Enrollment.objects.filter(user = self.request.user)
    
    def create(self, request, *args, **kwargs):
        hackathon_id = request.data.get('hackathon')
        try:
            hackathon = Hackathon.objects.get(pk = hackathon_id)
            existing_enrollment = Enrollment.objects.filter(user=request.user, hackathon=hackathon).first()
            if existing_enrollment:
                return Response({"message": "You are already registered for this hackathon."}, status=status.HTTP_400_BAD_REQUEST)
            enrollment = Enrollment.objects.create(user=request.user, hackathon=hackathon)
            return Response({"message":"Registration Successful!"}, status=status.HTTP_201_CREATED)
        except Hackathon.DoesNotExist:
            return Response({"message":"Hackathon not found."}, status=status.HTTP_404_BAD_REQUEST)

class SubmissionView(APIView):
    permission_classes = [IsAuthenticated]        