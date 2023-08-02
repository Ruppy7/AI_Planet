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
        
class SubmissionSerializer(serializers.ModelSerializer):
    submission_data = serializers.SerializerMethodField()
    
    class Meta:
        model = Submission
        fields = ['name', 'summary', 'submission_data']
        
        def get_submission_data(self,obj):
            request = self.context.get('request', None)
            if request and hasattr(request, 'resolver_match'):
                hackathon_id = request.resolver_match.kwargs.get('hackathon_id')
                if hackathon_id:
                    try:
                        hackathon = Hackathon.objects.get(pk=hackathon_id)
                        hk_submission_type = hackathon.submission_type
                        if hk_submission_type == 'image':
                            return obj.submission_image.url if obj.submission_image else None
                        elif hk_submission_type == 'file':
                            return obj.submission_file.url if obj.submission_file else None
                        elif hk_submission_type == 'link':
                            return obj.submission_link if obj.submission_link else None
                    except Hackathon.DoesNotExist:
                        pass
            return None
                        