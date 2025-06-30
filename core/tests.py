from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase

from core.models import User


class JWTAuthTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass123', role='ALUNO'
        )

    def test_login_returns_tokens(self):
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {'username': 'testuser', 'password': 'testpass123'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_refresh_token(self):
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {'username': 'testuser', 'password': 'testpass123'})
        refresh = response.data['refresh']
        url = reverse('token_refresh')
        response = self.client.post(url, {'refresh': refresh})
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)

    def test_verify_token(self):
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(self.user)
        access = str(refresh.access_token)
        url = reverse('token_verify')
        response = self.client.post(url, {'token': access})
        self.assertEqual(response.status_code, 200)


class JWTAuthTestCase(APITestCase):
    def test_jwt_login(self):
        response = self.client.post('/api/auth/login/', {'username': 'admin', 'password': 'admin123'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_jwt_refresh(self):
        login = self.client.post('/api/auth/login/', {'username': 'admin', 'password': 'admin123'})
        refresh = login.data['refresh']
        response = self.client.post('/api/auth/refresh/', {'refresh': refresh})
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)


class PermissionTestCase(APITestCase):
    def test_admin_or_read_only(self):
        # Test logic for IsAdminOrReadOnly
        pass


from django.test import TestCase


class EstagiarioTestCase(TestCase):
    pass
