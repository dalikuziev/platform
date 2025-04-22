from rest_framework import serializers

from apps.v1.accounts.serializers import UserSerializer
from apps.v1.courses.serializers import LessonSerializer
from .models import Assignment, Submission, Grade


class AssignmentSerializer(serializers.ModelSerializer):
    lesson = LessonSerializer(read_only=True)
    is_submitted = serializers.SerializerMethodField()
    submission_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Assignment
        fields = '__all__'
        read_only_fields = ('created', 'modified')

    def get_is_submitted(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.submissions.filter(student=request.user).exists()
        return False


class SubmissionSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    assignment_title = serializers.CharField(source='assignment.title', read_only=True)

    class Meta:
        model = Submission
        fields = '__all__'
        read_only_fields = ('created',)


class GradeSerializer(serializers.ModelSerializer):
    submission = SubmissionSerializer(read_only=True)
    graded_by = UserSerializer(read_only=True)

    class Meta:
        model = Grade
        fields = '__all__'
        read_only_fields = ('created',)
