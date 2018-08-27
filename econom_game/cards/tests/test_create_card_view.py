from django.urls import reverse, resolve
from django.test import TestCase
from django.contrib.auth import get_user_model
import json

from ..models import Card

from ..views import create_card


User = get_user_model()


class SuperUserTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_superuser(
            email='test',
            password='test',
        )
        self.client.force_login(user)


class CreateCardTests(TestCase):
    def test_create_card_url_resolves_create_card_view(self):
        view = resolve('/api/v1/create_card/')
        self.assertEquals(view.func, create_card)


class SuccessfulCreateCardTest(TestCase):
    def setUp(self):
        url = reverse("create_card")
        data = {'card_number': '1', 'chip_number': '1', 'money_amount': 1}
        self.response = self.client.post(
            url, json.dumps(data), content_type="application/json"
        )
        self.card = Card.objects.get(id=Card.objects.count())

    def test_successul_create_card_view_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_successful_create_card_add_card_to_database(self):
        self.assertTrue(self.card._state.db)

    def test_successful_create_card_return_correct_data(self):
        expected_data = {"success": True}
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)


class InvalidCardNumberFormatCreateCardTests(TestCase):
    def setUp(self):
        self.url = reverse("create_card")
        data = {
            'card_number': 'invalid_format', 'chip_number': '1',
            'money_amount': 1
        }
        self.response = self.client.post(
            self.url, json.dumps(data), content_type="application/json"
        )

    def test_success_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_do_not_add_card_to_database(self):
        self.assertEquals(Card.objects.count(), 0)

    def test_return_correct_data(self):
        expected_data = {
            'success': False,
            'error': 'Неверный формат номера карты'
        }
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)


class NotGivedOneRequiredFieldCreateCardTests(
        InvalidCardNumberFormatCreateCardTests):
    def setUp(self):
        super().setUp()
        data = {'chip_number': '1', 'money_amount': 1}
        self.response = self.client.post(
            self.url, json.dumps(data), content_type="application/json"
        )

    def test_return_correct_data(self):
        expected_data = {'success': False, 'error': 'Поле card_number пустое'}
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)


class NotGivedManyRequiredFieldsCreateCardTests(
        InvalidCardNumberFormatCreateCardTests):
    def setUp(self):
        super().setUp()
        data = {'money_amount': 1}
        self.response = self.client.post(
            self.url, json.dumps(data), content_type="application/json"
        )

    def test_return_correct_data(self):
        expected_data = {
            'success': False, 'error': 'Поля [card_number, chip_number] пустые'
        }
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)


class NotUniqueCardNumberCreateCardTests(
        InvalidCardNumberFormatCreateCardTests):
    def setUp(self):
        super().setUp()
        self.card_number = '1'
        Card.objects.create(
            id=1, card_number=self.card_number, chip_number='1',
            money_amount=0
        )
        data = {
            'card_number': self.card_number, 'chip_number': '1',
            'money_amount': 1
        }
        self.response = self.client.post(
            self.url, json.dumps(data), content_type="application/json"
        )

    def test_do_not_add_card_to_database(self):
        self.assertEquals(Card.objects.count(), 1)

    def test_return_correct_data(self):
        expected_data = {
            'success': False,
            'error': 'Карта с номером %s уже существует' % self.card_number
        }
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)


class InvalidChipNumberFormatCreateCardTest(
        InvalidCardNumberFormatCreateCardTests):
    def setUp(self):
        super().setUp()
        self.url = reverse("create_card")
        data = {
            'card_number': '1', 'chip_number': 'invalid_format',
            'money_amount': 1
        }
        self.response = self.client.post(
            self.url, json.dumps(data), content_type="application/json"
        )

    def test_return_correct_data(self):
        expected_data = {
            'success': False,
            'error': 'Неверный формат номера чипа'
        }
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)


class NotUniqueChipNumberFieldCreateCardTests(
        InvalidCardNumberFormatCreateCardTests):
    def setUp(self):
        super().setUp()
        self.chip_number = '1'
        Card.objects.create(
            id=1, card_number='1', chip_number=self.chip_number,
            money_amount=0
        )
        data = {
            'card_number': '2', 'chip_number': self.chip_number,
            'money_amount': 1
        }
        self.response = self.client.post(
            self.url, json.dumps(data), content_type="application/json"
        )

    def test_(self):
        self.assertEquals(Card.objects.count(), 1)

    def test_do_not_add_card_to_database(self):
        self.assertEquals(Card.objects.count(), 1)

    def test_return_correct_data(self):
        expected_data = {
            'success': False,
            'error': (
                'Картa с номером чипа "%s" уже существует' % self.chip_number
            )
        }
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)


class InvalidMoneyAmountFormatCreateCardTest(
        InvalidCardNumberFormatCreateCardTests):
    def setUp(self):
        super().setUp()
        self.url = reverse("create_card")
        data = {
            'card_number': '1', 'chip_number': '1',
            'money_amount': 'invalid_format'
        }
        self.response = self.client.post(
            self.url, json.dumps(data), content_type="application/json"
        )

    def test_return_correct_data(self):
        expected_data = {
            'success': False,
            'error': 'Неверный формат количества денег'
        }
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)
