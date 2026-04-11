from rest_framework.permissions import BasePermission


class IsNotTrainee(BasePermission):
    # For GET
    def has_permission(self, request, view):

        return (
            request.user.is_authenticated and
            request.user.role != 'trainee'
        )


class IsAdminOrMobilizer(BasePermission):
    # Allows create. For POST, PUT
    def has_permission(self, request, view):

        return (
            request.user.is_authenticated and
            request.user.role in ['admin', 'mobilizer']
        )


class IsAdminOrOwnerMobilizer(BasePermission):
    # For DELETE.Admin OR Mobilizer (own only)
    def has_object_permission(self, request, view, obj):

        if request.user.role == 'admin':
            return True

        return obj.created_by == request.user