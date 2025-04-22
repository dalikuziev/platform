from django.contrib import admin
from django.contrib.auth import get_user_model
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Payment
from apps.v1.shared.admin import BaseAdmin

User = get_user_model()


@admin.register(Payment)
class PaymentAdmin(ImportExportModelAdmin, BaseAdmin):
    list_display = [f.name for f in Payment._meta.fields]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            kwargs["queryset"] = User.objects.filter(role='student')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class PaymentResource(resources.ModelResource):
    class Meta:
        model = Payment