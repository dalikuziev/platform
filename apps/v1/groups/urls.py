from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import StudentGroupViewSet, EnrollGroupView

router = DefaultRouter()
router.register(r'student-groups', StudentGroupViewSet)

urlpatterns = [
    path('<int:pk>/enroll', EnrollGroupView.as_view(), name='group-enroll'),
]

urlpatterns += router.urls