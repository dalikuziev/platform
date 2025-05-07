from django.contrib.auth import get_user_model
from django_extensions.db.models import TimeStampedModel
from django.db import models

User = get_user_model()

class Teacher(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)