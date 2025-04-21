from rest_framework import viewsets, filters
from .models import StudentGroup
from .serializers import StudentGroupSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

class StudentGroupViewSet(viewsets.ModelViewSet):
    queryset = StudentGroup.objects.all().prefetch_related('students', 'lesson_days')
    serializer_class = StudentGroupSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['course', 'teacher', 'is_active']
    search_fields = ['name']
    ordering_fields = ['start_date', 'end_date', 'students__count']
    ordering = ['-start_date']
