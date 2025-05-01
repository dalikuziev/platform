from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django_extensions.db.models import TimeStampedModel
from apps.v1.courses.models import Lesson
from apps.v1.shared.validators import clean_future_date, clean_past_date

class Assignment(TimeStampedModel):
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='assignments'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    deadline = models.DateTimeField(validators=[clean_past_date])
    max_score = models.PositiveIntegerField(
        default=100,
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    class Meta:
        ordering = ['deadline']

    def __str__(self):
        return f"{self.lesson.course.title} - {self.title}"