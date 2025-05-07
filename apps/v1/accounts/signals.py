from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Teacher

User = get_user_model()

@receiver(pre_save, sender=User)
def cache_old_role_before_save(sender, instance, **kwargs):
    if instance.pk:
        try:
            instance._old_role = User.objects.get(pk=instance.pk).role
        except User.DoesNotExist:
            instance._old_role = None

@receiver(post_save, sender=User)
def create_or_delete_teacher_on_role_change(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'teacher':
            Teacher.objects.create(user=instance)
    else:
        old_role = getattr(instance, '_old_role', None)
        # Agar teacher bo‘ldi — yaratamiz
        if old_role != instance.role and instance.role == 'teacher':
            if not Teacher.objects.filter(user=instance).exists():
                transaction.on_commit(lambda: Teacher.objects.create(user=instance))
        # Agar teacher bo‘lmay qolsa — o‘chiramiz
        elif old_role == 'teacher' and instance.role != 'teacher':
            def delete_teacher():
                Teacher.objects.filter(user=instance).delete()
            transaction.on_commit(delete_teacher)