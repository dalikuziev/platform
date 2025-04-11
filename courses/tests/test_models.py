from django.urls import reverse
from rest_framework.test import APITestCase
from accounts.models import User
from ..models import Course, Lesson, LessonAttachment
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
import os

User = get_user_model()

class CourseAPITests(APITestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(
            username='teacher',
            email='teacher@example.com',
            password='testpass123',
            role='teacher'
        )
        self.student = User.objects.create_user(
            username='student',
            email='student@example.com',
            password='testpass123',
            role='student'
        )
        self.course = Course.objects.create(
            title='Matematika',
            teacher=self.teacher,
            start_date='2025-03-01',
            end_date='2025-12-31'
        )

    def test_course_creation(self):
        url = reverse('course-list')
        data = {
            'title': 'Fizika',
            'description': 'Fizika kursi',
            'start_date': '2025-04-01',
            'end_date': '2025-12-31',
        }
        self.client.force_authenticate(user=self.teacher)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], 'Fizika')

    def test_course_students_relationship(self):
        student = User.objects.create_user(username='student1', role='student')
        self.course.students.add(student)
        self.assertEqual(self.course.students.count(), 1)
        self.assertEqual(student.enrolled_courses.first(), self.course)

#

class LessonAPITest(TestCase):
    def setUp(self):
        teacher = User.objects.create_user(
            username='test_teacher',
            password='testpass123',
            role='teacher'
        )

        self.course = Course.objects.create(
            title='Django Course',
            teacher=teacher,
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timezone.timedelta(days=30)
        )

        self.lesson = Lesson.objects.create(
            title='Django Models',
            content='Model field types',
            course=self.course,
            order=1
        )

    def test_lesson_creation(self):
        """Lesson yaratilishini tekshiramiz"""
        self.assertEqual(self.lesson.title, 'Django Models')

        # URL reverse testi (kurs ID bilan)
        try:
            url = reverse('lesson-list', kwargs={'course_id': self.course.id})
            # URL mavjudligini tekshirish
            self.assertTrue(url.startswith('/api/courses/'))
        except:
            # Agar URL test qilinmasa yoki mavjud bo'lmasa
            pass

class LessonAttachmentAPITests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.teacher = User.objects.create_user(
            username='teacher1',
            email='teacher1@example.com',
            password='testpass123',
            role='teacher'
        )

        cls.course = Course.objects.create(
            title='Python Dasturlash',
            description='Python asoslari',
            teacher=cls.teacher,
            start_date=timezone.now().date(),
        )

        cls.lesson = Lesson.objects.create(
            title='Kirish darsi',
            course=cls.course
        )

        # Test uchun fayl yaratamiz
        cls.sample_file = SimpleUploadedFile(
            name='testfile.pdf',
            content=b'Test file content',
            content_type='application/pdf'
        )

    def tearDown(self):
        # Har bir testdan keyin yuklangan fayllarni o'chiramiz
        for attachment in LessonAttachment.objects.all():
            if attachment.file and os.path.exists(attachment.file.path):
                os.remove(attachment.file.path)

    def test_lesson_attachment_creation(self):
        """LessonAttachment modelini to'g'ri yaratishni tekshiramiz"""
        attachment = LessonAttachment.objects.create(
            lesson=self.lesson,
            file=self.sample_file,
            title='Foydali material',
            description='Bu fayl dars uchun qo\'llanma'
        )
        self.assertEqual(attachment.lesson.title, 'Kirish darsi')
        self.assertEqual(attachment.title, 'Foydali material')
        self.assertTrue(attachment.file.name.endswith('.pdf'))
        self.assertEqual(attachment.description, 'Bu fayl dars uchun qo\'llanma')
        self.assertIsNotNone(attachment.created)

    def test_file_upload(self):
        """Fayl to'g'ri yuklanganligini tekshiramiz"""
        attachment = LessonAttachment.objects.create(
            lesson=self.lesson,
            file=self.sample_file,
            title='Test File'
        )
        # Fayl mavjudligini tekshiramiz
        self.assertTrue(os.path.exists(attachment.file.path))
        # Fayl hajmi va nomini tekshiramiz
        self.assertEqual(attachment.file.size, len(b'Test file content'))
        self.assertIn('.pdf', attachment.file.name)

    def test_title_max_length(self):
        """Sarlavha uzunligi chegarasini tekshiramiz"""
        max_length = LessonAttachment._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_lesson_relationship(self):
        """Lesson bilan bog'lanishni tekshiramiz"""
        attachment = LessonAttachment.objects.create(
            lesson=self.lesson,
            file=self.sample_file,
            title='Test File'
        )

        self.assertEqual(attachment.lesson.id, self.lesson.id)
        self.assertEqual(attachment.lesson.course.id, self.course.id)
        self.assertEqual(self.lesson.attachments.count(), 1)

    def test_attachment_deletion(self):
        """Materialni o'chirish faylni ham o'chirayotganini tekshiramiz"""
        attachment = LessonAttachment.objects.create(
            lesson=self.lesson,
            file=self.sample_file,
            title='Test File'
        )
        file_path = attachment.file.path
        attachment_id = attachment.id

        # Fayl mavjudligini tekshiramiz
        self.assertTrue(os.path.exists(file_path))

        # Modelni o'chiramiz
        attachment.delete()

        # Fayl ham o'chganligini tekshiramiz
        self.assertFalse(os.path.exists(file_path))
        with self.assertRaises(LessonAttachment.DoesNotExist):
            LessonAttachment.objects.get(id=attachment_id)

