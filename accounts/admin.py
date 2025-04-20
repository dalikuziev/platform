from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from shared.admin import BaseAdmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import User

class UserResource(resources.ModelResource):
    class Meta:
        model = User

class CustomUserAdmin(ImportExportModelAdmin, BaseAdmin, UserAdmin):
    resource_classes = [UserResource]
    # Ro'yxat ko'rinishi
    list_display = [f.name for f in User._meta.fields]
    list_display.remove('password')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'phone')
    ordering = ('-date_joined', 'birth_date')

    # Foydalanuvchini tahrirlash formasi
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal Info'), {'fields': ('email', 'phone', 'first_name', 'last_name', 'birth_date')}),
        (_('Permissions'), {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    # Yangi foydalanuvchi qo'shish formasi
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'phone', 'first_name', 'last_name', 'birth_date', 'role'),
        }),
    )

    # Custom actions
    actions = ['make_teacher', 'make_student']

    @admin.action(description="Tanlangan foydalanuvchilarni o'qituvchi qilish")
    def make_teacher(self, request, queryset):
        modified = queryset.update(role='teacher')
        self.message_user(request, f"{modified} ta foydalanuvchi o'qituvchi qilindi")

    @admin.action(description="Tanlangan foydalanuvchilarni o'quvchi qilish")
    def make_student(self, request, queryset):
        modified = queryset.update(role='student')
        self.message_user(request, f"{modified} ta foydalanuvchi o'quvchi qilindi")


# Django ning standart User modelini ro'yxatdan o'chirish
from django.contrib.auth.models import Group

admin.site.unregister(Group)

# Custom User modelini ro'yxatdan o'tkazish
admin.site.register(User, CustomUserAdmin)

# 2. Maxsus Actionlar

@admin.action(description="Tanlangan foydalanuvchilarni bloklash")
def block_users(self, request, queryset):
    queryset.update(is_active=False)

@admin.action(description="Tanlangan foydalanuvchilarni aktivlashtirish")
def unblock_users(self, request, queryset):
    queryset.update(is_active=True)

# 3. Qo'shimcha Filterlar

from django.contrib.admin import SimpleListFilter

class ActiveUserFilter(SimpleListFilter):
    title = 'Faollik holati'
    parameter_name = 'is_active'

    def lookups(self, request, model_admin):
        return (
            ('active', 'Faol foydalanuvchilar'),
            ('inactive', 'Nofaol foydalanuvchilar'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'active':
            return queryset.filter(is_active=True)
        if self.value() == 'inactive':
            return queryset.filter(is_active=False)

# UserAdmin classiga qo'shing
list_filter = (ActiveUserFilter, 'role', 'is_staff')
