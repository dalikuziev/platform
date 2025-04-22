from django.urls import reverse
from rest_framework.test import APITestCase
from ..models import User

class AuthAPITests(APITestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'Testpass123!',
            'role': 'teacher',
            'phone': '+998901234567',
        }
        self.user_data2 = {
            'username': 'testuser2',
            'email': 'test2@example.com',
            'password': 'Testpass123!',
            'role': 'teacher',
            'phone': '+998901234567',
        }

    def test_user_registration(self):
        url = reverse('register')
        response = self.client.post(url, self.user_data)
        self.client.post(url, self.user_data2)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 2)

    def test_user_login(self):
        User.objects.create_user(**self.user_data)
        url = reverse('login')
        response = self.client.post(url, {
            'username': 'testuser',
            'password': 'Testpass123!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)

