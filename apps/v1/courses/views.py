from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Course, Lesson, LessonAttachment, IndividualTask
from .serializers import CourseSerializer, LessonSerializer, IndividualTaskSerializer, IndividualTaskCreateSerializer
from .permissions import IsCourseTeacher, IsEnrolledStudent

class CourseListCreateView(generics.ListCreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Course.objects.filter(is_active=True)
        if self.request.user.is_authenticated:
            if self.request.user.role == 'teacher':
                return queryset.filter(teacher=self.request.user)
            elif self.request.user.role == 'student':
                return queryset.filter(students=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # ID ni URL dan olish
        pk = self.kwargs.get('pk')
        return get_object_or_404(Course, pk=pk)

class LessonListCreateView(generics.ListCreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsCourseTeacher]

    def get_queryset(self):
        return Lesson.objects.filter(
            course_id=self.kwargs['course_id']
        ).select_related('course').prefetch_related('attachments')

    def perform_create(self, serializer):
        serializer.save(course_id=self.kwargs['course_id'])

class EnrollCourseView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsEnrolledStudent]

    def post(self, request, *args, **kwargs):
        course = generics.get_object_or_404(Course, pk=kwargs['pk'])
        course.students.add(request.user)
        return Response(
            {'status': 'success', 'message': 'Kursga muvaffaqiyatli yozildingiz'},
            status=status.HTTP_200_OK
        )

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

