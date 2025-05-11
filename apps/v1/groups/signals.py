from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from rest_framework.generics import get_object_or_404

from apps.v1.accounts.models import Student
from apps.v1.groups.models import StudentGroup

User = get_user_model()

@receiver(m2m_changed, sender=StudentGroup.students.through)
def create_student_profile_on_add(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        for user_id in pk_set:
            user = User.objects.filter(pk=user_id).first()
            if user and user.role in ('student', 'teacher'):
                Student.objects.get_or_create(user=user)