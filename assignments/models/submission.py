from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User
from courses.models import Course, Lesson
from django_extensions.db.models import TimeStampedModel

from .assignment import Assignment

class Submission(TimeStampedModel):
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name='submissions',
        verbose_name="Topshiriq"
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'},
        related_name='submissions',
        verbose_name="O'quvchi"
    )
    file = models.FileField(upload_to='submissions/%Y/%m/%d/', verbose_name="Fayl")
    yechim = models.TextField(verbose_name="Yechim")

    # submitted_at = models.DateTimeField(auto_now_add=True, verbose_name="Topshirilgan vaqt")
    is_late = models.BooleanField(default=False, verbose_name="Kech qoldirilgan")

    class Meta:
        verbose_name = "Topshiriq topshirig'i"
        verbose_name_plural = "Topshiriq topshiriqlari"
        unique_together = ('assignment', 'student')

    def save(self, *args, **kwargs):
        if None in (self.created, self.assignment.deadline):
            self.is_late = False
        else:
            self.is_late = self.created > self.assignment.deadline
        super().save(*args, **kwargs)
    def __str__(self):
        return f'{self.student} - {self.assignment}'
