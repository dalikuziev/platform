from django.contrib.auth import get_user_model
from django_extensions.db.models import TimeStampedModel
from django.db import models
from courses.models import Lesson
User = get_user_model()

class StudentAssignment(TimeStampedModel):
    STATES = (
        ('qabul qilingan', 'Qabul qilingan'),
        ('berilmagan', 'Berilmagan'),
        ('qaytarilgan', 'Qaytarilgan'),
        ('bajarilmagan', 'Bajarilmagan'),
    )
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.CharField(max_length=20, choices=STATES, default='berilmagan')

    def __str__(self):
        return f"{self.lesson.title} - {self.student.username} - {self.state}" # noqa

