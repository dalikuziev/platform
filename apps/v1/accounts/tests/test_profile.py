from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class ProfileTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='Testpass123!',
            email = 'test@example.com',
            role='teacher',
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            password='Testpass123!',
            email='test2@example.com',
            role='student',
        )
        self.client.force_authenticate(user=self.user)

    def test_get_profile(self):
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], 'testuser')

    def test_update_profile(self):
        url = reverse('profile')
        data = {'first_name': 'Test', 'phone': '+998901234567'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)

