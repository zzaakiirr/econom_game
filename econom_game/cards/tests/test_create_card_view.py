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
        data = {'card': '1', 'pay_pass': '1', 'money_amount': 1}
        self.response = self.client.post(
            url, json.dumps(data), content_type="application/json"
        )
        self.card = Card.objects.get(id=Card.objects.count())

    def test_successul_create_card_view_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_successful_create_card_add_card_to_database(self):
        self.assertTrue(self.card._state.db)

    def test_successful_create_card_return_correct_data(self):
        expected_data = {"status": True}
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)


class InvalidCardFormatCreateCardTests(TestCase):
    def setUp(self):
        self.url = reverse("create_card")
        data = {'card': 'invalid_format', 'pay_pass': '1', 'money_amount': 1}
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
            'error': 'Неверный формат карты'
        }
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)


class NotGivedOneRequiredFieldCreateCardTests(
        InvalidCardFormatCreateCardTests):
    def setUp(self):
        super().setUp()
        data = {'pay_pass': '1', 'money_amount': 1}
        self.response = self.client.post(
            self.url, json.dumps(data), content_type="application/json"
        )

    def test_return_correct_data(self):
        expected_data = {'success': False, 'error': 'Поле card пустое'}
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)


class NotGivedManyRequiredFieldsCreateCardTests(
        InvalidCardFormatCreateCardTests):
    def setUp(self):
        super().setUp()
        data = {'money_amount': 1}
        self.response = self.client.post(
            self.url, json.dumps(data), content_type="application/json"
        )

    def test_return_correct_data(self):
        expected_data = {
            'success': False, 'error': 'Поля [card, pay_pass] пустые'
        }
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)


class NotUniqueCardFieldCreateCardTests(InvalidCardFormatCreateCardTests):
    def setUp(self):
        super().setUp()
        self.card = '1'
        Card.objects.create(id=1, card=self.card, pay_pass='1', money_amount=0)
        data = {'card': self.card, 'pay_pass': '1', 'money_amount': 1}

        self.response = self.client.post(
            self.url, json.dumps(data), content_type="application/json"
        )

    def test_do_not_add_card_to_database(self):
        self.assertEquals(Card.objects.count(), 1)

    def test_return_correct_data(self):
        expected_data = {
            'success': False,
            'error': 'Карта уже существует'
        }
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)


class InvalidPayPassFormatCreateCardTest(InvalidCardFormatCreateCardTests):
    def setUp(self):
        super().setUp()
        self.url = reverse("create_card")
        data = {'card': '1', 'pay_pass': 'invalid_format', 'money_amount': 1}
        self.response = self.client.post(
            self.url, json.dumps(data), content_type="application/json"
        )

    def test_return_correct_data(self):
        expected_data = {
            'success': False,
            'error': 'Неверный формат PayPass'
        }
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)


class NotUniquePayPassFieldCreateCardTests(InvalidCardFormatCreateCardTests):
    def setUp(self):
        super().setUp()
        self.pay_pass = '1'
        Card.objects.create(
            id=1, card='1', pay_pass=self.pay_pass, money_amount=0
        )
        data = {'card': '2', 'pay_pass': self.pay_pass, 'money_amount': 1}

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
            'error': 'Картa с PayPass "%s" уже существует' % self.pay_pass
        }
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)
