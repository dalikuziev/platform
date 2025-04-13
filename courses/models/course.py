from django.db import models
from accounts.models import User
from django_extensions.db.models import TimeStampedModel

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
    title = models.CharField(max_length=200, verbose_name="Course name")
    description = models.TextField()
    cover_image = models.ImageField(upload_to='course_covers/', null=True, blank=True)
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'teacher'},
        related_name='taught_courses'
    )
    students = models.ManyToManyField(
        User,
        limit_choices_to={'role__in': ['student', 'teacher']},
        related_name='enrolled_courses',
        blank=True
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    start_date = models.DateField()
    lesson_days = models.ManyToManyField(
        WeekDay,
        blank=True
    )
    lesson_start_time = models.TimeField(
        default='14:00',
    )
    lesson_duration = models.PositiveIntegerField(
        default=90
    )
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title
