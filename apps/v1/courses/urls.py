from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CourseListCreateView,
    CourseDetailView,
    LessonViewSet,
    IndividualTaskListCreateView,
    IndividualTaskRetrieveUpdateDestroyView
)

router = DefaultRouter()
router.register(r'<int:course_id>/lessons', LessonViewSet, basename='lessons')

urlpatterns = [
    path('', CourseListCreateView.as_view(), name='course-list'),
    path('<int:pk>', CourseDetailView.as_view(), name='course-detail'),
    path('individual-tasks', IndividualTaskListCreateView.as_view(), name='individual-task-list'),
    path('individual-tasks/<int:pk>', IndividualTaskRetrieveUpdateDestroyView.as_view(),
         name='individual-task-detail'),
]
urlpatterns += router.urls