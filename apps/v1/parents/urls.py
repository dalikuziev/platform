from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    ChildrenReportsView,
    GenerateReportView, ParentProfileView
)

# router = DefaultRouter()
# router.register('', ParentProfileViewSet, basename='parent-profile')

urlpatterns = [
    path('profile/', ParentProfileView.as_view(), name='parent-profile'),
    path('reports/', ChildrenReportsView.as_view(), name='children-reports'),
    path('generate-report/', GenerateReportView.as_view(), name='generate-report'),
] # + router.urls