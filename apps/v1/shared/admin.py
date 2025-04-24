from django.contrib import admin

class BaseAdmin(admin.ModelAdmin):
    list_per_page = 10
    class Meta:
        abstract = True