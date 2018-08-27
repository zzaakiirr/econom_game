from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
import json

from accounts.models import StationAdmin
from ..models import Station

from ..views import create_station

from cards.tests.test_create_card_view import SuperUserTestCase


class CreateStationTests(TestCase):
    def test_create_station_url_resolves_create_station_view(self):
        view = resolve('/api/v1/create_station/')
        self.assertEquals(view.func, create_station)


class SuccessfulCreateStationTest(SuperUserTestCase):
    def setUp(self):
        super().setUp()
        url = reverse("create_station")
        self.data = {
            'name': 'test', 'min_bet': 1, 'max_bet': 2, 'complexity': 2.0,
            'email': 'test@test', 'owner': 'test'
        }
        self.response = self.client.post(
            url, json.dumps(self.data), content_type="application/json"
        )
        self.station = Station.objects.get(id=Station.objects.count())
        self.created_user_email = self.data.get('email')

    def test_successul_create_station_view_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_successful_create_station_add_station_to_database(self):
        self.assertTrue(self.station._state.db)

    def test_successful_create_station_add_new_station_admin_to_database(self):
        new_station_admin = get_user_model().objects.get(
            email=self.created_user_email)
        self.assertTrue(new_station_admin._state.db)

    def test_success_add_station_admin_permissions_to_created_user(self):
        station_admin_content_type = ContentType.objects.get_for_model(
            StationAdmin)
        station_admin_permissions = Permission.objects.filter(
            content_type=station_admin_content_type)

        created_user = get_user_model().objects.get(
            email=self.created_user_email)
        created_user_permissions = Permission.objects.filter(user=created_user)

        is_equal_permissions = True
        for created_user_permission in created_user_permissions:
            if created_user_permission not in station_admin_permissions:
                is_equal_permissions = False

        self.assertTrue(is_equal_permissions)

    def test_successful_create_station_return_correct_data(self):
        expected_data = {"success": True}
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)


class InvalidMinBetFormatCreateStationTests(SuperUserTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("create_station")
        data = {
            'name': 'test', 'min_bet': -1, 'max_bet': 2, 'complexity': 2.0,
            'email': 'test@test', 'owner': 'test'
        }
        self.response = self.client.post(
            self.url, json.dumps(data), content_type="application/json"
        )

    def test_success_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_do_not_add_station_to_database(self):
        self.assertEquals(Station.objects.count(), 0)

    def test_do_not_add_station_admin_to_database(self):
        self.assertEquals(StationAdmin.objects.count(), 0)

    def test_return_correct_data(self):
        expected_data = {
            'success': False,
            'error': 'Неверный формат минимальной ставки'
        }
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)


class NotSuperUserCreateStationTests(InvalidMinBetFormatCreateStationTests):
    def setUp(self):
        url = reverse("create_station")
        data = {
            'name': 'test', 'min_bet': 1, 'max_bet': 2, 'complexity': 2.0,
            'email': 'test@test', 'owner': 'test'
        }
        self.response = self.client.post(
            url, json.dumps(data), content_type="application/json"
        )

    def test_return_correct_data(self):
        expected_data = {'success': False, 'error': 'Недостаточно прав'}
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)


class NotGivedOneRequiredFieldCreateStationTests(
        InvalidMinBetFormatCreateStationTests):
    def setUp(self):
        super().setUp()
        data = {
            'min_bet': 1, 'max_bet': 2, 'complexity': 2.0,
            'email': 'test@test', 'owner': 'test'
        }
        self.response = self.client.post(
            self.url, json.dumps(data), content_type="application/json"
        )

    def test_return_correct_data(self):
        expected_data = {'success': False, 'error': 'Поле name пустое'}
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)


class NotGivedManyRequiredFieldsCreateStationTests(
        InvalidMinBetFormatCreateStationTests):
    def setUp(self):
        super().setUp()
        data = {
            'max_bet': 2, 'complexity': 2.0, 'email': 'test@test',
            'owner': 'test'
        }
        self.response = self.client.post(
            self.url, json.dumps(data), content_type="application/json"
        )

    def test_return_correct_data(self):
        expected_data = {
            'success': False, 'error': 'Поля [name, min_bet] пустые'
        }
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)


class NotUniqueNameCreateStationTests(InvalidMinBetFormatCreateStationTests):
    def setUp(self):
        super().setUp()
        self.name = 'test'
        Station.objects.create(
            id=999, name=self.name, owner='test',
            min_bet=1, max_bet=2, complexity=2,
        )
        data = {
            'name': self.name, 'min_bet': 1, 'max_bet': 2,
            'complexity': 2.0, 'email': 'test@test', 'owner': 'test'
        }
        self.response = self.client.post(
            self.url, json.dumps(data), content_type="application/json"
        )

    def test_do_not_add_station_to_database(self):
        self.assertEquals(Station.objects.count(), 1)

    def test_return_correct_data(self):
        expected_data = {
            'success': False,
            'error': 'Станция с именем "%s" уже существует' % self.name
        }
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)


class InvalidComplexityFormatCreateStationTest(
        InvalidMinBetFormatCreateStationTests):
    def setUp(self):
        super().setUp()
        data = {
            'name': 'test', 'min_bet': 1, 'max_bet': 2,
            'complexity': -2.0, 'email': 'test@test', 'owner': 'test'
        }
        self.response = self.client.post(
            self.url, json.dumps(data), content_type="application/json"
        )

    def test_return_correct_data(self):
        expected_data = {
            'success': False,
            'error': 'Неверный формат множителя'
        }
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)


class InvalidMaxBetFormatCreateStationTestCase(
        InvalidMinBetFormatCreateStationTests):
    def setUp(self):
        super().setUp()
        data = {
            'name': 'test', 'min_bet': 1, 'max_bet': -2, 'complexity': 2.0,
            'email': 'test@test', 'owner': 'test'
        }
        self.response = self.client.post(
            self.url, json.dumps(data), content_type="application/json"
        )

    def test_return_correct_data(self):
        expected_data = {
            'success': False,
            'error': 'Неверный формат максимальной ставки'
        }
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)


class MaxBetLessMinBetCreateStationTestCase(
        InvalidMinBetFormatCreateStationTests):
    def setUp(self):
        super().setUp()
        data = {
            'name': 'test', 'min_bet': 3, 'max_bet': 2, 'complexity': 2.0,
            'email': 'test@test', 'owner': 'test'
        }
        self.response = self.client.post(
            self.url, json.dumps(data), content_type="application/json"
        )

    def test_return_correct_data(self):
        expected_data = {
            'success': False,
            'error': "Максимальная ставка меньше минимальной ставки"
        }
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)


class NotUniqueEmailCreateStationTests(InvalidMinBetFormatCreateStationTests):
    def setUp(self):
        super().setUp()
        self.email = 'test@test'
        get_user_model().objects.create(email=self.email, password='test')
        data = {
            'name': 'test', 'min_bet': 1, 'max_bet': 2,
            'complexity': 2.0, 'email': self.email, 'owner': 'test'
        }
        self.response = self.client.post(
            self.url, json.dumps(data), content_type="application/json"
        )

    def test_return_correct_data(self):
        expected_data = {
            'success': False,
            'error': 'email "%s" уже занят' % self.email
        }
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)
