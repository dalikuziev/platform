from icecream import ic
from rest_framework import permissions
from rest_framework.permissions import BasePermission

from apps.v1.assignments.models import Assignment


# from apps.v1.accounts.models.assignment import Assignment

class IsCourseTeacher(BasePermission):
    def has_permission(self, request, view):
        # bu yerga kerakli logika
        return request.user.is_authenticated and request.user.is_teacher

class IsGroupTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'teacher' and request.submission.student

# class IsEnrolledStudent(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return request.user.role == 'student' and obj.students.filter(student=request.user).exists()
class IsEnrolledStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        ic()
        assignment_id = request.data.get('assignment')
        ic(assignment_id)
        if not assignment_id:
            ic('if')
            return False

        try:
            # ic(Assignment.objects.all())
            assignment = Assignment.objects.get(id=assignment_id)
            ic(assignment)
        except Assignment.DoesNotExist:
            return False

        course = assignment.lesson.course  # Assignment orqali Course ga o'tamiz
        ic(request)
        return request.user.role == 'student' and course.students.filter(id=request.user.id).exists()
