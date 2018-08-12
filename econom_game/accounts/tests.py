import json
from django.test import TestCase
from django.contrib import auth
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.urls import resolve

from .views import login_user


class LoginTests(TestCase):
    def setUp(self):
        url = reverse('login')
        self.response = self.client.get(url)

    def test_login_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_login_url_resolves_login_view(self):
        view = resolve('/login/')
        self.assertEquals(view.func, login_user)


class SuccessfulLoginTests(TestCase):
    def setUp(self):
        User.objects.create_user(username='test', password='test')
        url = reverse('login')
        data = {'username': 'test', 'password': 'test'}
        self.response = self.client.post(
            url, json.dumps(data), content_type="application/json"
        )

    def test_valid_login_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_user_is_authenticated(self):
        user = auth.get_user(self.client)
        assert user.is_authenticated()

    def test_successful_login_return_correct_data(self):
        expected_data = {"success": True}
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)


class InvalidLoginTests(TestCase):
    def setUp(self):
        url = reverse('login')
        data = {'username': 'does_not_exist', 'password': 'does_not_exist'}
        self.response = self.client.post(
            url, json.dumps(data), content_type="application/json"
        )

    def test_invalid_login_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_user_is_not_authenticated(self):
        user = auth.get_user(self.client)
        assert not user.is_authenticated()

    def test_invalid_login_return_correct_data(self):
        expected_data = {"success": False}
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)