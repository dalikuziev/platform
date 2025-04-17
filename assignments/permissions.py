from rest_framework import permissions
from courses.models import Course

class IsCourseTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        if 'lesson_id' in view.kwargs:
            return Course.objects.filter(
                lessons__id=view.kwargs['lesson_id'],
                teacher=request.user
            ).exists()
        elif 'assignment_id' in view.kwargs:
            return Course.objects.filter(
                lessons__assignments__id=view.kwargs['assignment_id'],
                teacher=request.user
            ).exists()
        return False

class IsEnrolledStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        if 'assignment_id' in view.kwargs:
            return Course.objects.filter(
                lessons__assignments__id=view.kwargs['assignment_id'],
                students=request.user
            ).exists()
        return False
