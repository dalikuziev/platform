from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import ParentProfile, StudentReport
from .serializers import (
    ParentProfileSerializer,
    StudentReportSerializer,
    ReportGenerateSerializer
)
from accounts.models import User
from courses.models import Course
from assignments.models import Assignment, Submission

class ParentProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ParentProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return get_object_or_404(
            ParentProfile,
            user=self.request.user
        )

class ChildrenReportsView(generics.ListAPIView):
    serializer_class = StudentReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        parent = get_object_or_404(
            ParentProfile,
            user=self.request.user
        )
        return StudentReport.objects.filter(
            student__in=parent.children.all(),
            is_published=True
        ).select_related('student', 'course')

class GenerateReportView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        serializer = ReportGenerateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        student = get_object_or_404(
            User,
            id=serializer.validated_data['student_id'],
            role='student'
        )
        course = get_object_or_404(
            Course,
            id=serializer.validated_data['course_id']
        )

        # Hisobot ma'lumotlarini yig'amiz
        total_assignments = Assignment.objects.filter(
            lesson__course=course
        ).count()
        completed_assignments = Submission.objects.filter(
            assignment__lesson__course=course,
            student=student
        ).count()

        # O'rtacha bahoni hisoblaymiz
        from django.db.models import Avg
        average_grade = Grade.objects.filter(
            submission__assignment__lesson__course=course,
            submission__student=student
        ).aggregate(avg=Avg('score'))['avg'] or 0

        report = StudentReport.objects.create(
            student=student,
            course=course,
            attendance_percentage=85.5,  # Demo qiymat
            average_grade=average_grade,
            completed_assignments=completed_assignments,
            total_assignments=total_assignments,
            teacher_comments="Yaxshi ishlagan!",
            is_published=serializer.validated_data['publish']
        )

        return Response(
            StudentReportSerializer(report).data,
            status=status.HTTP_201_CREATED
        )
