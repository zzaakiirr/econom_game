from django.test import TestCase
from django.core.urlresolvers import reverse
from django.urls import resolve

from ..models import Bank

from ..views import get_banks_list

from teams.tests import SuperUserTestCase


class GetBanksListTests(TestCase):
    def test_get_banks_list_url_resolves_get_banks_list_view(self):
        view = resolve('/api/v1/get_banks_list/')
        self.assertEquals(view.func, get_banks_list)


class UserNotAllowedGetBanksListTests(TestCase):
    def setUp(self):
        url = reverse("get_banks_list")
        self.response = self.client.get(url)

    def test_user_not_allowed_get_banks_list_view_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_get_banks_list_return_correct_data(self):
        expected_data = {'success': False, 'error': 'Недостаточно прав'}
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)


class SuperUserGetBanksListTests(SuperUserTestCase):
    def setUp(self):
        super().setUp()
        Bank.objects.create(
            id=999, name='test', deposit=0, credit_for_one_year=1,
            credit_for_two_years=2
        )
        url = reverse("get_banks_list")
        self.response = self.client.get(url)

    def test_super_user_get_banks_list_view_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_super_user_get_banks_list_return_correct_data(self):
        expected_data = [
            {
                "id": 999, "name": "test", "deposit": 0,
                "credit_for_one_year": 1, "credit_for_two_years": 2
            }
        ]
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)
