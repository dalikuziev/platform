from django.contrib.auth import get_user_model
from django.db import models
from groups.models import StudentGroup
from . import Lesson
from django_extensions.db.models import TimeStampedModel
from shared.models import DraftModel

User = get_user_model()

class Attendance(TimeStampedModel, DraftModel):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    is_attended = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.lesson.title} - {self.student.username} - {self.state}"
