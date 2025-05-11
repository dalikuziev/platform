from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
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
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0
    )
    feedback = models.TextField(
        blank=True,
        null=True,
    )
    graded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'teacher'},
        related_name='graded_assignments',
    )

    def save(self, **kwargs):
        if not self.graded_by:
            raise ValidationError("Grade must be assigned by a teacher (graded_by is required).")
        super().save(**kwargs)

    def __str__(self):
        return f"{self.submission.student.username} - {self.score}"