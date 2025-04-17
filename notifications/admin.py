from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export.resources import ModelResource
from shared.admin import BaseAdmin
from .models import NotificationSettings
from .models import Notification

class NotificationSettingsResource(ModelResource):
    class Meta:
        model = NotificationSettings

@admin.register(NotificationSettings)
class NotificationSettingsAdmin(BaseAdmin, ImportExportModelAdmin):
    resource_classes = [NotificationSettingsResource]
    list_display = ['user', 'new_exams', 'exam_announcement', 'exam_due_soon', 'xp_awarded']
    search_fields = ['user__username']



class NotificationResource(ModelResource):
    class Meta:
        model = Notification


@admin.register(Notification)
class NotificationAdmin(BaseAdmin, ImportExportModelAdmin):
    resource_classes = [NotificationResource]
    list_display = ('message', 'category', 'scheduled_at', 'is_draft')
    list_filter = ('category', 'is_draft')
    search_fields = ('message',)

