from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIRequestFactory
from apps.v1.accounts.models import User
from ..models import Course, Lesson, LessonAttachment
from ..serializers import (
    LessonAttachmentSerializer,
    LessonSerializer,
    CourseSerializer
)
import os

class SerializersTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Test uchun ma'lumotlar yaratamiz
        cls.factory = APIRequestFactory()
        cls.teacher = User.objects.create_user(
            username='teacher1',
            email='teacher1@example.com',
            password='testpass123',
            role='teacher'
        )
        cls.student = User.objects.create_user(
            username='student1',
            email='student1@example.com',
            password='testpass123',
            role='student'
        )
        cls.course = Course.objects.create(
            title='Python Dasturlash',
            description='Python asoslari',
            teacher=cls.teacher,
            price=100000,
            start_date='2023-01-01',
            end_date='2023-12-31'
        )
        cls.lesson = Lesson.objects.create(
            title='Kirish darsi',
            content='Python haqida tushuncha',
            course=cls.course,
            duration=90,
            # order=1
        )
        cls.attachment = LessonAttachment.objects.create(
            lesson=cls.lesson,
            file=SimpleUploadedFile('test.pdf', b'content'),
            title='Dars materiali'
        )

    def tearDown(self):
        # Fayllarni tozalash
        for attachment in LessonAttachment.objects.all():
            if attachment.file and os.path.exists(attachment.file.path):
                os.remove(attachment.file.path)

    def test_lesson_attachment_serializer(self):
        serializer = LessonAttachmentSerializer(instance=self.attachment)
        data = serializer.data
        self.assertEqual(data['id'], self.attachment.id)
        self.assertEqual(data['title'], 'Dars materiali')
        self.assertIn('test.pdf', data['file'])
        self.assertEqual(data['description'], '')
        self.assertIsNotNone(data['created'])

        # Create test
        new_data = {
            'title': 'Yangi material',
            'description': 'Yangi tavsif',
            'file': SimpleUploadedFile('new.pdf', b'new content')
        }
        serializer = LessonAttachmentSerializer(data=new_data)
        self.assertTrue(serializer.is_valid())

        # Update test
        update_data = {'title': 'Yangilangan sarlavha'}
        serializer = LessonAttachmentSerializer(instance=self.attachment, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.attachment.refresh_from_db()
        self.assertEqual(self.attachment.title, 'Yangilangan sarlavha')

    def test_lesson_serializer(self):
        request = self.factory.get('/')
        request.user = self.student
        serializer = LessonSerializer(
            instance=self.lesson,
            context={'request': request}
        )

        data = serializer.data
        self.assertEqual(data['id'], self.lesson.id)
        self.assertEqual(data['title'], 'Kirish darsi')
        self.assertEqual(data['duration'], 90)
        self.assertEqual(len(data['attachments']), 1)

        # Create test
        new_data = {
            'title': 'Yangi dars',
            'content': 'Yangi kontent',
            'duration': 60,
            # 'order': 2
        }
        serializer = LessonSerializer(data=new_data, context={'request': request})
        self.assertTrue(serializer.is_valid())

    def test_course_serializer(self):
        request = self.factory.get('/')
        request.user = self.student
        # Studentni kursga qo'shamiz
        self.course.students.add(self.student)
        serializer = CourseSerializer(
            instance=self.course,
            context={'request': request}
        )
        data = serializer.data
        self.assertEqual(data['id'], self.course.id)
        self.assertEqual(data['title'], 'Python Dasturlash')
        self.assertEqual(data['price'], '100000.00')
        self.assertEqual(len(data['lessons']), 1)
        self.assertTrue(data['is_enrolled'])
        self.assertEqual(data['teacher']['username'], 'teacher1')

        # Enroll bo'lmagan holat
        self.course.students.remove(self.student)
        serializer = CourseSerializer(
            instance=self.course,
            context={'request': request}
        )
        self.assertFalse(serializer.data['is_enrolled'])

        # Create test (o'qituvchi uchun)
        request.user = self.teacher
        new_data = {
            'title': 'Yangi kurs',
            'description': 'Yangi kurs tavsifi',
            'price': 150000,
            'start_date': '2023-02-01',
            'end_date': '2023-12-31'
        }
        serializer = CourseSerializer(data=new_data, context={'request': request})
        self.assertTrue(serializer.is_valid())
        course = serializer.save(teacher=self.teacher)
        self.assertEqual(course.teacher.id, self.teacher.id)

    def test_course_validation(self):
        # Noto'g'ri ma'lumot yaratish
        invalid_data = {
            'title': '',  # Bo'sh sarlavha
            'description': 'Test',
            'price': -100  # Manfiy narx
        }
        serializer = CourseSerializer(data=invalid_data)

        # Serializer valid bo'lmasligi kerak
        self.assertFalse(serializer.is_valid(),
                         "Serializer noto'g'ri ma'lumotlar uchun valid deb qaytmaydi kerak")

        # Qaysi maydonlarda xatolik borligini tekshirish
        self.assertIn('title', serializer.errors)
        self.assertIn('price', serializer.errors)


    # def test_course_validation(self):
    #     # Sana validatsiyasi
    #     invalid_data = {
    #         'title': 'Noto\'g\'ri kurs',
    #         'description': 'Tugash sanasi boshlanish sanasidan oldin',
    #         'price': 100000,
    #         'start_date': '2023-12-31',
    #         'end_date': '2023-01-01'
    #     }
    #     serializer = CourseSerializer(data=invalid_data)
    #     self.assertFalse(serializer.is_valid())
        # self.assertIn('non_field_errors', serializer.errors)

        # # Narx validatsiyasi
        # invalid_data = {
        #     'title': 'Noto\'g\'ri narx',
        #     'description': 'Manfiy narx',
        #     'price': -100,
        #     'start_date': '2023-01-01',
        #     'end_date': '2023-12-31'
        # }
        # serializer = CourseSerializer(data=invalid_data)
        # self.assertFalse(serializer.is_valid())
        # self.assertIn('price', serializer.errors)














