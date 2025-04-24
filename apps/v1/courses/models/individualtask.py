from django.db import models
from django_extensions.db.models import TimeStampedModel
from apps.v1.accounts.models import User
from .lesson import Lesson
from ...groups.models import StudentGroup
from ...shared.validators import clean_past_date

class IndividualTask(TimeStampedModel):
    group = models.ForeignKey(
        StudentGroup,
        on_delete=models.CASCADE,
        related_name='individual_tasks'
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='individual_tasks',
        null=True,
        blank=True
    )
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='assigned_tasks',
        limit_choices_to={'role': 'teacher'},
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='individual_tasks',
        limit_choices_to={'role': 'student'},
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField(validators=[clean_past_date])
    class Meta:
        ordering = ['-created']
        unique_together = ['group', 'student', 'title']  # Bir o'quvchiga bir xil nomli topshiriq bir marta
    def __str__(self):
        return f"{self.title} - {self.student.username}"