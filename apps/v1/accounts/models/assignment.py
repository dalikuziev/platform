from django.db import models
from django_extensions.db.models import TimeStampedModel

class Assignment(TimeStampedModel):
    teacher = models.ForeignKey('accounts.User', on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'},
                                related_name='teacher_assignments')
    students = models.ManyToManyField('accounts.User', limit_choices_to={'role': 'student'},
                                      related_name='student_assignments')