from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLES = (
        ('teacher', 'O\'qituvchi'),
        ('student', 'O\'quvchi'),
        ('parents', 'Ota-ona'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLES, default='student')
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f'{self.email} ({self.get_role_display()})'
        # return f'{self.username} ({self.role})'
