from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User
from courses.models import Course
from django_extensions.db.models import TimeStampedModel


class StudentReport(TimeStampedModel):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'},
        related_name='reports',
        verbose_name="O'quvchi"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='reports',
        verbose_name="Kurs"
    )
    attendance_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Davomat foizi"
    )
    average_grade = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="O'rtacha baho"
    )
    completed_assignments = models.PositiveIntegerField(verbose_name="Bajargan topshiriqlar")
    total_assignments = models.PositiveIntegerField(verbose_name="Jami topshiriqlar")
    teacher_comments = models.TextField(blank=True, verbose_name="O'qituvchi izohlari")
    # generated_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False, verbose_name="Publik")

    class Meta:
        verbose_name = "O'quvchi hisoboti"
        verbose_name_plural = "O'quvchilar hisobotlari"
        unique_together = ('student', 'course')
        ordering = ['-created']

    def progress_percentage(self):
        return (self.completed_assignments / self.total_assignments) * 100
