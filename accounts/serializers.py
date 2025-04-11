from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'phone']
        read_only_fields = ['id', 'role']

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """JWT tokeniga qo'shimcha maydonlar (role) qo'shish"""
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        return token

class UserRegisterSerializer(serializers.ModelSerializer):
    """Ro'yxatdan o'tish uchun serializer"""
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'role', 'phone')
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role'],
            phone=validated_data['phone']
        )
        return user
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'role', 'phone', 'date_joined')
        read_only_fields = ('id', 'role', 'date_joined',)
        extra_kwargs = {
            'email': {'required': False},
            'phone': {'required': False},
        }
