from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.contrib.auth.password_validation import validate_password
from rest_framework import viewsets

from .serializers import UserSerializer
from .forms import CustomUserCreationForm
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required

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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    token = Token.objects.filter(user=request.user).delete()
    return redirect('index')

def index(request):
    return render(request, "index.html")

@login_required(login_url='/login')
def home(request):
    return render(request, "home.html")