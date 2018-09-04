from django.test import TestCase
from django.contrib.auth import get_user, get_user_model
from django.core.urlresolvers import reverse
from django.urls import resolve

import json

from ..views import logout_user


User = get_user_model()


class LogoutTests(TestCase):
    def setUp(self):
        url = reverse('logout')
        self.response = self.client.get(url)

    def test_logout_url_resolves_logout_view(self):
        view = resolve('/api/v1/logout/')
        self.assertEquals(view.func, logout_user)


class NotLoggedUserLogoutTests(TestCase):
    def setUp(self):
        self.url = reverse('logout')
        self.response = self.client.get(self.url)

    def test_logout_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_user_is_not_authenticated(self):
        user = get_user(self.client)
        assert not user.is_authenticated()

    def test_successful_logout_return_correct_data(self):
        expected_data = {"success": True}
        self.assertJSONEqual(self.response.content, expected_data)


class LoggedUserLogoutTests(NotLoggedUserLogoutTests):
    def setUp(self):
        super().setUp()
        user = User.objects.create(email='test', password='test')
        self.client.force_login(user)
        self.response = self.client.get(self.url)
