from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Course, Lesson, IndividualTask
from .serializers import CourseSerializer, LessonSerializer, IndividualTaskSerializer, IndividualTaskCreateSerializer
from ..accounts.permissions import IsTeacher

class CourseListCreateView(generics.ListCreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def get_queryset(self):
        queryset = Course.objects.filter(is_active=True)
        return queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # ID ni URL dan olish
        pk = self.kwargs.get('pk')
        return get_object_or_404(Course, pk=pk)

# class LessonListCreateView(generics.ListCreateAPIView):
#     serializer_class = LessonSerializer
#     # permission_classes = [IsAuthenticated, IsTeacher]
#     def get_queryset(self):
#         return Lesson.objects.filter(
#             course_id=self.kwargs['course_id']
#         ).select_related('course').prefetch_related('attachments')
#
#     def perform_create(self, serializer):
#         serializer.save(course_id=self.kwargs['course_id'])
#
#     def get_permissions(self):
#         if self.request.method == 'POST':
#             return [IsAuthenticated(), IsTeacher()]
#         return [IsAuthenticated()]
class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    def get_queryset(self):
        return Lesson.objects.filter(
            course_id=self.kwargs['course_id']
        ).select_related('course').prefetch_related('attachments')

    def perform_create(self, serializer):
        serializer.save(course_id=self.kwargs['course_id'])

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsTeacher()]
        return [IsAuthenticated()]

class IndividualTaskListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        if user.role == 'teacher':
            return IndividualTask.objects.filter(teacher=user)
        return IndividualTask.objects.filter(student=user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return IndividualTaskCreateSerializer
        return IndividualTaskSerializer

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

class IndividualTaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = IndividualTaskSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'teacher':
            return IndividualTask.objects.filter(teacher=user)
        return IndividualTask.objects.filter(student=user)