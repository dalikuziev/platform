from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Course, Lesson, LessonAttachment, WeekDay, IndividualTask
from shared.admin import BaseAdmin


@admin.register(WeekDay)
class WeekDayAdmin(admin.ModelAdmin):
    pass

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    fields = ('title', 'created')
    readonly_fields = ('created',)

class WeekDayResource(resources.ModelResource):
    class Meta:
        model = WeekDay

class CourseResource(resources.ModelResource):
    class Meta:
        model = Course
class LessonResource(resources.ModelResource):
    class Meta:
        model = Lesson
class LessonAttachmentResource(resources.ModelResource):
    class Meta:
        model = LessonAttachment
class IndividualTaskResource(resources.ModelResource):
    class Meta:
        model = IndividualTask


@admin.register(Course)
class CourseAdmin(BaseAdmin, ImportExportModelAdmin):
    resource_classes = [WeekDayResource]
    list_display = ('title', 'teacher', 'start_date', 'end_date', 'student_count', 'is_active')
    list_filter = ('is_active', 'start_date', 'teacher')
    search_fields = ('title', 'description', 'teacher__username')
    inlines = [LessonInline]
    actions = ['activate_courses', 'deactivate_courses']

    def student_count(self, obj):
        return obj.students.count()
    student_count.short_description = "Students"

    @admin.action(description="Tanlangan kurslarni faollashtirish")
    def activate_courses(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description="Tanlangan kurslarni nofaol qilish")
    def deactivate_courses(self, request, queryset):
        queryset.update(is_active=False)

@admin.register(Lesson)
class LessonAdmin(BaseAdmin, ImportExportModelAdmin):
    resource_classes = [WeekDayResource]
    list_display = ('title', 'course', 'created')
    list_filter = ('course',)
    search_fields = ('title', 'content', 'course__title')
    # ordering = ('course', 'order')

@admin.register(LessonAttachment)
class LessonAttachmentAdmin(BaseAdmin, ImportExportModelAdmin):
    resource_classes = [WeekDayResource]
    list_display = ('title', 'lesson', 'created')
    list_filter = ('lesson__course',)
    search_fields = ('title', 'description', 'lesson__title')

@admin.register(IndividualTask)
class IndividualTaskAdmin(BaseAdmin, ImportExportModelAdmin):
    resource_classes = [WeekDayResource]
    list_display = ('title', 'teacher', 'student', 'course', 'deadline')
    list_filter = ('course', 'teacher')
    search_fields = ('title', 'description', 'student__username')
    readonly_fields = ('created', 'modified')
