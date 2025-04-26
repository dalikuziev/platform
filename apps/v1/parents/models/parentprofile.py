from django.db import models
from django_extensions.db.models import TimeStampedModel
from apps.v1.accounts.models import User

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
    def __str__(self):
        return f"{self.user.username} (Ota-ona)"