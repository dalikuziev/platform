from django.urls import path
from .views import (
    AssignmentListCreateView,
    SubmissionCreateView,
    GradeCreateUpdateView,
    GradeStudentsCreateView,
    GradeStudentsListView,
)

urlpatterns = [
    path('lessons/<int:lesson_id>/assignments/',
         AssignmentListCreateView.as_view(), name='assignment-list'),
    path('<int:assignment_id>/submit/',
         SubmissionCreateView.as_view(), name='submission-create'),
    path('submissions/<int:submission_id>/grade/',
         GradeCreateUpdateView.as_view(), name='grade-submission'),
    path('my-grades/',
         GradeStudentsListView.as_view(), name='student-grades'),
    path('grades/',
         GradeStudentsCreateView.as_view(), name='grades'),
]