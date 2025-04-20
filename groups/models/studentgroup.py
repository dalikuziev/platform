from django.db import models
from django.contrib.auth import get_user_model
from django_extensions.db.models import TimeStampedModel
from icecream import ic
from rest_framework.exceptions import ValidationError
from courses.models import Course, WeekDay
from shared.validators import clean_future_date

User = get_user_model()

class StudentGroup(TimeStampedModel):
    name = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='studentgroups')  # teacher_id
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

    def save(self, *args, **kwargs):
        # Agar teacher bo'lsa, uni students ro'yxatidan chiqaramiz
        if self.students.exists():
            # Get the students based on role
            students = User.objects.filter(role='student')
            # Assign students to the group using set() instead of direct assignment
            self.students.set(students)  # This will set the correct students for the ManyToMany relationship
            ic(self.students.__dict__)

        super().save(*args, **kwargs)  # Odatdagi saqlash

    # def clean(self):
    #     # Validatsiya: teacher students orasida bo'lmasligi kerak
    #     if self.pk:  # faqat saqlangan instanslarda ManyToMany mavjud bo'ladi
    #         if self.teacher in self.students.all():
    #             raise ValidationError("Teacher o'zining guruhida student bo‘la olmaydi.")
