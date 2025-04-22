from rest_framework.routers import DefaultRouter

from .views import StudentGroupViewSet

router = DefaultRouter()
router.register(r'student-groups', StudentGroupViewSet)

urlpatterns = router.urls
