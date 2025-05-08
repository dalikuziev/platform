from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, generics, permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import StudentGroup, Attendance
from .permissions import IsEnrolledStudent
from .serializers import StudentGroupSerializer, AttendanceBulkUpdateSerializer
from ..accounts.permissions import IsTeacherOrAdmin
from ..courses.models import Lesson

User = get_user_model()

class StudentGroupViewSet(viewsets.ModelViewSet):
    serializer_class = StudentGroupSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['course', 'teacher', 'is_active']
    search_fields = ['name']
    ordering_fields = ['start_date', 'end_date', 'students__count']
    ordering = ['-start_date']

    def get_queryset(self):
        teacher = self.request.user
        queryset = StudentGroup.objects.filter(teacher=teacher).prefetch_related('students', 'lesson_days')
        return queryset

class EnrollGroupView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsTeacherOrAdmin]
    def post(self, request, *args, **kwargs):
        group_id = request.data.get('group_id')
        student_id = request.data.get('student_id')
        if not group_id or not student_id:
            return Response({'error': 'group_id va student_id majburiy'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            group = StudentGroup.objects.get(id=group_id)
            student = User.objects.get(id=student_id, role__in=['student', 'teacher'])
        except StudentGroup.DoesNotExist:
            return Response({'error': 'Group topilmadi'}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({'error': 'Student topilmadi'}, status=status.HTTP_404_NOT_FOUND)
        if student in group.students.all():
            return Response({'error': 'Student allaqachon guruhga qo‘shilgan'}, status=status.HTTP_400_BAD_REQUEST)
        group.students.add(student)
        return Response(
            {'status': 'success', 'message': 'Student guruhga muvaffaqiyatli qo‘shildi'},
            status=status.HTTP_200_OK
        )

class AttendanceBulkUpdateView(generics.GenericAPIView):
    serializer_class = AttendanceBulkUpdateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        lesson_id = serializer.validated_data['lesson_id']
        group_id = serializer.validated_data['group_id']
        attendances_data = serializer.validated_data['attendances']

        group = get_object_or_404(StudentGroup, id=group_id)
        lesson = get_object_or_404(Lesson, id=lesson_id)

        for item in attendances_data:
            Attendance.objects.update_or_create(
                lesson=lesson,
                group=group,
                student_id=item['student_id'],
                defaults={'is_attended': item['is_attended']}
            )

        return Response({"detail": "Attendance updated successfully."}, status=status.HTTP_200_OK)