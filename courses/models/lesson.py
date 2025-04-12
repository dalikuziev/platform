from django.db import models
from .course import Course
from django_extensions.db.models import TimeStampedModel

class Lesson(TimeStampedModel):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name="Kurs"
    )
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    content = models.TextField(verbose_name="Mazmuni")
    video_url = models.URLField(blank=True, null=True, verbose_name="Video havolasi")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib raqami")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Dars"
        verbose_name_plural = "Darslar"
        ordering = ['order']
        unique_together = ('course', 'order')

    def __str__(self):
        return f"{self.course.title} - {self.title}"
#