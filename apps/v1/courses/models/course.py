from django.contrib.auth import get_user_model
from django.db import models
from django_extensions.db.models import TimeStampedModel

User = get_user_model()

class WeekDay(TimeStampedModel):
    DAY_CHOICES = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    )
    day = models.CharField(max_length=30, choices=DAY_CHOICES, unique=True)
    def __str__(self):
        return self.day

class Course(TimeStampedModel):
    title = models.CharField(unique=True, max_length=200, verbose_name="Course name")
    description = models.TextField()
    cover_image = models.ImageField(upload_to='course_covers/', null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'}, related_name='taught_courses')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title