from rest_framework import permissions
from django.contrib.auth.models import Group

class IsAdminUser(permissions.BasePermission):
    """
    Permission for admin users only - untuk akses data ML
    """
    
    def has_permission(self, request, view):
        return (request.user and 
                request.user.is_authenticated and 
                request.user.is_admin)

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit objects.
    Read-only permissions are allowed to any authenticated user.
    """
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
            
        # Read permissions for authenticated users
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Write permissions only for admins
        return request.user.is_admin

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admins to edit it.
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Read permissions for authenticated users
        if request.method in permissions.SAFE_METHODS:
            # Check if user can view this object based on role
            if request.user.is_admin or request.user.role == 'hr':
                return True
            elif request.user.is_manager and hasattr(obj, 'department'):
                return obj.department == request.user.department
            elif hasattr(obj, 'employee'):
                return obj.employee == request.user
            elif hasattr(obj, 'user'):
                return obj.user == request.user
            else:
                return obj == request.user
        
        # Write permissions for owners or admins
        if request.user.is_admin:
            return True
            
        if hasattr(obj, 'employee'):
            return obj.employee == request.user
        elif hasattr(obj, 'user'):
            return obj.user == request.user
        else:
            return obj == request.user

class IsManagerOrAbove(permissions.BasePermission):
    """
    Permission for managers, HR, and admins only.
    """
    
    def has_permission(self, request, view):
        return (request.user and 
                request.user.is_authenticated and 
                request.user.is_manager)

class IsHROrAdmin(permissions.BasePermission):
    """
    Permission for HR and admin users only.
    """
    
    def has_permission(self, request, view):
        return (request.user and 
                request.user.is_authenticated and 
                (request.user.is_admin or request.user.role == 'hr'))

class IsSelfOrAdmin(permissions.BasePermission):
    """Allow users to edit their own profile or admin users to edit any profile."""

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions for self or admin
        if request.user and request.user.is_authenticated:
            if request.user.is_admin:
                return True
            return obj == request.user
        return False
