from rest_framework import permissions # type: ignore

class IsStaffUser(permissions.BasePermission):
    """
    Custom permission to only allow access to staff users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff
    
class IsSuperUser(permissions.BasePermission):
    """
    Custom permission to only allow access to staff users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser