from django.urls import reverse, resolve
from django.test import TestCase
from django.contrib.auth import get_user_model

import json

from accounts.models import Operator
from cards.models import Card
from teams.models import Team
from ..models import Bank, Credit

from ..views import repay_credit


User = get_user_model()


class RepayCreditTests(TestCase):
    def test_make_repay_credit_url_resolves_url_credit_view(self):
        view = resolve('/api/v1/repay_credit/')
        self.assertEquals(view.func, repay_credit)


class RepayCreditTestCase(TestCase):
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
        self.old_credit = Credit.objects.create(
            id=1, team=self.team, bank=self.bank, term=1,
            debt_amount=100
        )

        self.user = User.objects.create(email='test@test', password='test')
        Operator.objects.create(user=self.user, bank=self.bank)
        self.client.force_login(self.user)

        self.url = reverse("repay_credit")
        self.data = {
            'card_type': 'card_number', 'card': '1',
            'repay_amount': 50
        }


class SuccessfulRepayCreditRepayAmountNotMoreCreditDebtAmountTests(
        RepayCreditTestCase):
    def setUp(self):
        super().setUp()
        self.response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )
        self.changed_card = Card.objects.get(id=self.old_card.id)
        self.changed_credit = Credit.objects.get(id=self.old_credit.id)

    def test_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_credit_amount_decreased_to_repay_amount(self):
        self.assertEquals(
            self.changed_credit.debt_amount,
            self.old_credit.debt_amount - self.data.get('repay_amount')
        )

    def test_card_money_amount_decreased_to_repay_amount(self):
        self.assertEquals(
            self.changed_card.money_amount,
            self.old_card.money_amount - self.data.get('repay_amount')
        )

    def test_return_correct_data(self):
        expected_data = {'success': True}
        self.assertJSONEqual(self.response.content, expected_data)


class SuccessfulRepayCreditRepayAmountMoreCreditDebtAmountTests(
        RepayCreditTestCase):
    def setUp(self):
        super().setUp()
        self.data = {
            'card_type': 'card_number', 'card': '1',
            'repay_amount': 150
        }
        self.response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )
        self.changed_card = Card.objects.get(id=self.old_card.id)
        self.changed_credit = Credit.objects.get(id=self.old_credit.id)

    def test_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_credit_amount_decreased_to_debt_amount(self):
        self.assertEquals(self.changed_credit.debt_amount, 0)

    def test_card_money_amount_decreased_to_debt_amount(self):
        self.assertEqual(
            self.changed_card.money_amount,
            self.old_card.money_amount - self.old_credit.debt_amount
        )

    def test_return_correct_data(self):
        expected_data = {'success': True}
        self.assertJSONEqual(self.response.content, expected_data)


class InvalidRepayAmountFormatRepayCreditTests(RepayCreditTestCase):
    def setUp(self):
        super().setUp()
        self.data = {
            'card_type': 'card_number', 'card': '1',
            'repay_amount': 'invalid_format'
        }

        self.response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )
        self.changed_card = Card.objects.get(id=self.old_card.id)
        self.changed_credit = Credit.objects.get(id=self.old_credit.id)

    def test_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_card_money_amount_not_changed(self):
        self.assertEquals(
            self.changed_card.money_amount,
            self.old_card.money_amount
        )

    def test_credit_debt_amount_not_changed(self):
        self.assertEquals(
            self.old_credit.debt_amount,
            self.changed_credit.debt_amount
        )

    def test_return_correct_data(self):
        expected_data = {
            'success': False,
            'error': 'Неверный формат суммы погашения'
        }
        self.assertJSONEqual(self.response.content, expected_data)


class NotOperatorRepayCreditTests(InvalidRepayAmountFormatRepayCreditTests):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create(email='test_2@test', password='test')
        self.client.force_login(self.user)

        self.data = {
            'card_type': 'card_number', 'card': '1',
            'repay_amount': 50
        }
        self.response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )
        self.changed_card = Card.objects.get(id=self.old_card.id)
        self.changed_credit = Credit.objects.get(id=self.old_credit.id)

    def test_return_correct_data(self):
        expected_data = {'success': False, 'error': 'Недостаточно прав'}
        self.assertJSONEqual(self.response.content, expected_data)


class TeamHasNotCreditRepayCreditTests(TestCase):
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
            'repay_amount': 50
        }
        self.url = reverse('repay_credit')
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
            'error': 'У команды нет кредита'
        }
        self.assertJSONEqual(self.response.content, expected_data)


class CreditBankNotEqualTeamBankRepayCreditTests(
        InvalidRepayAmountFormatRepayCreditTests):
    def setUp(self):
        super().setUp()
        different_bank = Bank.objects.create(
            id=2, name='test_2', deposit=0,
            credit_for_one_year=0, credit_for_two_years=0
        )

        self.data = {
            'card_type': 'card_number', 'card': '1',
            'repay_amount': 50
        }

        self.user = User.objects.create(email='test_2@test', password='test')
        Operator.objects.create(user=self.user, bank=different_bank)
        self.client.force_login(self.user)

        self.response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )
        self.changed_card = Card.objects.get(id=self.old_card.id)
        self.changed_credit = Credit.objects.get(id=self.old_credit.id)

    def test_return_correct_data(self):
        expected_data = {
            'success': False,
            'error': 'Команда прикреплена к другому банку'
        }
        self.assertJSONEqual(self.response.content, expected_data)


class NotEnoughMoneyOnCardRepayCreditTests(
        InvalidRepayAmountFormatRepayCreditTests):
    def setUp(self):
        super().setUp()
        self.old_card.money_amount = 0
        self.old_card.save()

        self.data = {
            'card_type': 'card_number', 'card': '1',
            'repay_amount': 50
        }
        self.response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )
        self.changed_card = Card.objects.get(id=self.old_card.id)
        self.changed_credit = Credit.objects.get(id=self.old_credit.id)

    def test_return_correct_data(self):
        expected_data = {
            'success': False,
            'error': 'Недостаточно средств на карте'
        }
        self.assertJSONEqual(self.response.content, expected_data)
