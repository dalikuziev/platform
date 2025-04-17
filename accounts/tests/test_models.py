from django.test import TestCase
from ..models import User

class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            username='testuser',
            password='Testpass123!',
            role='teacher'
        )
        self.assertEqual(user.role, 'teacher')
        self.assertTrue(user.check_password('Testpass123!'))

    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            username='admin',
            password='adminpass'
        )
        self.assertTrue(admin.is_superuser)
