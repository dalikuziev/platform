from icecream import ic
from rest_framework import permissions

class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'teacher'

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'student'

class IsParent(permissions.BasePermission):
    """
    Allows access only to parents.
    """
    def has_permission(self, request, view):
        # ic(request.user.__dict__)
        return bool(request.user and request.user.role == 'parents')

class IsTeacherOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'teacher' or request.user.is_staff

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'admin'