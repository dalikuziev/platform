from django.db import models
from django_extensions.db.models import TimeStampedModel
from .course import Course
from ...shared.models import DraftModel

class Lesson(TimeStampedModel, DraftModel):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
    )
    title = models.CharField(max_length=200)
    content = models.TextField(null=True, blank=True)
    video_url = models.URLField(blank=True, null=True)
    is_exam = models.BooleanField(default=False)
    class Meta:
        unique_together = ('course', 'title')

    def __str__(self):
        return f"{self.course.title} - {self.title}"