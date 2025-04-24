from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.v1.groups.permissions import IsEnrolledStudent, IsGroupTeacher
from .models import Assignment, Grade
from .serializers import AssignmentSerializer, SubmissionSerializer, GradeSerializer
from ..courses.permissions import IsCourseOwner


class AssignmentListCreateView(generics.ListCreateAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated, IsCourseOwner]
    def get_queryset(self):
        lesson_id = self.kwargs['lesson_id']
        return Assignment.objects.filter(lesson__course__owner=self.request.user, lesson_id=lesson_id)

    # def perform_create(self, serializer):
    #     lesson_id = self.kwargs['lesson_id']
    #     serializer.save(lesson_id=lesson_id)

class SubmissionCreateView(generics.CreateAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [IsEnrolledStudent]
    def perform_create(self, serializer):
        assignment_id = self.kwargs['assignment_id']
        serializer.save(
            assignment_id=assignment_id,
            student=self.request.user
        )

class GradeCreateUpdateView(generics.CreateAPIView, generics.UpdateAPIView):
    serializer_class = GradeSerializer
    permission_classes = [IsGroupTeacher]

    def perform_create(self, serializer):
        serializer.save(graded_by=self.request.user)
    # def create(self, request, *args, **kwargs):
    #     submission_id = kwargs['submission_id']
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save(
    #         submission_id=submission_id,
    #         graded_by=request.user
    #     )
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

class StudentGradesView(generics.ListAPIView):
    serializer_class = GradeSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Grade.objects.filter(
            submission__student=self.request.user
        ).select_related('submission', 'submission__assignment')