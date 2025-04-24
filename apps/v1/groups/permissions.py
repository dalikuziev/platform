from rest_framework import permissions
from rest_framework.permissions import BasePermission

class IsCourseTeacher(BasePermission):
    def has_permission(self, request, view):
        # bu yerga kerakli logika
        return request.user.is_authenticated and request.user.is_teacher

class IsGroupTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'teacher'

class IsEnrolledStudent(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.role == 'student' and obj.students.filter(student=request.user).exists()