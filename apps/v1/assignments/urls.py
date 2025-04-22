from django.urls import path

from .views import (
    AssignmentListCreateView,
    SubmissionCreateView,
    GradeCreateUpdateView,
    StudentGradesView
)

urlpatterns = [
    path('lessons/<int:lesson_id>/assignments/',
         AssignmentListCreateView.as_view(), name='assignment-list'),
    path('assignments/<int:assignment_id>/submit/',
         SubmissionCreateView.as_view(), name='submission-create'),
    path('submissions/<int:submission_id>/grade/',
         GradeCreateUpdateView.as_view(), name='grade-submission'),
    path('my/grades/',
         StudentGradesView.as_view(), name='student-grades'),
]
