from django.db import models
from accounts.models import User
from django_extensions.db.models import TimeStampedModel
from ..models import Course, Lesson

class IndividualTask(TimeStampedModel):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='individual_tasks'
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='individual_tasks',
        null=True,
        blank=True
    )
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='assigned_tasks',
        limit_choices_to={'role': 'teacher'},
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='individual_tasks',
        limit_choices_to={'role': 'student'},
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
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
