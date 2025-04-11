from rest_framework import serializers
from .models import ParentProfile, StudentReport
from accounts.serializers import UserSerializer
from courses.serializers import CourseSerializer

class ParentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    children = UserSerializer(many=True, read_only=True)

    class Meta:
        model = ParentProfile
        fields = '__all__'
        read_only_fields = ('created',)

class StudentReportSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    progress = serializers.SerializerMethodField()

    class Meta:
        model = StudentReport
        fields = '__all__'
        read_only_fields = ('created',)

    def get_progress(self, obj):
        return {
            'completed': obj.completed_assignments,
            'total': obj.total_assignments,
            'percentage': obj.progress_percentage()
        }

class ReportGenerateSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()
    student_id = serializers.IntegerField()
    publish = serializers.BooleanField(default=False)
