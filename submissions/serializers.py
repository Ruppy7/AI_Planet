from rest_framework import serializers 
from django.contrib.auth.models import User
from .models import Hackathon, Submission, Enrollment

class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['id', 'username', 'password', 'email']
        
class HackathonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hackathon
        fields = '__all__'
        
class EnrollmentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default = serializers.CurrentUserDefault())
    class Meta:
        model = Enrollment
        fields = '__all__'
        
class ImageSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['name', 'summary', 'submission_image']
        
        
class FileSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['name', 'summary', 'submission_file']
        
class LinkSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['name', 'summary', 'submission_link']
