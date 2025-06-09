from django.test import TestCase
from django.urls import reverse, resolve
from .models import User
from django.test import SimpleTestCase


class RegistrationTest(TestCase):
    def test_student_registration(self):
        response = self.client.post(reverse('student_register'), {
            'email': 'student@test.com',
            'username': 'student',
            'password1': 'securepassword123',
            'password2': 'securepassword123',
            'grade_level': '10'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(User.objects.filter(role='student').exists())


class TestUrls(SimpleTestCase):
    def test_login_url(self):
        url = reverse('accounts:login')
        self.assertEqual(resolve(url).func.__name__, 'RoleBasedLoginView')