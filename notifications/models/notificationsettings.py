from django.db import models
from django.contrib.auth import get_user_model
from django_extensions.db.models import TimeStampedModel

User = get_user_model()

class NotificationSettings(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_settings')

    new_exams = models.BooleanField(default=True, verbose_name="New exams")
    exam_announcement = models.BooleanField(default=True, verbose_name="Exam announcement")
    exam_due_soon = models.BooleanField(default=True, verbose_name="Exam due soon")

    new_homework = models.BooleanField(default=True, verbose_name="New homework")
    homework_reviewed = models.BooleanField(default=True, verbose_name="Homework reviewed")
    homework_due_soon = models.BooleanField(default=True, verbose_name="Homework due soon")

    joined_group = models.BooleanField(default=True, verbose_name="Joined a group")
    removed_from_group = models.BooleanField(default=True, verbose_name="Removed from group")

    xp_awarded = models.BooleanField(default=True, verbose_name="XP or Silver awarded")

    def __str__(self):
        return f"Notification settings for {self.user.username}"
