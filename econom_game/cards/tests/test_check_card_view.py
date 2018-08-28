from django.urls import reverse, resolve
from django.test import TestCase
import json

from banks.models import Bank
from teams.models import Team
from ..models import Card

from ..views import check_card


class CheckCardTests(TestCase):
    def test_create_card_url_resolves_create_card_view(self):
        view = resolve('/api/v1/check_card/')
        self.assertEquals(view.func, check_card)


class SuccessfulCheckCardByCardNumberTests(TestCase):
    def setUp(self):
        Bank.objects.create(
            id=1, name='test', deposit=0,
            credit_for_one_year=0, credit_for_two_years=0
        )
        Card.objects.create(
            id=1, card_number='1234567890', chip_number='2', money_amount=0
        )
        Team.objects.create(
            id=1, name='test', owner='test', faculty='test',
            group='test', bank=1, card='1234567890', card_type='card_number'
        )
        self.url = reverse("check_card")
        data = {'card_type': 'card_number', 'card': '1234567890'}
        self.response = self.client.post(
            self.url, json.dumps(data), content_type="application/json"
        )

    def test_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_return_correct_data(self):
        expected_data = {"success": True, "team_name": "test"}
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)


class SuccessfulCheckCardByChipNumberTests(
        SuccessfulCheckCardByCardNumberTests):
    def setUp(self):
        super().setUp()
        data = {'card_type': 'chip_number', 'card': '2'}
        self.response = self.client.post(
            self.url, json.dumps(data), content_type="application/json"
        )


class InvalidCardTypeFormatCreateCardTests(
        SuccessfulCheckCardByCardNumberTests):
    def setUp(self):
        super().setUp()
        data = {'card_type': 'invalid_format', 'card': '1'}
        self.response = self.client.post(
            self.url, json.dumps(data), content_type="application/json"
        )

    def test_return_correct_data(self):
        expected_data = {
            'success': False,
            'error': 'Неверный формат типа карты'
        }
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)


class InvalidCardNumberFormatCreateCardTests(
        SuccessfulCheckCardByCardNumberTests):
    def setUp(self):
        super().setUp()
        data = {'card_type': 'card_number', 'card': 'invalid_format'}
        self.response = self.client.post(
            self.url, json.dumps(data), content_type="application/json"
        )

    def test_return_correct_data(self):
        expected_data = {
            'success': False,
            'error': 'Неверный формат номера карты'
        }
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)


class InvalidChipNumberFormatCreateCardTests(
        SuccessfulCheckCardByCardNumberTests):
    def setUp(self):
        super().setUp()
        data = {'card_type': 'chip_number', 'card': 'invalid_format'}
        self.response = self.client.post(
            self.url, json.dumps(data), content_type="application/json"
        )

    def test_return_correct_data(self):
        expected_data = {
            'success': False,
            'error': 'Неверный формат номера чипа карты'
        }
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)


class NotGivedOneRequiredFieldCreateCardTests(
        SuccessfulCheckCardByCardNumberTests):
    def setUp(self):
        super().setUp()
        data = {'card': '1'}
        self.response = self.client.post(
            self.url, json.dumps(data), content_type="application/json"
        )

    def test_return_correct_data(self):
        expected_data = {'success': False, 'error': 'Поле card_type пустое'}
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)


class NotGivedManyRequiredFieldsCreateCardTests(
        SuccessfulCheckCardByCardNumberTests):
    def setUp(self):
        super().setUp()
        data = {}
        self.response = self.client.post(
            self.url, json.dumps(data), content_type="application/json"
        )

    def test_return_correct_data(self):
        expected_data = {
            'success': False, 'error': 'Поля [card_type, card] пустые'
        }
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)


class CardDoesNotHaveTeamTests(TestCase):
    def setUp(self):
        Card.objects.create(
            id=1, card_number='1', chip_number='1', money_amount=0
        )
        url = reverse("check_card")
        data = {'card_type': 'card_number', 'card': '1'}
        self.response = self.client.post(
            url, json.dumps(data), content_type="application/json"
        )

    def test_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_return_correct_data(self):
        expected_data = {"success": False, "error": "У этой карты нет команды"}
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)


class CardDoesNotExistTests(TestCase):
    def setUp(self):
        url = reverse("check_card")
        data = {'card_type': 'card_number', 'card': '1'}
        self.response = self.client.post(
            url, json.dumps(data), content_type="application/json"
        )

    def test_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_return_correct_data(self):
        expected_data = {
            "success": False, "error": "Такой карты не существует"
        }
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)
