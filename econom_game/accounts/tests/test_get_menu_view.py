from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.urls import resolve
import json

from ..views import get_menu
from accounts.models import User, StationAdmin
from stations.views_helpers import add_user_model_permissions_to_user


class GetMenuTests(TestCase):
    def test_get_menu_url_resolves_get_menu_view(self):
        view = resolve('/api/v1/get_menu/')
        self.assertEquals(view.func, get_menu)


class NotLoggedUserGetMenuTests(TestCase):
    def setUp(self):
        self.url = reverse('get_menu')
        self.response = self.client.get(self.url)

    def test_not_logged_user_get_menu_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_not_logged_user_get_menu_return_correct_data(self):
        expected_data = {"user_allowed_urls": []}
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)


class LoggedUserGetMenuTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(email='test', password='test')
        self.url = reverse('get_menu')
        self.response = self.client.get(self.url)
        self.client.force_login(self.user)

    def test_not_logged_user_get_menu_status_code(self):
        self.assertEquals(self.response.status_code, 200)


class StationAdminGetMenuTests(LoggedUserGetMenuTests):
    def setUp(self):
        super().setUp()
        add_user_model_permissions_to_user(self.user, StationAdmin)
        self.response = self.client.get(self.url)

    def test_station_admin_get_menu_return_correct_data(self):
        expected_data = {"user_allowed_urls": ['/admin/station/']}
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)


class SuperUserGetMenuTests(LoggedUserGetMenuTests):
    def setUp(self):
        super().setUp()
        add_user_model_permissions_to_user(self.user, User)
        self.response = self.client.get(self.url)

    def test_super_user_get_menu_return_correct_data(self):
        expected_data = {"user_allowed_urls": ['/admin/add_station/']}
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)
