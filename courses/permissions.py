from rest_framework import permissions

from groups.models import StudentGroup
from .models import Course

class IsCourseTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        if 'course_id' in view.kwargs:
            return Course.objects.filter(
                id=view.kwargs['course_id'],
                owner=request.user
            ).exists()
        # elif 'pk' in view.kwargs:
        #     return Course.objects.filter(
        #         id=view.kwargs['pk'],
        #         teacher=request.user
        #     ).exists()
        return False

class IsEnrolledStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        if 'course_id' in view.kwargs:
            return StudentGroup.objects.filter(
                id=view.kwargs['course_id'],
                students=request.user
            ).exists()
        elif 'pk' in view.kwargs:
            return StudentGroup.objects.filter(
                id=view.kwargs['pk'],
                students=request.user
            ).exists()
        return False
