import os
from django.db import models
from django_extensions.db.models import TimeStampedModel
from .lesson import Lesson

class LessonAttachment(TimeStampedModel):
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='attachments',
    )
    file = models.FileField(upload_to='lesson_attachments/')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    def delete(self, *args, **kwargs):
        # faylni o'chiramiz
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)
        # modelni o'chiramiz
        super().delete(*args, **kwargs)
    def __str__(self):
        return self.title