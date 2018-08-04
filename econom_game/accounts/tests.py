from django.test import TestCase
from django.contrib import auth
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.urls import resolve

from .forms import LoginForm
from .views import login_user


class LoginFormTests(TestCase):
    def test_form_has_fields(self):
        form = LoginForm()
        excepted = ['username', 'password']
        actual = list(form.fields)
        self.assertSequenceEqual(excepted, actual)


class LoginTests(TestCase):
    def setUp(self):
        url = reverse('login')
        self.response = self.client.get(url)

    def test_login_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_login_url_resolves_login_view(self):
        view = resolve('/login/')
        self.assertEquals(view.func, login_user)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, LoginForm)


class SuccessfulLoginTests(TestCase):
    def setUp(self):
        User.objects.create_user(username='test', password='test')
        url = reverse('login')
        data = {'username': 'test', 'password': 'test'}
        self.response = self.client.post(url, data)

    def test_invalid_login_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_user_is_authenticated(self):
        user = auth.get_user(self.client)
        assert user.is_authenticated()

    def test_successful_login_return_correct_data(self):
        expected_data = {"status": "success"}
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)


class InvalidLoginTests(TestCase):
    def setUp(self):
        url = reverse('login')
        self.response = self.client.post(
            url, {'username': 'does_not_exist', 'password': 'does_not_exist'}
        )

    def test_invalid_login_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_user_is_not_authenticated(self):
        user = auth.get_user(self.client)
        assert not user.is_authenticated()

    def test_invalid_login_return_correct_data(self):
        expected_data = {"status": "failure"}
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)
