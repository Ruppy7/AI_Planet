from rest_framework.permissions import BasePermission

class CanCreateHackathon(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='List_hackathon').exists()