from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import RegexValidator

phone_regex = RegexValidator(
    regex=r'^\+998\d{9}$',
    message="Telefon raqam quyidagi formatda bo'lishi kerak: '+998XXXXXXXXX' (masalan, +998901234567)."
)

class User(AbstractUser):
    ROLES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('parents', 'Parents'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLES, default='student')
    phone = models.CharField(validators=[phone_regex], max_length=13, blank=True)
    email = models.EmailField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f'{self.get_full_name()} ({self.role})'

    def clean(self):
        super().clean()
        if self.email:
            if User.objects.exclude(pk=self.pk).filter(email=self.email).exists():
                raise ValidationError({'email': 'Bu email allaqachon foydalanilgan.'})
        if self.phone:
            if User.objects.exclude(pk=self.pk).filter(phone=self.phone).exists():
                raise ValidationError({'phone': 'Bu raqam allaqachon foydalanilgan.'})

