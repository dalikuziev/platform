from rest_framework.test import APITestCase
from ..serializers import UserRegisterSerializer


class UserSerializerTest(APITestCase):
    def test_valid_registration(self):
        data = {
            'username': 'newuser',
            'password': 'Newuser123!',
            'email': 'newuser@gmail.com',
            'role': 'student',
            'phone': '+998901234567',
        }
        serializer = UserRegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_password(self):
        data = {'username': 'user1', 'password': '123', 'role': 'teacher'}
        serializer = UserRegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())

