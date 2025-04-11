from rest_framework import permissions
from .models import Course

class IsCourseTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        if 'course_id' in view.kwargs:
            return Course.objects.filter(
                id=view.kwargs['course_id'],
                teacher=request.user
            ).exists()
        elif 'pk' in view.kwargs:
            return Course.objects.filter(
                id=view.kwargs['pk'],
                teacher=request.user
            ).exists()
        return False

class IsEnrolledStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        if 'course_id' in view.kwargs:
            return Course.objects.filter(
                id=view.kwargs['course_id'],
                students=request.user
            ).exists()
        elif 'pk' in view.kwargs:
            return Course.objects.filter(
                id=view.kwargs['pk'],
                students=request.user
            ).exists()
        return False

# class IsCourseOwner(permissions.BasePermission):
#     def has_permission(self, request, view):
#         course_id = view.kwargs.get('pk')
#         course = Course.objects.get(id=course_id)
#         return course.owner == request.user


