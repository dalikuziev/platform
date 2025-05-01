from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from apps.v1.shared.admin import BaseAdmin
from .models import Course, Lesson, LessonAttachment, IndividualTask, Enrollment

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    fields = ('title', 'created')
    readonly_fields = ('created',)

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

class EnrollmentResource(resources.ModelResource):
    class Meta:
        model = Enrollment

@admin.register(Course)
class CourseAdmin(BaseAdmin, ImportExportModelAdmin):
    resource_classes = [CourseResource]
    list_display = [f.name for f in Course._meta.fields]
    list_filter = ('is_active', 'owner')
    search_fields = ('title', 'description', 'owner__username')
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
    resource_classes = [CourseResource]
    list_display = [f.name for f in Lesson._meta.fields]
    list_filter = ('course',)
    search_fields = ('title', 'content', 'course__title')

@admin.register(LessonAttachment)
class LessonAttachmentAdmin(BaseAdmin, ImportExportModelAdmin):
    resource_classes = [CourseResource]
    list_display = [f.name for f in LessonAttachment._meta.fields]
    list_filter = ('lesson__course',)
    search_fields = ('title', 'description', 'lesson__title')

@admin.register(IndividualTask)
class IndividualTaskAdmin(BaseAdmin, ImportExportModelAdmin):
    resource_classes = [CourseResource]
    list_display = [f.name for f in IndividualTask._meta.fields]
    list_filter = ('group', 'teacher')
    search_fields = ('title', 'description', 'student__username')
    readonly_fields = ('created', 'modified')

@admin.register(Enrollment)
class EnrollmentAdmin(BaseAdmin, ImportExportModelAdmin):
    list_display = [f.name for f in Enrollment._meta.fields]
    list_filter = ('group',)
    search_fields = ('student__username', 'student__first_name', 'student__last_name', 'group__name')