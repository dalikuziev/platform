from django.contrib import admin

from shared.admin import BaseAdmin
from .models import Assignment, Submission, Grade


class SubmissionInline(admin.TabularInline):
    model = Submission
    extra = 0
    readonly_fields = ('created', 'is_late')
    show_change_link = True


class GradeInline(admin.StackedInline):
    model = Grade
    extra = 0
    readonly_fields = ('created',)


@admin.register(Assignment)
class AssignmentAdmin(BaseAdmin):
    list_display = ('title', 'lesson', 'deadline', 'max_score')
    list_filter = ('lesson__course',)
    search_fields = ('title', 'lesson__title')
    inlines = [SubmissionInline]


@admin.register(Submission)
class SubmissionAdmin(BaseAdmin):
    list_display = ('assignment', 'student', 'created', 'is_late')
    list_filter = ('assignment__lesson__course', 'is_late')
    search_fields = ('student__username', 'assignment__title')
    inlines = [GradeInline]


@admin.register(Grade)
class GradeAdmin(BaseAdmin):
    list_display = ('submission', 'score', 'graded_by', 'created')
    list_filter = ('graded_by', 'submission__assignment__lesson__course')
    search_fields = ('submission__student__username', 'feedback')
