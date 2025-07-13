# permissions.py - Custom permissions for HR features

from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admin users to edit objects.
    Regular users get read-only access.
    """
    
    def has_permission(self, request, view):
        # Read permissions for authenticated users
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        
        # Write permissions only for admin users
        return request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners or admin users to access objects.
    """
    
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Admin users have full access
        if request.user.is_staff or request.user.is_superuser:
            return True
        
        # Check if user is the owner of the object
        if hasattr(obj, 'employee'):
            return obj.employee == request.user
        elif hasattr(obj, 'user'):
            return obj.user == request.user
        
        return False


class IsAdminUser(permissions.BasePermission):
    """
    Permission that only allows admin users.
    """
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)


class IsEmployeeOrAdmin(permissions.BasePermission):
    """
    Permission for employee-specific data access.
    Employees can only access their own data, admins can access all.
    """
    
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Admin users have full access
        if request.user.is_staff or request.user.is_superuser:
            return True
        
        # Employees can only access their own records
        if hasattr(obj, 'employee'):
            return obj.employee == request.user
        
        return False
