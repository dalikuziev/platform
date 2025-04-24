from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django_extensions.db.models import TimeStampedModel
from apps.v1.shared.validators import clean_future_date

User = get_user_model()

class Payment(TimeStampedModel):
    PAYMENT_TYPES = [
        ('card', 'Card'),
        ('cash', 'Cash'),
    ]
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments', limit_choices_to={'role': 'student'})
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=50, choices=PAYMENT_TYPES)
    paid_at = models.DateTimeField(default=timezone.now, validators=[clean_future_date])
    def clean(self):
        if self.student.role != 'student':
            raise ValidationError("Faqat studentlar uchun to'lov yaratilishi mumkin.")
    def save(self, *args, **kwargs):
        self.full_clean()  # clean() metodini chaqirish uchun
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.student} - {self.payment_type} - ${self.amount}"