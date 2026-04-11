from rest_framework.permissions import BasePermission


class IsAdminUserRole(BasePermission):

    def has_permission(self, request, view):
        # For this Permission: Only admin can Access
        return request.user.is_authenticated and request.user.role == 'admin'