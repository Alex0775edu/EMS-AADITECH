from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model


User = get_user_model()


class CsrfIntegrationTests(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'Password123!'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_login_post_without_csrf_fails(self):
        c = Client(enforce_csrf_checks=True)
        login_url = reverse('accounts:login')
        response = c.post(login_url, {'identifier': self.username, 'password': self.password})
        # Without CSRF token, Django should return 403
        self.assertEqual(response.status_code, 403)

    def test_login_post_with_csrf_succeeds(self):
        c = Client(enforce_csrf_checks=True)
        login_url = reverse('accounts:login')
        # GET to set csrftoken cookie
        c.get(login_url)
        token = c.cookies.get('csrftoken').value
        response = c.post(login_url, {'identifier': self.username, 'password': self.password}, HTTP_X_CSRFTOKEN=token)
        # Successful login should redirect (302)
        self.assertIn(response.status_code, (302, 200))

    def test_ajax_newsletter_post_with_csrf(self):
        c = Client(enforce_csrf_checks=True)
        url = reverse('newsletter')
        c.get('/')  # set csrftoken
        token = c.cookies.get('csrftoken').value
        response = c.post(url, {'email': 'qa@example.com'}, HTTP_X_CSRFTOKEN=token, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json())

    def test_ajax_newsletter_post_without_csrf_fails(self):
        c = Client(enforce_csrf_checks=True)
        url = reverse('newsletter')
        response = c.post(url, {'email': 'qa2@example.com'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 403)
