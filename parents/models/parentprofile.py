from django.db import models
from accounts.models import User
from courses.models import Course
from django_extensions.db.models import TimeStampedModel


class ParentProfile(TimeStampedModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='parent_profile',
        verbose_name="Foydalanuvchi"
    )
    children = models.ManyToManyField(
        User,
        related_name='parents',
        limit_choices_to={'role': 'student'},
        verbose_name="Farzandlar"
    )
    phone = models.CharField(max_length=20, verbose_name="Telefon raqami")
    # created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Ota-ona profili"
        verbose_name_plural = "Ota-onalar profillari"

    def __str__(self):
        return f"{self.user.username} (Ota-ona)"
