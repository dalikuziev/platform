from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Course, Lesson, IndividualTask
from .serializers import CourseSerializer, LessonSerializer, IndividualTaskSerializer, IndividualTaskCreateSerializer
from ..accounts.permissions import IsTeacher

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def get_queryset(self):
        return Course.objects.filter(is_active=True, owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        # Faqat o‘ziga tegishli bo‘lgan kursni olish
        instance = get_object_or_404(
            Course.objects.filter(owner=request.user, is_active=True),
            pk=kwargs.get("pk")
        )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class LessonListCreateView(generics.ListCreateAPIView):
    serializer_class = LessonSerializer
    # permission_classes = [IsAuthenticated, IsTeacher]
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

class IndividualTaskViewSet(viewsets.ModelViewSet):
    serializer_class = IndividualTaskSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def get_queryset(self):
        user = self.request.user
        return IndividualTask.objects.filter(teacher=user)

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

# class IndividualTaskListCreateView(generics.ListCreateAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     def get_queryset(self):
#         user = self.request.user
#         if user.role == 'teacher':
#             return IndividualTask.objects.filter(teacher=user)
#         return IndividualTask.objects.filter(student=user)
#
#     def get_serializer_class(self):
#         if self.request.method == 'POST':
#             return IndividualTaskCreateSerializer
#         return IndividualTaskSerializer
#
#     def perform_create(self, serializer):
#         serializer.save(teacher=self.request.user)
#
# class IndividualTaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = IndividualTaskSerializer
#
#     def get_queryset(self):
#         user = self.request.user
#         if user.role == 'teacher':
#             return IndividualTask.objects.filter(teacher=user)
#         return IndividualTask.objects.filter(student=user)