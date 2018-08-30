from django.urls import reverse, resolve
from django.test import TestCase
from django.contrib.auth import get_user_model

import json

from accounts.models import Operator
from cards.models import Card
from teams.models import Team
from ..models import Bank, Deposit

from ..views import invest_money


User = get_user_model()


class InvestMoneyTests(TestCase):
    def test_make_invest_money_url_resolves_url_credit_view(self):
        view = resolve('/api/v1/invest_money/')
        self.assertEquals(view.func, invest_money)


class InvestMoneyTestCase(TestCase):
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

        self.url = reverse("invest_money")
        self.data = {
            'card_type': 'card_number', 'card': '1',
            'invest_amount': 50,
        }


class NotOperatorInvestMoneyTests(InvestMoneyTestCase):
    def setUp(self):
        super().setUp()
        self.response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )
        self.changed_card = Card.objects.get(id=1)

    def test_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_money_not_transfered_from_card(self):
        self.assertEquals(
            self.changed_card.money_amount,
            self.old_card.money_amount
        )

    def test_not_add_deposit_to_database(self):
        self.assertEquals(Deposit.objects.count(), 0)

    def test_return_correct_data(self):
        expected_data = {'success': False, 'error': 'Недостаточно прав'}
        self.assertJSONEqual(self.response.content, expected_data)


class SuccessfulInvestMoneyTests(InvestMoneyTestCase):
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

    def test_money_transfered_from_card(self):
        self.assertEquals(
            self.changed_card.money_amount,
            self.old_card.money_amount - self.data.get('invest_amount')
        )

    def test_add_deposit_to_database(self):
        self.assertEquals(Deposit.objects.count(), 1)

    def test_return_correct_data(self):
        expected_data = {"success": True}
        self.assertJSONEqual(self.response.content, expected_data)


class InvalidInvestAmountFormatInvestMoneyTests(NotOperatorInvestMoneyTests):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create(email='test@test', password='test')
        Operator.objects.create(user=self.user, bank=self.bank)
        self.client.force_login(self.user)

        self.data = {
            'card_type': 'card_number', 'card': '1',
            'invest_amount': 'invalid_format',
        }
        self.response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )
        self.changed_card = Card.objects.get(id=1)

    def test_return_correct_data(self):
        expected_data = {
            'success': False,
            'error': 'Неверный формат инвестируемой суммы'
        }
        self.assertJSONEqual(self.response.content, expected_data)


class CreditBankNotEqualTeamBankInvestMoneyTests(
        InvalidInvestAmountFormatInvestMoneyTests):
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
            'invest_amount': 30,
        }
        self.response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )

    def test_return_correct_data(self):
        expected_data = {
            'success': False,
            'error': 'Команда прикреплена к другому банку'
        }
        self.assertJSONEqual(self.response.content, expected_data)


class NotEnoughMoneyOnCardInvestMoneyTests(
        InvalidInvestAmountFormatInvestMoneyTests):
    def setUp(self):
        super().setUp()
        self.data = {
            'card_type': 'card_number', 'card': '1',
            'invest_amount': self.old_card.money_amount + 100,
        }
        self.response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )

    def test_return_correct_data(self):
        expected_data = {
            'success': False,
            'error': 'Недостаточно средств на карте'
        }
        self.assertJSONEqual(self.response.content, expected_data)
