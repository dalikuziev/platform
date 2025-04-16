from django.db import models
from django.contrib.auth import get_user_model
from django_extensions.db.models import TimeStampedModel

from shared.models import DraftModel

User = get_user_model()


class Notification(TimeStampedModel, DraftModel):
    CATEGORY_CHOICES = [
        ('imtihon', 'Imtihon'),
        ('guruh', 'Guruhga qo‘shilganlik'),
        ('uyga_vazifa', 'Uyga vazifa'),
        ('dars', 'Darsni baholang'),
    ]

    message = models.CharField(max_length=255)
    url = models.URLField(blank=True, null=True)
    scheduled_at = models.DateTimeField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.message
