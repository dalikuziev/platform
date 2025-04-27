from django.urls import path
from .views import (
    ChildrenReportsView,
    GenerateReportView, ParentProfileView
)

urlpatterns = [
    path('profile/', ParentProfileView.as_view(), name='parent-profile'),
    path('reports/', ChildrenReportsView.as_view(), name='children-reports'),
    path('generate-report/', GenerateReportView.as_view(), name='generate-report'),
]