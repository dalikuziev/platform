from icecream import ic
from rest_framework import permissions

class IsCourseOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # ic(obj.course.owner == request.user)
        # ic(request.user.role)
        return obj.course.owner == request.user
