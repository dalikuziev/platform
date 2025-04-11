# from django.urls import reverse
# from rest_framework.test import APITestCase
# from rest_framework import status
# from accounts.models import User
# from courses.models import Course, Lesson
# from .models import Assignment, Submission, Grade
#
# class AssignmentAPITests(APITestCase):
#     def setUp(self):
#         # Test foydalanuvchilari
#         self.teacher = User.objects.create_user(
#             username='teacher1',
#             email='teacher1@example.com',
#             password='testpass123',
#             role='teacher'
#         )
#         self.student = User.objects.create_user(
#             username='student1',
#             email='student1@example.com',
#             password='testpass123',
#             role='student'
#         )
#
#         # Test kursi va darsi
#         self.course = Course.objects.create(
#             title='Matematika',
#             teacher=self.teacher,
#             start_date='2023-09-01',
#             end_date='2023-12-31'
#         )
#         self.course.students.add(self.student)
#         self.lesson = Lesson.objects.create(
#             course=self.course,
#             title='Algebra',
#             order=1
#         )
#
#         # Test topshirig'i
#         self.assignment = Assignment.objects.create(
#             lesson=self.lesson,
#             title='Birinchi topshiriq',
#             description='Matematik masalalar',
#             deadline='2023-10-31T23:59:00Z',
#             max_score=100
#         )
#
#     def test_assignment_creation_by_teacher(self):
#         """O'qituvchi yangi topshiriq yaratishi"""
#         url = reverse('assignment-list', kwargs={'lesson_id': self.lesson.id})
#         self.client.force_authenticate(user=self.teacher)
#
#         data = {
#             'title': 'Yangi topshiriq',
#             'description': 'Test topshiriq tavsifi',
#             'deadline': '2023-11-15T23:59:00Z',
#             'max_score': 50
#         }
#
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Assignment.objects.count(), 2)
#         self.assertEqual(response.data['title'], 'Yangi topshiriq')
#
#     def test_assignment_creation_by_student_fails(self):
#         """O'quvchi topshiriq yarata olmasligi"""
#         url = reverse('assignment-list', kwargs={'lesson_id': self.lesson.id})
#         self.client.force_authenticate(user=self.student)
#
#         response = self.client.post(url, {}, format='json')
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#
#     def test_submission_creation_by_student(self):
#         """O'quvchi topshiriq topshirishi"""
#         url = reverse('submission-create', kwargs={'assignment_id': self.assignment.id})
#         self.client.force_authenticate(user=self.student)
#
#         # Fayl yuklash uchun mock fayl
#         from io import BytesIO
#         from django.core.files.uploadedfile import SimpleUploadedFile
#         test_file = SimpleUploadedFile("test_file.txt", b"file_content")
#
#         data = {
#             'file': test_file
#         }
#
#         response = self.client.post(url, data, format='multipart')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Submission.objects.count(), 1)
#         self.assertTrue(Submission.objects.filter(student=self.student).exists())
#
#     def test_grade_creation_by_teacher(self):
#         """O'qituvchi baho qo'yishi"""
#         # Avval topshiriq topshirilishi kerak
#         submission = Submission.objects.create(
#             assignment=self.assignment,
#             student=self.student,
#             file='submissions/test.txt'
#         )
#
#         url = reverse('grade-submission', kwargs={'submission_id': submission.id})
#         self.client.force_authenticate(user=self.teacher)
#
#         data = {
#             'score': 85.5,
#             'feedback': 'Yaxshi ishlagan!'
#         }
#
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Grade.objects.count(), 1)
#         self.assertEqual(Grade.objects.first().score, 85.5)
#
#     def test_student_grades_list(self):
#         """O'quvchi o'z baholarini ko'rishi"""
#         # Test uchun baho yaratamiz
#         submission = Submission.objects.create(
#             assignment=self.assignment,
#             student=self.student,
#             file='submissions/test.txt'
#         )
#         Grade.objects.create(
#             submission=submission,
#             score=90,
#             feedback='Ajoyib!',
#             graded_by=self.teacher
#         )
#
#         url = reverse('student-grades')
#         self.client.force_authenticate(user=self.student)
#
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#         self.assertEqual(response.data[0]['score'], '90.00')
#
#     def test_late_submission_flag(self):
#         """Kech topshirilgan topshiriqlarni tekshirish"""
#         import datetime
#         from django.utils import timezone
#
#         # Deadline o'tgan topshiriq yaratamiz
#         past_deadline = timezone.now() - datetime.timedelta(days=1)
#         late_assignment = Assignment.objects.create(
#             lesson=self.lesson,
#             title='Kech topshirish testi',
#             deadline=past_deadline,
#             max_score=100
#         )
#
#         # Topshirish
#         submission = Submission.objects.create(
#             assignment=late_assignment,
#             student=self.student,
#             file='submissions/late.txt'
#         )
#
#         self.assertTrue(submission.is_late)
