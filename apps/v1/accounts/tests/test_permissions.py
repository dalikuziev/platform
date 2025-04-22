from django.test import TestCase, RequestFactory
from ..models import User
from ..permissions import IsTeacher, IsStudent, IsParent, IsTeacherOrAdmin

class PermissionTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.teacher = User.objects.create_user(
            username='teacher1',
            password='testpass123',
            email='teacher1@gmail.com',
            role='teacher',
        )
        self.student = User.objects.create_user(
            username='student1',
            password='testpass123',
            email='student1@gmail.com',
            role='student',
        )
        self.parent = User.objects.create_user(
            username='parent1',
            password='testpass123',
            email='parent1@gmail.com',
            role='parent',
        )
        self.admin = User.objects.create_user(
            username='admin1',
            password='testpass123',
            email='admin1@gmail.com',
            role='admin',
            is_staff=True,
        )

    def test_is_teacher_permission(self):
        request = self.factory.get('/api/courses/')
        request.user = self.teacher
        permission = IsTeacher()
        self.assertTrue(permission.has_permission(request, None))

    def test_is_not_teacher_permission(self):
        request = self.factory.get('/api/courses/')
        request.user = self.student
        permission = IsTeacher()
        self.assertFalse(permission.has_permission(request, None))

    def test_is_student_permission(self):
        request = self.factory.get('/api/enroll/')
        request.user = self.student
        permission = IsStudent()
        self.assertTrue(permission.has_permission(request, None))

    def test_is_not_student_permission(self):
        request = self.factory.get('/api/enroll/')
        request.user = self.teacher
        permission = IsStudent()
        self.assertFalse(permission.has_permission(request, None))

    def test_is_parent_permission(self):
        request = self.factory.get('/api/courses/')
        request.user = self.parent
        permission = IsParent()
        self.assertTrue(permission.has_permission(request, None))

    def test_is_not_parent_permission(self):
        request = self.factory.get('/api/courses/')
        request.user = self.teacher
        permission = IsParent()
        self.assertFalse(permission.has_permission(request, None))

    def test_is_teacher_or_admin_permission(self):
        request = self.factory.get('/api/courses/')
        # request.user = self.teacher
        request.user = self.admin
        permission = IsTeacherOrAdmin()
        self.assertTrue(permission.has_permission(request, None))

    def test_is_not_teacher_or_admin_permission(self):
        request = self.factory.get('/api/enroll/')
        # request.user = self.student
        request.user = self.parent
        permission = IsTeacherOrAdmin()
        self.assertFalse(permission.has_permission(request, None))
