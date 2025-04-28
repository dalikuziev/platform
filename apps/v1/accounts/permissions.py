from icecream import ic
from rest_framework import permissions

from apps.v1.courses.models import Lesson


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

class IsTeacherAndCourseOwner(permissions.BasePermission):
    """
    Faqat teacher bo'lgan va shu lessonning course owner'i bo'lgan foydalanuvchilarga ruxsat beradi.
    """
    def has_permission(self, request, view):
        if request.user.role != 'teacher':
            return False
        lesson_id = view.kwargs.get('lesson_id')
        if lesson_id is None:
            return False
        try:
            lesson = Lesson.objects.select_related('course').get(id=lesson_id)
        except Lesson.DoesNotExist:
            return False
        return lesson.course.owner == request.user