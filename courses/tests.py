from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Course, Enrollment
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()
