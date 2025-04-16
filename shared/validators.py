from django.core.exceptions import ValidationError
from django.utils.timezone import now

def clean_future_date(value):
    if value < now():
        raise ValidationError("Vaqt hozirgi vaqtdan oldin bo'lishi mumkin emas.")
