from rest_framework import permissions
from django.contrib.auth.models import Group

class IsAdminUser(permissions.BasePermission):
    """Custom permission to only allow users in the 'HR/Admin' group to access."""

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            try:
                admin_group = Group.objects.get(name='HR/Admin')
                return admin_group in request.user.groups.all()
            except Group.DoesNotExist:
                return False
        return False

class IsEmployeeUser(permissions.BasePermission):
    """Custom permission to only allow authenticated employees to access."""

    def has_permission(self, request, view):
        # Allow access if user is authenticated and is not an admin
        if request.user and request.user.is_authenticated:
            try:
                admin_group = Group.objects.get(name='HR/Admin')
                return admin_group not in request.user.groups.all()
            except Group.DoesNotExist:
                # If admin group doesn't exist, all authenticated users are considered employees
                return True
        return False

class IsSelfOrAdmin(permissions.BasePermission):
    """Custom permission to allow users to edit their own profile or admin users to edit any profile."""

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request, so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        if request.user and request.user.is_authenticated:
            try:
                admin_group = Group.objects.get(name='HR/Admin')
                if admin_group in request.user.groups.all():
                    return True # Admin can do anything
            except Group.DoesNotExist:
                pass # Continue to check if it's the user's own object

            return obj == request.user
        return False
