# from django.urls import reverse
# from rest_framework.test import APITestCase
# from rest_framework import status
# from accounts.models import User
# from courses.models import Course
# from .models import ParentProfile, StudentReport
#
# class ParentAPITests(APITestCase):
#     def setUp(self):
#         # Foydalanuvchilar
#         self.parent_user = User.objects.create_user(
#             username='parent1',
#             email='parent1@example.com',
#             password='testpass123',
#             role='parent'
#         )
#         self.student_user = User.objects.create_user(
#             username='student1',
#             email='student1@example.com',
#             password='testpass123',
#             role='student'
#         )
#
#         # Ota-ona profil
#         self.parent_profile = ParentProfile.objects.create(
#             user=self.parent_user,
#             phone='+998901234567'
#         )
#         self.parent_profile.children.add(self.student_user)
#
#         # Kurs va hisobot
#         self.course = Course.objects.create(
#             title='Matematika',
#             teacher=User.objects.create_user(
#                 username='teacher1',
#                 email='teacher1@example.com',
#                 password='testpass123',
#                 role='teacher'
#             )
#         )
#         self.report = StudentReport.objects.create(
#             student=self.student_user,
#             course=self.course,
#             attendance_percentage=90,
#             average_grade=85.5,
#             completed_assignments=8,
#             total_assignments=10,
#             is_published=True
#         )
#
#     def test_parent_profile_retrieve(self):
#         url = reverse('parent-profile')
#         self.client.force_authenticate(user=self.parent_user)
#
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['user']['username'], 'parent1')
#         self.assertEqual(len(response.data['children']), 1)
#
#     def test_children_reports_list(self):
#         url = reverse('children-reports')
#         self.client.force_authenticate(user=self.parent_user)
#
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#         self.assertEqual(response.data[0]['average_grade'], '85.50')
#
#     def test_report_generation_by_admin(self):
#         admin_user = User.objects.create_superuser(
#             username='admin',
#             email='admin@example.com',
#             password='adminpass123'
#         )
#
#         url = reverse('generate-report')
#         self.client.force_authenticate(user=admin_user)
#
#         data = {
#             'course_id': self.course.id,
#             'student_id': self.student_user.id,
#             'publish': True
#         }
#
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertTrue(StudentReport.objects.filter(is_published=True).count(), 2)
