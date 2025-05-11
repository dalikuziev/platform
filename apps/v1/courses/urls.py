from rest_framework_nested import routers
from apps.v1.courses.views import CourseViewSet, LessonViewSet, IndividualTaskViewSet

router = routers.SimpleRouter()
router.register(r'', CourseViewSet, basename='course')

courses_router = routers.NestedSimpleRouter(router, r'', lookup='course')
courses_router.register(r'lessons', LessonViewSet, basename='course-lessons')
# router.register('individual-tasks', IndividualTaskViewSet, basename='individual-tasks')

urlpatterns = router.urls + courses_router.urls