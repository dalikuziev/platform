from django.db import models
from django_extensions.db.models import TimeStampedModel
from apps.v1.accounts.models import User
from .assignment import Assignment

class Submission(TimeStampedModel):
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'},
        related_name='submissions'
    )
    file = models.FileField(upload_to='submissions/%Y/%m/%d/')
    answer = models.TextField()
    class Meta:
        unique_together = ('assignment', 'student',)
    def save(self, *args, **kwargs):
        if None in (self.created, self.assignment.deadline):
            self.is_late = False
        else:
            self.is_late = self.created > self.assignment.deadline
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.student} - {self.assignment}'