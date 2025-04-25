from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    LessonListCreateView,
    IndividualTaskViewSet, CourseViewSet
)
router = DefaultRouter()
router.register('individual-tasks', IndividualTaskViewSet, basename='individual-tasks')
router.register('', CourseViewSet, basename='course')

urlpatterns = [
    path('<int:course_id>/lessons/', LessonListCreateView.as_view(), name='lesson-list'),
]
urlpatterns += router.urls