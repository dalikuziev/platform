from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.v1.shared.serializers import BaseCleanSerializer

User = get_user_model()

class UserSerializer(BaseCleanSerializer):
    class Meta:
        model = User
        # exclude = ['password']
        # fields = ('id', 'username', 'email', 'first_name', 'last_name', 'role', 'phone')
        # fields = '__all__'
        exclude = ('password', 'groups', 'user_permissions', 'is_staff', 'is_superuser')
        read_only_fields = ['role']

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """JWT tokeniga qo'shimcha maydonlar (role) qo'shish"""
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        return token

class UserRegisterSerializer(serializers.ModelSerializer):
    """Simplified registration serializer"""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # exclude = ['password']
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'role', 'phone', 'date_joined')
        read_only_fields = ('role',)
        extra_kwargs = {
            'email': {'required': False},
            'phone': {'required': False},
        }

class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)
    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "New passwords must match."})
        return attrs