from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import User


class AuthTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='Testpass123!',
            email='test@example.com',
            role='teacher',
        )

    def test_login(self):
        url = reverse('login')
        data = {'username': 'testuser', 'password': 'Testpass123!'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
