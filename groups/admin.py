from django.contrib import admin
from django.contrib.auth import get_user_model
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import StudentGroup
from shared.admin import BaseAdmin
from django import forms

User = get_user_model()

@admin.register(StudentGroup)
class StudentGroupAdmin(ImportExportModelAdmin, BaseAdmin):
    list_display = [f.name for f in StudentGroup._meta.fields]

class StudentGroupResource(resources.ModelResource):
    class Meta:
        model = StudentGroup

class StudentGroupForm(forms.ModelForm):
    class Meta:
        model = StudentGroup
        fields = '__all__'


