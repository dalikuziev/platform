from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User
from courses.models import Course, Lesson
from django_extensions.db.models import TimeStampedModel

from shared.validators import clean_future_date

class Assignment(TimeStampedModel):
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='assignments'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    deadline = models.DateTimeField(validators=[clean_future_date])
    max_score = models.PositiveIntegerField(
        default=100,
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )

    class Meta:
        ordering = ['deadline']

    def __str__(self):
        return f"{self.lesson.course.title} - {self.title}"
