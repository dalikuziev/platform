import os

from django.db import models
from django_extensions.db.models import TimeStampedModel

from .lesson import Lesson

class LessonAttachment(TimeStampedModel):
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='attachments',
        verbose_name="Dars"
    )
    file = models.FileField(upload_to='lesson_attachments/', verbose_name="Fayl")
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    description = models.TextField(blank=True, verbose_name="Tavsif")

    def delete(self, *args, **kwargs):
        # faylni o'chiramiz
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)
        # modelni o'chiramiz
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = "Dars materiali"
        verbose_name_plural = "Dars materiallari"

    def __str__(self):
        return self.title
