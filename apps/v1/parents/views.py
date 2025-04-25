from django.shortcuts import get_object_or_404
from icecream import ic
from rest_framework import generics, status, permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.v1.accounts.models import User
from apps.v1.assignments.models import Assignment, Submission
from apps.v1.courses.models import Course
from .models import ParentProfile, StudentReport
from .serializers import (
    ParentProfileSerializer,
    StudentReportSerializer,
    ReportGenerateSerializer
)
from ..accounts.permissions import IsParent

# class ParentProfileViewSet(viewsets.ModelViewSet):
#     serializer_class = ParentProfileSerializer
#     permission_classes = [permissions.IsAuthenticated, IsParent]
#     http_method_names = ['get']
#
#     def get_object(self):
#         return get_object_or_404(
#             ParentProfile,
#             user=self.request.user
#         )
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
    permission_classes = [permissions.IsAuthenticated, IsParent]
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
        report = StudentReport.objects.create(
            student=student,
            course=course,
            completed_assignments=completed_assignments,
            total_assignments=total_assignments,
            teacher_comments="Yaxshi ishlagan!",
            is_published=serializer.validated_data['publish']
        )
        return Response(
            StudentReportSerializer(report).data,
            status=status.HTTP_201_CREATED
        )