from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django_extensions.db.models import TimeStampedModel

from apps.v1.accounts.models import User
from apps.v1.courses.models import Course


class StudentReport(TimeStampedModel):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'},
        related_name='reports'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='reports'
    )
    attendance_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    completed_assignments = models.PositiveIntegerField()
    total_assignments = models.PositiveIntegerField()
    teacher_comments = models.TextField(blank=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'course')
        ordering = ['-created']

    def progress_percentage(self):
        return (self.completed_assignments / self.total_assignments) * 100
