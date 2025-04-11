from django.db import models
from accounts.models import User
from django_extensions.db.models import TimeStampedModel
from ..models import Course, Lesson

class IndividualTask(TimeStampedModel):
    STATUS_CHOICES = (
        ('assigned', 'Topshirilgan'),
        ('in_progress', 'Bajarilmoqda'),
        ('completed', 'Yakunlangan'),
        ('rejected', 'Rad etilgan'),
        ('accepted', 'Qabul qilingan'),
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='individual_tasks',
        verbose_name="Kurs"
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='individual_tasks',
        verbose_name="Dars",
        null=True,
        blank=True
    )
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='assigned_tasks',
        limit_choices_to={'role': 'teacher'},
        verbose_name="O'qituvchi"
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='individual_tasks',
        limit_choices_to={'role': 'student'},
        verbose_name="O'quvchi"
    )
    title = models.CharField(max_length=255, verbose_name="Sarlavha")
    description = models.TextField(verbose_name="Tavsif")
    deadline = models.DateTimeField(verbose_name="Topshirish muddati")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='assigned',
        verbose_name="Holati"
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Individual topshiriq"
        verbose_name_plural = "Individual topshiriqlar"
        ordering = ['-created']
        unique_together = ['course', 'student', 'title']  # Bir o'quvchiga bir xil nomli topshiriq bir marta

    def __str__(self):
        return f"{self.title} - {self.student.username}"

    def save(self, *args, **kwargs):
        # O'qituvchi kursning o'qituvchisi ekanligini tekshiramiz
        if self.teacher != self.course.teacher:
            raise ValueError("Faqat kurs o'qituvchisi topshiriq berishi mumkin")

        # O'quvchi kursda ro'yxatdan o'tganligini tekshiramiz
        if not self.course.students.filter(id=self.student.id).exists():
            raise ValueError("O'quvchi kursda ro'yxatdan o'tmagan")

        super().save(*args, **kwargs)
