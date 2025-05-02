from django.contrib import admin
from django import forms
from django.contrib.auth import get_user_model
from icecream import ic
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from apps.v1.shared.base_admin import BaseAdmin
from .models import Assignment, Submission, Grade

User = get_user_model()

class SubmissionInline(admin.TabularInline):
    model = Submission
    extra = 0
    readonly_fields = ('created',)
    show_change_link = True

class GradeInline(admin.StackedInline):
    model = Grade
    extra = 0
    readonly_fields = ('created',)

class AssignmentResource(resources.ModelResource):
    class Meta:
        model = Assignment

class SubmissionResource(resources.ModelResource):
    class Meta:
        model = Submission

class GradeResource(resources.ModelResource):
    class Meta:
        model = Grade

class GradeAdminForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limit to teachers
        self.fields['graded_by'].queryset = User.objects.filter(role='teacher')
        self.fields['graded_by'].required = True

@admin.register(Assignment)
class AssignmentAdmin(BaseAdmin, ImportExportModelAdmin):
    resource_classes = [AssignmentResource]
    list_display = [f.name for f in Assignment._meta.fields]
    list_filter = ('lesson__course',)
    search_fields = ('title', 'lesson__title')
    inlines = [SubmissionInline]

# @admin.register(Submission)
class SubmissionAdmin(BaseAdmin, ImportExportModelAdmin):
    resource_classes = [SubmissionResource]
    list_display = [f.name for f in Submission._meta.fields]
    # list_filter = ('assignment__lesson__course',)
    # search_fields = ('student__username', 'assignment__title')
    # inlines = [GradeInline]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "student":
            ic(db_field.name)
            ic(request.user)
            ic(Submission.objects.filter(student=request.user))
            kwargs["queryset"] = Submission.objects.filter(student=request.user)
        # return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Grade)
class GradeAdmin(BaseAdmin, ImportExportModelAdmin):
    form = GradeAdminForm
    resource_classes = [GradeResource]
    list_display = [f.name for f in Grade._meta.fields]
    list_filter = ('graded_by', 'submission__assignment__lesson__course')
    search_fields = ('submission__student__username', 'feedback')