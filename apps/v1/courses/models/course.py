from django.contrib.auth import get_user_model
from django.db import models
from django_extensions.db.models import TimeStampedModel

User = get_user_model()

class Course(TimeStampedModel):
    title = models.CharField(
        unique=True,
        max_length=200,
        verbose_name="Course name"
    )
    description = models.TextField(
        blank=True,
        null=True,
    )
    cover_image = models.ImageField(
        upload_to='course_covers/',
        null=True,
        blank=True
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={
            'role': 'teacher'
        },
        related_name='taught_courses'
    )
    price = models.PositiveIntegerField(
        default=0
    )
    is_active = models.BooleanField(
        default=True
    )
    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title