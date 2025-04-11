from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User
from courses.models import Course, Lesson
from django_extensions.db.models import TimeStampedModel

from .submission import Submission

class Grade(TimeStampedModel):
    submission = models.OneToOneField(
        Submission,
        on_delete=models.CASCADE,
        related_name='grade',
        verbose_name="Topshiriq topshirig'i"
    )
    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Ball"
    )
    feedback = models.TextField(blank=True, verbose_name="Izoh")
    graded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'role': 'teacher'},
        verbose_name="Baholovchi"
    )
    # graded_at = models.DateTimeField(auto_now_add=True, verbose_name="Baholangan vaqt")

    class Meta:
        verbose_name = "Baho"
        verbose_name_plural = "Boholar"

    def __str__(self):
        return f"{self.submission.student.username} - {self.score}"
