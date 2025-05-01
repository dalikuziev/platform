from rest_framework import serializers
from apps.v1.accounts.serializers import UserSerializer
from .models import Assignment, Submission, Grade

class AssignmentSerializer(serializers.ModelSerializer):
    is_submitted = serializers.SerializerMethodField()
    submission_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Assignment
        fields = '__all__'

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

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'
        extra_kwargs = {
            'graded_by': {'required': True},
        }