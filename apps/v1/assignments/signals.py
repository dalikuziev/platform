from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Grade

@receiver(post_save, sender=Grade)
def send_grade_notification(sender, instance, created, **kwargs):
    if created:
        subject = f"Topshirigingiz baholandi: {instance.submission.assignment.title}"
        message = f"Assalomu alaykum {instance.submission.student.username},\n\n"
        message += f"Sizning '{instance.submission.assignment.title}' topshirig'ingiz {instance.score} ball bilan baholandi.\n"
        message += f"Baholovchi: {instance.graded_by.username}\n"
        message += f"Izoh: {instance.feedback}\n\n" if instance.feedback else ""
        message += "EduPlatform jamoasi"

        recipient_email = instance.submission.student.email
        send_mail(
            subject,
            message,
            'noreply@eduplatform.uz',
            [recipient_email],
            fail_silently=True
        )
