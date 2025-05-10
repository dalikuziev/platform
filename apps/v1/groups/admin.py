from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from apps.v1.shared.admin import BaseAdmin
from .models import StudentGroup, WeekDay, Attendance

User = get_user_model()

class StudentGroupForm(forms.ModelForm):
    class Meta:
        model = StudentGroup
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)  # requestni ushlab olamiz
        super().__init__(*args, **kwargs)
        if request:
            # teacher fieldni cheklaymiz: teacher faqat `role='teacher'` bo'lgan user bo'lishi kerak
            self.fields['teacher'].queryset = User.objects.filter(role='teacher').exclude(id=request.user.id)

class StudentGroupResource(resources.ModelResource):
    class Meta:
        model = StudentGroup

class WeekDayResource(resources.ModelResource):
    class Meta:
        model = WeekDay

@admin.register(WeekDay)
class WeekDayAdmin(admin.ModelAdmin):
    resource_classes = [WeekDayResource]

@admin.register(StudentGroup)
class StudentGroupAdmin(ImportExportModelAdmin, BaseAdmin):
    list_display = [f.name for f in StudentGroup._meta.fields if f.name != 'students'] + ['students_list', 'students_count']
    def students_list(self, obj):
        students = obj.students.all()[:2]
        student_names = [str(student) for student in students]
        result = ", ".join(student_names)
        if obj.students.count() > 3:
            result += "..."
        return result
    def students_count(self, obj):
        return obj.students.count()
    students_count.short_description = 'Students Count'
    def get_form(self, request, obj=None, **kwargs):
        kwargs['form'] = StudentGroupForm  # o'z formimizni beramiz
        form = super().get_form(request, obj, **kwargs)
        # formga request qo‘shamiz
        class RequestForm(form):
            def __new__(cls, *args, **kwargs2):
                kwargs2['request'] = request
                return form(*args, **kwargs2)
        return RequestForm

class AttendanceResource(resources.ModelResource):
    class Meta:
        model = Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    resource_classes = [AttendanceResource]
    list_display = [f.name for f in Attendance._meta.fields]