from rest_framework import serializers
from .models import Course, Lesson, LessonAttachment, IndividualTask
from accounts.serializers import UserSerializer

class LessonAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonAttachment
        fields = ['id', 'title', 'file', 'description', 'created']
        read_only_fields = ['created']

class LessonSerializer(serializers.ModelSerializer):
    attachments = LessonAttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = [
            'id', 'title', 'content', 'video_url', 'duration',
            'is_free', 'created', 'attachments',
        ]
        read_only_fields = ['created']

class CourseSerializer(serializers.ModelSerializer):
    teacher = UserSerializer(read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)
    student_count = serializers.IntegerField(read_only=True)
    is_enrolled = serializers.SerializerMethodField()

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Sarlavha bo'sh bo'lishi mumkin emas")
        return value
    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Narh manfiy bo'lishi mumkin emas")
        return value

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'cover_image', 'teacher',
            'price', 'start_date', 'end_date', 'is_active', 'created',
            'lessons', 'student_count', 'is_enrolled'
        ]
        read_only_fields = ['teacher', 'created', 'modified']

    def get_is_enrolled(self, obj):
        user = self.context['request'].user
        return obj.students.filter(id=user.id).exists()

class IndividualTaskSerializer(serializers.ModelSerializer):
    teacher = serializers.StringRelatedField()
    student = serializers.StringRelatedField()
    course = serializers.StringRelatedField()
    lesson = serializers.StringRelatedField()
    deadline = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = IndividualTask
        fields = [
            'id', 'course', 'lesson', 'teacher', 'student',
            'title', 'description', 'deadline', 'status',
            'created', 'modified'
        ]
        read_only_fields = ['teacher', 'created', 'modified']

class IndividualTaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndividualTask
        fields = [
            'course', 'lesson', 'student',
            'title', 'description', 'deadline'
        ]
    def validate(self, data):
        # O'qituvchi kurs o'qituvchisi ekanligini tekshiramiz
        if self.context['request'].user != data['course'].teacher:
            raise serializers.ValidationError(
                "Faqat kurs o'qituvchisi topshiriq berishi mumkin"
            )

        # O'quvchi kursda ekanligini tekshiramiz
        if not data['course'].students.filter(id=data['student'].id).exists():
            raise serializers.ValidationError(
                "O'quvchi kursda ro'yxatdan o'tmagan"
            )
        return data
