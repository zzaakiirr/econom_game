from django.urls import reverse, resolve
from django.test import TestCase
from django.contrib.auth import get_user_model

import json

from accounts.models import Operator
from cards.models import Card
from teams.models import Team
from ..models import Bank, Deposit

from ..views import exclude_deposit_money


User = get_user_model()


class ExcludeMoneyTests(TestCase):
    def test_make_exclude_money_url_resolves_url_deposit_view(self):
        view = resolve('/api/v1/exclude_deposit_money/')
        self.assertEquals(view.func, exclude_deposit_money)


class ExcludeMoneyTestCase(TestCase):
    def setUp(self):
        self.bank = Bank.objects.create(
            id=1, name='test', deposit=0,
            credit_for_one_year=0, credit_for_two_years=0
        )
        self.old_card = Card.objects.create(
            id=1, card_number='1', chip_number='1', money_amount=1000
        )
        self.team = Team.objects.create(
            id=1, name='test', owner='test', faculty='test',
            group='test', bank=self.bank, card=self.old_card
        )
        self.old_deposit = Deposit.objects.create(
            id=1, team=self.team, bank=self.bank, invest_amount=100
        )

        self.user = User.objects.create(email='test@test', password='test')
        Operator.objects.create(user=self.user, bank=self.bank)
        self.client.force_login(self.user)

        self.url = reverse("exclude_deposit_money")
        self.data = {
            'card_type': 'card_number', 'card': '1',
            'exclude_amount': 50
        }


class SuccessfulExcludeMoneyTests(ExcludeMoneyTestCase):
    def setUp(self):
        super().setUp()
        self.response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )
        self.changed_card = Card.objects.get(id=self.old_card.id)
        self.changed_deposit = Deposit.objects.get(id=self.old_deposit.id)

    def test_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_deposit_amount_decreased_to_exclude_amount(self):
        self.assertEquals(
            self.changed_deposit.invest_amount,
            self.old_deposit.invest_amount - self.data.get('exclude_amount')
        )

    def test_card_money_amount_increased_to_exclude_amount(self):
        self.assertEquals(
            self.changed_card.money_amount,
            self.old_card.money_amount + self.data.get('exclude_amount')
        )

    def test_return_correct_data(self):
        expected_data = {'success': True}
        self.assertJSONEqual(self.response.content, expected_data)


class InvalidExcludeAmountFormatExcludeMoneyTests(ExcludeMoneyTestCase):
    def setUp(self):
        super().setUp()
        self.data = {
            'card_type': 'card_number', 'card': '1',
            'exclude_amount': 'invalid_format'
        }

        self.response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )
        self.changed_card = Card.objects.get(id=self.old_card.id)
        self.changed_deposit = Deposit.objects.get(id=self.old_deposit.id)

    def test_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_card_money_amount_not_changed(self):
        self.assertEquals(
            self.changed_card.money_amount,
            self.old_card.money_amount
        )

    def test_deposit_invest_amount_not_changed(self):
        self.assertEquals(
            self.old_deposit.invest_amount,
            self.changed_deposit.invest_amount
        )

    def test_return_correct_data(self):
        expected_data = {
            'success': False,
            'error': 'Неверный формат снимаемой суммы'
        }
        self.assertJSONEqual(self.response.content, expected_data)


class NotOperatorExcludeMoneyTests(
        InvalidExcludeAmountFormatExcludeMoneyTests):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create(email='test_2@test', password='test')
        self.client.force_login(self.user)

        self.data = {
            'card_type': 'card_number', 'card': '1',
            'exclude_amount': 50
        }
        self.response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )
        self.changed_card = Card.objects.get(id=self.old_card.id)
        self.changed_deposit = Deposit.objects.get(id=self.old_deposit.id)

    def test_return_correct_data(self):
        expected_data = {'success': False, 'error': 'Недостаточно прав'}
        self.assertJSONEqual(self.response.content, expected_data)


class TeamHasNotDepositExcludeMoneyTests(TestCase):
    def setUp(self):
        self.bank = Bank.objects.create(
            id=2, name='test_2', deposit=0,
            credit_for_one_year=0, credit_for_two_years=0
        )
        self.old_card = Card.objects.create(
            id=2, card_number='2', chip_number='2', money_amount=100
        )
        self.team = Team.objects.create(
            id=2, name='test_2', owner='test', faculty='test',
            group='test', bank=self.bank, card=self.old_card
        )

        self.user = User.objects.create(email='test@test', password='test')
        Operator.objects.create(user=self.user, bank=self.bank)
        self.client.force_login(self.user)

        self.data = {
            'card_type': 'card_number', 'card': '2',
            'exclude_amount': 50
        }
        self.url = reverse('exclude_deposit_money')
        self.response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )
        self.changed_card = Card.objects.get(id=self.old_card.id)

    def test_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_card_money_amount_not_changed(self):
        self.assertEquals(
            self.changed_card.money_amount,
            self.old_card.money_amount
        )

    def test_return_correct_data(self):
        expected_data = {
            'success': False,
            'error': 'У команды нет депозита'
        }
        self.assertJSONEqual(self.response.content, expected_data)


class DepositBankNotEqualTeamBankExcludeMoneyTests(
        InvalidExcludeAmountFormatExcludeMoneyTests):
    def setUp(self):
        super().setUp()
        different_bank = Bank.objects.create(
            id=2, name='test_2', deposit=0,
            credit_for_one_year=0, credit_for_two_years=0
        )

        self.data = {
            'card_type': 'card_number', 'card': '1',
            'exclude_amount': 50
        }

        self.user = User.objects.create(email='test_2@test', password='test')
        Operator.objects.create(user=self.user, bank=different_bank)
        self.client.force_login(self.user)

        self.response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )
        self.changed_card = Card.objects.get(id=self.old_card.id)
        self.changed_deposit = Deposit.objects.get(id=self.old_deposit.id)

    def test_return_correct_data(self):
        expected_data = {
            'success': False,
            'error': 'Команда прикреплена к другому банку'
        }
        self.assertJSONEqual(self.response.content, expected_data)


class ExcludeAmountMoreDepositInvestAmountMoneyTests(
        InvalidExcludeAmountFormatExcludeMoneyTests):
    def setUp(self):
        super().setUp()
        self.old_card.save()

        self.data = {
            'card_type': 'card_number', 'card': '1',
            'exclude_amount': self.old_deposit.invest_amount + 100
        }
        self.response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )
        self.changed_card = Card.objects.get(id=self.old_card.id)
        self.changed_deposit = Deposit.objects.get(id=self.old_deposit.id)

    def test_return_correct_data(self):
        expected_data = {
            'success': False,
            'error': 'Снимаемая сумма превышает сумму инвестиций'
        }
        self.assertJSONEqual(self.response.content, expected_data)
