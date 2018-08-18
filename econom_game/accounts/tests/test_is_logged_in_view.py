import json
from django.test import TestCase
from django.contrib import auth
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.urls import resolve
from django.contrib.auth import authenticate, login

from ..views import is_logged_in


class IsLoggedInTestCase(TestCase):
    def setUp(self):
        self.url = reverse('is_logged_in')
        self.response = self.client.get(self.url)


class IsLoggedInTests(IsLoggedInTestCase):
    def test_login_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_is_logged_in_url_resolves_login_view(self):
        view = resolve('/api/v1/is_logged_in/')
        self.assertEquals(view.func, is_logged_in)


class IsLoggedInTrueTests(IsLoggedInTestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create(username='test', password='test')
        self.client.force_login(self.user)
        self.response = self.client.get(self.url)

    def test_is_logged_in_true_return_correct_data(self):
        expected_data = {'username': 'test'}
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)


class IsLoggedInFalseTests(IsLoggedInTestCase):
    def test_is_logged_in_false_return_correct_data(self):
        expected_data = {'username': None}
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)
