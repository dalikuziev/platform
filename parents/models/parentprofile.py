from django.db import models
from accounts.models import User
from courses.models import Course
from django_extensions.db.models import TimeStampedModel

class ParentProfile(TimeStampedModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='parent_profile'
    )
    children = models.ManyToManyField(
        User,
        related_name='parents',
        limit_choices_to={'role': 'student'}
    )
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.username} (Ota-ona)"
