from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Hackathon
from django import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'user_role']
