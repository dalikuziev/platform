from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CourseListCreateView,
    CourseDetailView,
    LessonListCreateView,
    IndividualTaskViewSet
)
router = DefaultRouter()
router.register('individual-tasks', IndividualTaskViewSet, basename='individual-tasks')

urlpatterns = [
    path('', CourseListCreateView.as_view(), name='course-list'),
    path('<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('<int:course_id>/lessons/', LessonListCreateView.as_view(), name='lesson-list'),
]
urlpatterns += router.urls