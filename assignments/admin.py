from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Assignment, Submission, Grade
from shared.admin import BaseAdmin

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


@admin.register(Assignment)
class AssignmentAdmin(BaseAdmin, ImportExportModelAdmin):
    resource_classes = [AssignmentResource]
    list_display = ('title', 'lesson', 'deadline', 'max_score')
    list_filter = ('lesson__course',)
    search_fields = ('title', 'lesson__title')
    inlines = [SubmissionInline]

@admin.register(Submission)
class SubmissionAdmin(BaseAdmin, ImportExportModelAdmin):
    resource_classes = [SubmissionResource]
    list_display = ('assignment', 'student', 'created')
    list_filter = ('assignment__lesson__course',)
    search_fields = ('student__username', 'assignment__title')
    inlines = [GradeInline]

@admin.register(Grade)
class GradeAdmin(BaseAdmin, ImportExportModelAdmin):
    resource_classes = [GradeResource]
    list_display = ('submission', 'score', 'graded_by', 'created')
    list_filter = ('graded_by', 'submission__assignment__lesson__course')
    search_fields = ('submission__student__username', 'feedback')
