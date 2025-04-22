from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from .models import Assignment, Grade, StudentAssignment
from .serializers import AssignmentSerializer, SubmissionSerializer, GradeSerializer, StudentAssignmentSerializer
from .permissions import IsCourseOwner, IsEnrolledStudent
from rest_framework.permissions import IsAuthenticated

class AssignmentListCreateView(generics.ListCreateAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [IsCourseOwner]

    def get_queryset(self):
        lesson_id = self.kwargs['lesson_id']
        return Assignment.objects.filter(lesson_id=lesson_id)

    def perform_create(self, serializer):
        lesson_id = self.kwargs['lesson_id']
        serializer.save(lesson_id=lesson_id)

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
    permission_classes = [IsCourseOwner]

    def create(self, request, *args, **kwargs):
        submission_id = kwargs['submission_id']
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            submission_id=submission_id,
            graded_by=request.user
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class StudentGradesView(generics.ListAPIView):
    serializer_class = GradeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Grade.objects.filter(
            submission__student=self.request.user
        ).select_related('submission', 'submission__assignment')

class StudentAssignmentViewSet(viewsets.ModelViewSet):
    queryset = StudentAssignment.objects.all()
    serializer_class = StudentAssignmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Faqat o'ziga tegishli topshiriqlarni ko'rsin (agar kerak bo‘lsa)
        user = self.request.user
        return StudentAssignment.objects.filter(student=user) if not user.is_staff else StudentAssignment.objects.all()
