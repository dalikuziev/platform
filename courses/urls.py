from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    CourseListCreateView,
    CourseDetailView,
    LessonListCreateView,
    EnrollCourseView
)

urlpatterns = [
    path('', CourseListCreateView.as_view(), name='course-list'),
    path('<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('<int:pk>/enroll/', EnrollCourseView.as_view(), name='course-enroll'),
    path('<int:course_id>/lessons/', LessonListCreateView.as_view(), name='lesson-list'),
]
