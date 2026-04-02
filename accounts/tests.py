from django.test import TestCase, Client
from django.urls import reverse

from .models import User


class LoginTests(TestCase):
	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_user(
			username='testuser',
			email='user@example.com',
			password='secret123',
			institute_id='INST1',
			role='STUDENT',
		)

	def test_login_with_email(self):
		resp = self.client.post(reverse('accounts:login'), {
			'identifier': 'user@example.com',
			'password': 'secret123',
		})
		# Successful login should set session auth user id
		session = self.client.session
		self.assertIn('_auth_user_id', session)

	def test_login_with_institute_id(self):
		resp = self.client.post(reverse('accounts:login'), {
			'identifier': 'INST1',
			'password': 'secret123',
		})
		session = self.client.session
		self.assertIn('_auth_user_id', session)

