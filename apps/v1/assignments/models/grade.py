from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django_extensions.db.models import TimeStampedModel
from .submission import Submission

User = get_user_model()

class Grade(TimeStampedModel):
    submission = models.OneToOneField(
        Submission,
        on_delete=models.CASCADE,
        related_name='grade'
    )
    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    feedback = models.TextField(blank=True, verbose_name="Izoh")
    graded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'role': 'teacher'}
    )
    def __str__(self):
        return f"{self.submission.student.username} - {self.score}"