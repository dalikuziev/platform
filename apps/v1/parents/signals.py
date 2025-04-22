from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import StudentReport


@receiver(post_save, sender=StudentReport)
def notify_parent_on_report(sender, instance, created, **kwargs):
    if created and instance.is_published:
        for parent in instance.student.parents.all():
            subject = f"Yangi hisobot: {instance.student.username} - {instance.course.title}"
            message = f"Assalomu alaykum {parent.username},\n\n"
            message += f"{instance.student.username}ning {instance.course.title} kursidagi hisoboti:\n"
            # message += f"O'rtacha baho: {instance.average_grade}\n"
            # message += f"Davomat: {instance.attendance_percentage}%\n"
            message += f"Topshiriqlar: {instance.completed_assignments}/{instance.total_assignments}\n\n"
            message += f"O'qituvchi izohlari: {instance.teacher_comments}\n\n"
            message += "EduPlatform jamoasi"

            send_mail(
                subject,
                message,
                'noreply@eduplatform.uz',
                [parent.email],
                fail_silently=True
            )
