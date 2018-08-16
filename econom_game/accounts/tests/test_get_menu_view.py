from django.contrib.auth import login
from django.test import TestCase
from django.contrib import auth
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import resolve
import json

from ..views import get_menu


class NotLoggedGetMenuTestCase(TestCase):
    def setUp(self):
        self.url = reverse('get_menu')


class LoggedGetMenuTestCase(NotLoggedGetMenuTestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create(username='test', password='test')
        self.client.force_login(self.user)


class NotLoggedUserGetMenuTests(NotLoggedGetMenuTestCase):
    def setUp(self):
        super().setUp()
        self.response = self.client.get(self.url)

    def test_not_logged_user_get_menu_status_code(self):
        self.assertEquals(self.response.status_code, 302)


class LoggedUserHasPermissionToOnePageGetMenuTests(LoggedGetMenuTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.station_admins = Group.objects.create(name="station_admins")

        content_type = ContentType.objects.get(
            app_label='accounts', model='group')
        cls.can_view_station = Permission.objects.create(
            codename='view_station',
            name='Can view "/station" page',
            content_type=content_type
        )

    def setUp(self):
        super().setUp()
        self.station_admins.permissions.add(self.can_view_station)
        self.user.groups.add(self.station_admins)

        self.response = self.client.get(self.url)

    def test_get_menu_url_resolves_get_menu_view(self):
        view = resolve('/api/v1/get_menu/')
        self.assertEquals(view.func, get_menu)

    def test_logged_user_get_menu_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_logged_user_get_menu_return_correct_data(self):
        expected_data = {"success": True, "user_allowed_urls": ['/station/']}
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)


class LoggedUserHasNotPermissionToPageGetMenuTests(LoggedGetMenuTestCase):
    def setUp(self):
        super().setUp()
        self.response = self.client.get(self.url)

    def test_user_has_not_permission_to_page_get_menu_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_user_has_no_permission_to_page_get_menu_return_correct_data(self):
        expected_data = {"success": True, "user_allowed_urls": []}
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)
