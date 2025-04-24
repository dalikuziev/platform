from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import StudentGroup
from .permissions import IsEnrolledStudent
from .serializers import StudentGroupSerializer
from ..accounts.permissions import IsTeacherOrAdmin

User = get_user_model()

class StudentGroupViewSet(viewsets.ModelViewSet):
    queryset = StudentGroup.objects.all().prefetch_related('students', 'lesson_days')
    serializer_class = StudentGroupSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['course', 'teacher', 'is_active']
    search_fields = ['name']
    ordering_fields = ['start_date', 'end_date', 'students__count']
    ordering = ['-start_date']

class EnrollGroupView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsTeacherOrAdmin]
    def post(self, request, *args, **kwargs):
        group_id = request.data.get('group_id')
        student_id = request.data.get('student_id')
        if not group_id or not student_id:
            return Response({'error': 'group_id va student_id majburiy'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            group = StudentGroup.objects.get(id=group_id)
            student = User.objects.get(id=student_id, role='student')
        except StudentGroup.DoesNotExist:
            return Response({'error': 'Group topilmadi'}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({'error': 'Student topilmadi yoki role noto‘g‘ri'}, status=status.HTTP_404_NOT_FOUND)
        if student in group.students.all():
            return Response({'error': 'Student allaqachon guruhga qo‘shilgan'}, status=status.HTTP_400_BAD_REQUEST)
        group.students.add(student)
        return Response(
            {'status': 'success', 'message': 'Student guruhga muvaffaqiyatli qo‘shildi'},
            status=status.HTTP_200_OK
        )