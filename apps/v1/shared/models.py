from django.db import models


class DraftModel(models.Model):
    is_draft = models.BooleanField(default=True)

    class Meta:
        abstract = True
