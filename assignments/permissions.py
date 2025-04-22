from rest_framework import permissions

class IsCourseOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class IsEnrolledStudent(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
