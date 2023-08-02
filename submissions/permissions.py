from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework import status
class CanCreateHackathon(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='List_hackathon').exists()
    
class CanEnrolHackathon(BasePermission):
    message = "You can not enroll in hackathons as you are a lister yourself!"
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Enrol_hackathon').exists()
    