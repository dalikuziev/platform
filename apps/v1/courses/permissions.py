from rest_framework import permissions

class IsCourseOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.course.owner == request.user