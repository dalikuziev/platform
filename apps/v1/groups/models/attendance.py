from django_extensions.db.models import TimeStampedModel
from django.db import models

class Attendance(TimeStampedModel):
    lesson = models.ForeignKey('courses.Lesson', on_delete=models.CASCADE)
    group = models.ForeignKey('groups.StudentGroup', on_delete=models.CASCADE)
    student = models.ForeignKey('accounts.Student', on_delete=models.CASCADE)
    is_attended = models.BooleanField()