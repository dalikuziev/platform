from django.contrib import admin
from .models import ParentProfile, StudentReport

class StudentReportInline(admin.TabularInline):
    model = StudentReport
    extra = 0
    readonly_fields = ('created',)
    fields = ('student', 'course', 'is_published')

@admin.register(ParentProfile)
class ParentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'children_list')
    search_fields = ('user__username', 'phone')
    filter_horizontal = ('children',)

    def children_list(self, obj):
        return ", ".join([child.username for child in obj.children.all()])
    children_list.short_description = "Children"

@admin.register(StudentReport)
class StudentReportAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'attendance_percentage', 'is_published')
    list_filter = ('course', 'is_published')
    search_fields = ('student__username', 'course__title')
    readonly_fields = ('created',)
    actions = ['publish_reports', 'unpublish_reports']

    @admin.action(description="Tanlangan hisobotlarni nashr qilish")
    def publish_reports(self, request, queryset):
        queryset.update(is_published=True)

    @admin.action(description="Nashrdan olib tashlash")
    def unpublish_reports(self, request, queryset):
        queryset.update(is_published=False)
