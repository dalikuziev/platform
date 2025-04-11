from django.db import models
from accounts.models import User
from django_extensions.db.models import TimeStampedModel

class WeekDay(TimeStampedModel):
    DAY_CHOICES = (
        ('Monday', 'Dushanba'),
        ('Tuesday', 'Seshanba'),
        ('Wednesday', 'Chorshanba'),
        ('Thursday', 'Payshanba'),
        ('Friday', 'Juma'),
        ('Saturday', 'Shanba'),
        ('Sunday', 'Yakshanba'),
    )
    day = models.CharField(max_length=30, choices=DAY_CHOICES, unique=True)
    def __str__(self):
        return self.day

class Course(TimeStampedModel):
    title = models.CharField(max_length=200, verbose_name="Kurs nomi")
    description = models.TextField(verbose_name="Tavsif")
    cover_image = models.ImageField(upload_to='course_covers/', null=True, blank=True)
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'teacher'},
        related_name='taught_courses',
        verbose_name="O'qituvchi"
    )
    students = models.ManyToManyField(
        User,
        limit_choices_to={'role__in': ['student', 'teacher']},
        related_name='enrolled_courses',
        blank=True,
        verbose_name="O'quvchilar"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Narxi")
    start_date = models.DateField(verbose_name="Boshlanish sanasi")
    lesson_days = models.ManyToManyField(
        WeekDay,
        verbose_name="Dars kunlari",
        help_text="Dars bo'ladigan hafta kunlari",
        blank=True,
    )
    lesson_start_time = models.TimeField(
        verbose_name="Dars boshlanish vaqti",
        help_text="Har bir darsning boshlanish vaqti (soat:daqiqa)",
        default='14:00'
    )
    lesson_duration = models.PositiveIntegerField(
        verbose_name="Dars davomiyligi (daqiqa)",
        default=90,
        help_text="Har bir darsning davomiyligi daqiqalarda"
    )
    end_date = models.DateField(verbose_name="Tugash sanasi", null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Kurs"
        verbose_name_plural = "Kurslar"
        ordering = ['-created']

    def __str__(self):
        return self.title
