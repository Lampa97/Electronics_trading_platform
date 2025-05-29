from rest_framework.permissions import BasePermission


class IsActiveEmployee(BasePermission):
    """Permission class to check if the user is an active employee."""
    def has_permission(self, request, view):
        return request.user.is_employee is True


class IsAdmin(BasePermission):
    """Permission class to check if the user is an admin."""
    def has_permission(self, request, view):
        return request.user.is_staff is True
