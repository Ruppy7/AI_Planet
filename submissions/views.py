from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.contrib.auth.password_validation import validate_password

from .serializers import UserSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
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
            return Response({"Error" : "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    elif request.method == "GET":
        return render(request, 'index.html')

@api_view(['GET', 'POST'])
def signup(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            email = serializer.validated_data.get('email')
            if User.objects.filter(username=username).exists():
                error = "Username is already taken."
            elif User.objects.filter(email=email).exists():
                error = "Email is already in use!"
            else:
                try:
                    validate_password(password)
                    user = User.objects.create_user(username=username, password=password, email=email)
                    token, created = Token.objects.get_or_create(user=user)
                    login(request, user)
                    return redirect("home")
                except Exception as e:
                    error = str(e)
        else:
            error = "Invalid data. Please check the form fields."
        return render(request, 'signup.html', {'error': error})
    elif request.method == 'GET':
        return render(request, 'signup.html')

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

@login_required
def home(request):
    return render(request, "home.html")