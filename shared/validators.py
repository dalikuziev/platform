from django.core.exceptions import ValidationError
from datetime import date, datetime

def clean_future_date(value):
    if isinstance(value, datetime):
        value = value.date()  # datetime ni date turiga o‘tkazamiz
    if value < date.today():
        raise ValidationError("Sana o‘tgan kun bo‘lishi mumkin emas!")
    return value
