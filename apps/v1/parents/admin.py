from django.contrib import admin
from .models import ParentProfile, StudentReport
from import_export.admin import ImportExportModelAdmin
from import_export.resources import  ModelResource

from apps.v1.shared.admin import BaseAdmin


class StudentReportInline(admin.TabularInline):
    model = StudentReport
    extra = 0
    readonly_fields = ('created',)
    fields = ('student', 'course', 'is_published')


class ParentProfileResource(ModelResource):
    class Meta:
        model = ParentProfile

class StudentReportResource(ModelResource):
    class Meta:
        model = StudentReport


@admin.register(ParentProfile)
class ParentProfileAdmin(BaseAdmin, ImportExportModelAdmin):
    resource_classes = [ParentProfileResource]
    list_display = [f.name for f in ParentProfile._meta.fields]
    search_fields = ('user__username', 'phone')
    filter_horizontal = ('children',)

    def children_list(self, obj):
        return ", ".join([child.username for child in obj.children.all()])
    children_list.short_description = "Children"

@admin.register(StudentReport)
class StudentReportAdmin(BaseAdmin, ImportExportModelAdmin):
    resource_classes = [StudentReportResource]
    list_display = [f.name for f in StudentReport._meta.fields]
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
