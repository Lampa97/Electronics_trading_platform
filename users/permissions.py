from rest_framework.permissions import BasePermission


class IsActiveEmployee(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_employee == True


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff == True