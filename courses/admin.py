from django.contrib import admin

from shared.admin import BaseAdmin
from .models import Course, Lesson, LessonAttachment, WeekDay

@admin.register(WeekDay)
class WeekDayAdmin(admin.ModelAdmin):
    pass


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    fields = ('title', 'order', 'is_free', 'created')
    readonly_fields = ('created',)

@admin.register(Course)
class CourseAdmin(BaseAdmin):
    list_display = ('title', 'teacher', 'start_date', 'end_date', 'student_count', 'is_active')
    list_filter = ('is_active', 'start_date', 'teacher')
    search_fields = ('title', 'description', 'teacher__username')
    inlines = [LessonInline]
    actions = ['activate_courses', 'deactivate_courses']

    def student_count(self, obj):
        return obj.students.count()
    student_count.short_description = "O'quvchilar soni"

    @admin.action(description="Tanlangan kurslarni faollashtirish")
    def activate_courses(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description="Tanlangan kurslarni nofaol qilish")
    def deactivate_courses(self, request, queryset):
        queryset.update(is_active=False)

@admin.register(Lesson)
class LessonAdmin(BaseAdmin):
    list_display = ('title', 'course', 'order', 'is_free', 'created')
    list_filter = ('course', 'is_free')
    search_fields = ('title', 'content', 'course__title')
    # ordering = ('course', 'order')

@admin.register(LessonAttachment)
class LessonAttachmentAdmin(BaseAdmin):
    list_display = ('title', 'lesson', 'created')
    list_filter = ('lesson__course',)
    search_fields = ('title', 'description', 'lesson__title')
