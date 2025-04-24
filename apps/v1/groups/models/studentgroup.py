from django.contrib.auth import get_user_model
from django.db import models
from django_extensions.db.models import TimeStampedModel
from apps.v1.courses.models import Course, WeekDay
from apps.v1.shared.validators import clean_future_date

User = get_user_model()

class StudentGroup(TimeStampedModel):
    name = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='studentgroups',
                                limit_choices_to={'role': 'teacher'})
    students = models.ManyToManyField(
        User,
        limit_choices_to={'role__in': ['student', 'teacher']},
        related_name='enrolled_groups',
        blank=True
    )
    start_date = models.DateField(validators=[clean_future_date])
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
    end_date = models.DateField(null=True, blank=True, validators=[clean_future_date])
    is_active = models.BooleanField(default=True)  # faol / tugagan
    def __str__(self):
        return self.name