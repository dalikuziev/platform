from rest_framework import permissions

class IsParentOfStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        if not hasattr(request.user, 'parent_profile'):
            return False
        parent_profile = request.user.parent_profile
        student_id = view.kwargs.get('student_id') or request.data.get('student_id')
        return parent_profile.children.filter(id=student_id).exists()