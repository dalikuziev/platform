from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import StudentGroup

User = get_user_model()

class StudentGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentGroup
        fields = '__all__'  # yoki agar kerakli fieldlar bo‘lsa, aniq yozib chiqamiz
        read_only_fields = ['students_list', 'students_count']
    def get_students_list(self, obj):
        students = obj.students.all()[:3]
        names = [str(student) for student in students]
        result = ", ".join(names)
        if obj.students.count() > 3:
            result += "..."
        return result
    def get_students_count(self, obj):
        return obj.students.count()

class AttendanceInputSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
    is_attended = serializers.BooleanField()

class AttendanceBulkUpdateSerializer(serializers.Serializer):
    lesson_id = serializers.IntegerField()
    group_id = serializers.IntegerField()
    attendances = AttendanceInputSerializer(many=True)