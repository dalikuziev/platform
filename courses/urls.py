from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    CourseListCreateView,
    CourseDetailView,
    LessonListCreateView,
    EnrollCourseView,
    IndividualTaskListCreateView,
    IndividualTaskRetrieveUpdateDestroyView
)

urlpatterns = [
    path('', CourseListCreateView.as_view(), name='course-list'),
    path('<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('<int:pk>/enroll/', EnrollCourseView.as_view(), name='course-enroll'),
    path('<int:course_id>/lessons/', LessonListCreateView.as_view(), name='lesson-list'),
    path('individual-tasks/', IndividualTaskListCreateView.as_view(), name='individual-task-list'),
    path('individual-tasks/<int:pk>/', IndividualTaskRetrieveUpdateDestroyView.as_view(),
         name='individual-task-detail'),
]