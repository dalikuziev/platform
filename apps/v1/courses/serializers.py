from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.v1.accounts.serializers import UserSerializer
from .models import Course, Lesson, LessonAttachment, IndividualTask

class LessonAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonAttachment
        fields = '__all__'
        read_only_fields = ['created']

class LessonSerializer(serializers.ModelSerializer):
    attachments = LessonAttachmentSerializer(many=True, read_only=True)
    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ['created']

class CourseSerializer(serializers.ModelSerializer):
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
        fields = '__all__'
        read_only_fields = ['owner']

class IndividualTaskSerializer(serializers.ModelSerializer):
    # teacher = serializers.StringRelatedField()
    # student = serializers.StringRelatedField()
    # course = serializers.StringRelatedField()
    # lesson = serializers.StringRelatedField()
    # deadline = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    class Meta:
        model = IndividualTask
        fields = '__all__'
        read_only_fields = ['teacher']

class IndividualTaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndividualTask
    fields = '__all__'
    def validate(self, data):
        # O'qituvchi kurs o'qituvchisi ekanligini tekshiramiz
        if self.context['request'].user != data['group'].teacher:
            raise serializers.ValidationError(
                "Faqat kurs o'qituvchisi topshiriq berishi mumkin"
            )
        # O'quvchi kursda ekanligini tekshiramiz
        if not data['course'].students.filter(id=data['student'].id).exists():
            raise ValidationError(
                "O'quvchi kursda ro'yxatdan o'tmagan"
            )
        return data