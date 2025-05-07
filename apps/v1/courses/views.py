from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status, viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Course, Lesson, IndividualTask
from .permissions import IsCourseOwnerOrReadOnly
from .serializers import CourseSerializer, LessonSerializer, IndividualTaskSerializer, IndividualTaskCreateSerializer
from ..accounts.permissions import IsTeacher

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsTeacher]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created', 'title']

    def get_queryset(self):
        user = self.request.user
        return Course.objects.filter(owner=user)

class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsCourseOwnerOrReadOnly]

    def get_queryset(self):
        course_id = self.kwargs.get('course_pk')
        return Lesson.objects.filter(course_id=course_id)

    def perform_create(self, serializer):
        course_id = self.kwargs.get('course_pk')
        serializer.save(course_id=course_id)

class IndividualTaskViewSet(viewsets.ModelViewSet):
    serializer_class = IndividualTaskSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def get_queryset(self):
        user = self.request.user
        return IndividualTask.objects.filter(teacher=user)

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)