from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from apps.v1.shared.serializers import BaseCleanSerializer

User = get_user_model()

class UserSerializer(BaseCleanSerializer):
    class Meta:
        model = User
        exclude = ('password', 'groups', 'user_permissions', 'is_staff', 'is_superuser')

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """JWT tokeniga qo'shimcha maydonlar (role) qo'shish"""
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        return token

class UserRegisterSerializer(serializers.ModelSerializer):
    """Simplified registration serializer"""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password2', 'role')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
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

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()