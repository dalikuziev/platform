from django.db import models
from .course import Course
from django_extensions.db.models import TimeStampedModel

from ...shared.models import DraftModel


class Lesson(TimeStampedModel, DraftModel):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    video_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.course.title} - {self.title}"
