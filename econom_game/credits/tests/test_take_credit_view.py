from django.urls import reverse, resolve
from django.test import TestCase
from django.contrib.auth import get_user_model

import json

from accounts.models import Operator
from cards.models import Card
from teams.models import Team
from ..models import Bank, Credit

from ..views import take_credit


User = get_user_model()


class TakeCreditTests(TestCase):
    def test_make_take_credit_url_resolves_url_credit_view(self):
        view = resolve('/api/v1/take_credit/')
        self.assertEquals(view.func, take_credit)


class TakeCreditTestCase(TestCase):
    def setUp(self):
        self.bank = Bank.objects.create(
            id=1, name='test', deposit=0,
            credit_for_one_year=0, credit_for_two_years=0
        )
        self.old_card = Card.objects.create(
            id=1, card_number='1', chip_number='1', money_amount=100
        )
        self.team = Team.objects.create(
            id=1, name='test', owner='test', faculty='test',
            group='test', bank=self.bank, card=self.old_card
        )

        self.url = reverse("take_credit")
        self.data = {
            'card_type': 'card_number', 'card': '1',
            'credit_amount': 50, 'term': 1
        }


class NotOperatorTakeCreditTests(TakeCreditTestCase):
    def setUp(self):
        super().setUp()
        self.response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )
        self.changed_card = Card.objects.get(id=1)

    def test_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_money_not_transfered_to_card(self):
        self.assertNotEquals(
            self.changed_card.money_amount,
            self.old_card.money_amount + self.data.get('credit_amount')
        )

    def test_not_add_credit_to_database(self):
        self.assertEquals(Credit.objects.count(), 0)

    def test_return_correct_data(self):
        expected_data = {'success': False, 'error': 'Недостаточно прав'}
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)


class SuccessfulTakeCreditTests(TakeCreditTestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create(email='test@test', password='test')
        Operator.objects.create(user=self.user, bank=self.bank)
        self.client.force_login(self.user)

        self.response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )

        self.changed_card = Card.objects.get(id=1)

    def test_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_money_transfered_to_card(self):
        self.assertEquals(
            self.changed_card.money_amount,
            self.old_card.money_amount + self.data.get('credit_amount')
        )

    def test_add_credit_to_database(self):
        self.assertEquals(Credit.objects.count(), 1)

    def test_return_correct_data(self):
        expected_data = {"success": True}
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)


class InvalidCreditAmountFormatTakeCreditTests(NotOperatorTakeCreditTests):
    def setUp(self):
        super().setUp()
        self.data = {
            'card_type': 'card_number', 'card': '1',
            'credit_amount': 'invalid_format', 'term': 1
        }

        self.user = User.objects.create(email='test@test', password='test')
        Operator.objects.create(user=self.user, bank=self.bank)
        self.client.force_login(self.user)

        self.response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )
        self.changed_card = Card.objects.get(id=1)

    def test_money_not_transfered_to_card(self):
        self.assertEquals(
            self.changed_card.money_amount,
            self.old_card.money_amount
        )

    def test_return_correct_data(self):
        expected_data = {
            'success': False,
            'error': 'Неверный формат количества денег'
        }
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)


class CreditBankNotEqualTeamBankTakeCreditTests(
        InvalidCreditAmountFormatTakeCreditTests):
    def setUp(self):
        super().setUp()
        different_bank = Bank.objects.create(
            id=2, name='test_2', deposit=0,
            credit_for_one_year=0, credit_for_two_years=0
        )

        self.user = User.objects.create(email='test_2@test', password='test')
        Operator.objects.create(user=self.user, bank=different_bank)
        self.client.force_login(self.user)

        self.data = {
            'card_type': 'card_number', 'card': '1',
            'credit_amount': 30, 'term': 1
        }
        self.response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )

    def test_return_correct_data(self):
        expected_data = {
            'success': False,
            'error': 'Команда прикреплена к другому банку'
        }
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)


class TeamTakeCreditNotForFirstTimeTests(
        InvalidCreditAmountFormatTakeCreditTests):
    def setUp(self):
        super().setUp()
        Credit.objects.create(
            id=1, team=self.team, bank=self.bank, term=1,
            debt_amount=100
        )
        self.data = {
            'card_type': 'card_number', 'card': '1',
            'credit_amount': 30, 'term': 1
        }
        self.response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )

    def test_not_add_credit_to_database(self):
        self.assertEquals(Credit.objects.count(), 1)

    def test_return_correct_data(self):
        expected_data = {
            'success': False,
            'error': 'У команды уже есть кредит'
        }
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)


class CreditAmountMoreHalfCardMoneyAmount(
        InvalidCreditAmountFormatTakeCreditTests):
    def setUp(self):
        super().setUp()
        self.data = {
            'card_type': 'card_number', 'card': '1',
            'credit_amount': self.old_card.money_amount, 'term': 1
        }
        self.response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )

    def test_return_correct_data(self):
        expected_data = {
            'success': False,
            'error': 'Сумма кредита более 50% количества денег на карте'
        }
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)
