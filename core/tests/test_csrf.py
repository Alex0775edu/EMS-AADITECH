from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model


class CsrfProtectionTests(TestCase):
    def setUp(self):
        self.User = get_user_model()
        # Create a test user with required role
        self.user = self.User.objects.create_user(
            username='testuser', email='test@example.com', password='pass1234', role='STUDENT'
        )

    def _get_csrf_token(self, client, url_name='home'):
        resp = client.get(reverse(url_name))
        return client.cookies.get('csrftoken').value if client.cookies.get('csrftoken') else ''

    def test_login_without_csrf_is_forbidden(self):
        client = Client(enforce_csrf_checks=True)
        login_url = reverse('accounts:login')
        # GET to set cookies
        client.get(login_url)
        # POST without CSRF header should be forbidden
        resp = client.post(login_url, {'identifier': 'testuser', 'password': 'pass1234'})
        self.assertEqual(resp.status_code, 403)

    def test_login_with_csrf_header_succeeds(self):
        client = Client(enforce_csrf_checks=True)
        login_url = reverse('accounts:login')
        client.get(login_url)
        token = client.cookies.get('csrftoken').value
        resp = client.post(
            login_url,
            {'identifier': 'testuser', 'password': 'pass1234'},
            HTTP_X_CSRFTOKEN=token,
        )
        # On success the view redirects to dashboard
        self.assertIn(resp.status_code, (302, 301))
        # Ensure session contains auth id
        self.assertIn('_auth_user_id', client.session)

    def test_newsletter_requires_csrf_header(self):
        client = Client(enforce_csrf_checks=True)
        url = reverse('newsletter')
        # GET home to set cookie
        client.get(reverse('home'))
        # POST without header -> 403
        resp = client.post(url, {'email': 'x@example.com'})
        self.assertEqual(resp.status_code, 403)

        # With header should succeed
        token = client.cookies.get('csrftoken').value
        resp2 = client.post(url, {'email': 'x@example.com'}, HTTP_X_CSRFTOKEN=token)
        self.assertIn(resp2.status_code, (200, 201))
