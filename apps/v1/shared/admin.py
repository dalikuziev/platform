from apps.v1.accounts.admin import CustomUserAdmin
from apps.v1.assignments.admin import AssignmentAdmin, SubmissionAdmin, GradeAdmin
from apps.v1.assignments.models import Submission, Grade
from django.contrib.admin import AdminSite
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from icecream import ic

from apps.v1.assignments.models.assignment import Assignment
from apps.v1.courses.admin import CourseAdmin, LessonAdmin, LessonAttachmentAdmin, IndividualTaskAdmin
from apps.v1.courses.models import Course, Lesson, LessonAttachment, IndividualTask
from apps.v1.groups.admin import StudentGroupAdmin
from apps.v1.groups.models import StudentGroup
from apps.v1.parents.admin import StudentReportAdmin, ParentProfileAdmin
from apps.v1.parents.models import ParentProfile, StudentReport
from apps.v1.payments.admin import PaymentAdmin
from apps.v1.payments.models import Payment

User = get_user_model()

class AdminAdminSite(AdminSite):
    site_header = 'Admin Panel'
    site_title = 'Admin'
    index_title = 'Welcome Admin'

    def has_permission(self, request):
        user = request.user
        return user.is_active and (user.role == 'admin' or user.is_superuser)

admin_site = AdminAdminSite(name='admin_panel')
# admin_site.register(Group)
# admin_site.register(User, CustomUserAdmin)
# admin_site.register(Submission, SubmissionAdmin)
# admin_site.register(Grade, GradeAdmin)
# admin_site.register(Course, CourseAdmin)
# admin_site.register(Lesson, LessonAdmin)
# admin_site.register(LessonAttachment, LessonAttachmentAdmin)
# admin_site.register(IndividualTask, IndividualTaskAdmin)
# admin_site.register(StudentGroup, StudentGroupAdmin)
# admin_site.register(ParentProfile, ParentProfileAdmin)
# admin_site.register(StudentReport, StudentReportAdmin)
# admin_site.register(Payment, PaymentAdmin)

    # def has_permission(self, request):
    #     user = request.user
    #     ic(user)
    #     ic(user.role)
    #     ic(user.is_staff)
    #     return user.is_active and user.role == 'student'

class TeacherAdminSite(AdminSite):
    site_header = 'Teacher Panel'
    site_title = 'Teacher Dashboard'
    index_title = 'Welcome Teacher'

    def has_permission(self, request):
        user = request.user
        return user.is_active and user.role == 'teacher'

teacher_site = TeacherAdminSite(name='teacher_panel')
teacher_site.register(Assignment, AssignmentAdmin)

class StudentAdminSite(AdminSite):
    site_header = 'Student Panel'
    site_title = 'Student Dashboard'
    index_title = 'Welcome Student'

student_site = StudentAdminSite(name='student_panel')
student_site.register(Assignment, AssignmentAdmin)
student_site.register(Submission, SubmissionAdmin)

class ParentAdminSite(AdminSite):
    site_header = 'Parent Panel'
    site_title = 'Parent Dashboard'
    index_title = 'Welcome Parent'

    def has_permission(self, request):
        user = request.user
        return user.is_active and user.role == 'parents'

parent_site = ParentAdminSite(name='parent_panel')