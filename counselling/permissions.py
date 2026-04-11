'''
GET	    Admin/Counsellor/Teacher
POST	Admin/Counsellor
PATCH	Admin/Counsellor
DELETE	Admin

So we make 3 permission classes.
'''

from rest_framework.permissions import BasePermission

class IsAdminCounsellorTeacher(BasePermission):

    def has_permission(self, request, view):
        return ( request.user.is_authenticated and request.user.role in ['admin', 'counsellor', 'teacher'])

class IsAdminOrCounsellor(BasePermission):

    def has_permission(self, request, view):
        return ( request.user.is_authenticated and request.user.role in ['admin', 'counsellor'] )


class IsAdminOnly(BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.role == 'admin')