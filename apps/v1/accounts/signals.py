from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Teacher

User = get_user_model()

@receiver(post_save, sender=User)
def create_teacher_profile(sender, instance, created, **kwargs):
    if created and instance.role == 'teacher':
        Teacher.objects.create(user=instance)