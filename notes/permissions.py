from django.contrib.auth.models import User
from rest_framework import permissions

class IsPOST(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == 'POST'