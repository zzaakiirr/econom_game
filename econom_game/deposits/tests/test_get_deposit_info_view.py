from django.urls import reverse, resolve
from django.test import TestCase
from django.contrib.auth import get_user_model

import json

from accounts.models import Operator
from cards.models import Card
from teams.models import Team
from ..models import Bank, Deposit

from ..views import get_deposit_info


User = get_user_model()


class GetDepositInfoTests(TestCase):
    def test_make_take_deposit_url_resolves_url_deposit_view(self):
        view = resolve('/api/v1/get_deposit_info/')
        self.assertEquals(view.func, get_deposit_info)


class GetDepositInfoTestCase(TestCase):
    def setUp(self):
        self.bank = Bank.objects.create(
            id=1, name='test', deposit=0,
            credit_for_one_year=0, credit_for_two_years=0
        )
        self.card = Card.objects.create(
            id=1, card_number='1', chip_number='1', money_amount=100
        )
        self.team = Team.objects.create(
            id=1, name='test', owner='test', faculty='test',
            group='test', bank=self.bank, card=self.card
        )

        self.url = reverse("get_deposit_info")
        self.data = {
            'card_type': 'card_number', 'card': '1',
        }
        self.expected_data = {
            'team_name': self.team.name,
            'team_owner': self.team.owner,
            'team_money_amount': self.card.money_amount,
            'team_bank': {
                'bank_id': self.bank.id,
                'bank_name': self.bank.name
            },
            'deposit': None,
        }


class NotOperatorAndNotSuperUserGetDepositInfoTests(GetDepositInfoTestCase):
    def setUp(self):
        super().setUp()
        self.response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )

    def test_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_return_correct_data(self):
        expected_data = {
            'success': False,
            'error': 'Недостаточно прав'
        }
        self.assertJSONEqual(self.response.content, expected_data)


class TeamHasDepositGetDepositInfoTests(GetDepositInfoTestCase):
    def setUp(self):
        super().setUp()
        self.deposit = Deposit.objects.create(
            id=1, team=self.team, bank=self.bank, invest_amount=100,
        )
        self.user = User.objects.create(email='test@test', password='test')
        Operator.objects.create(user=self.user, bank=self.bank)
        self.client.force_login(self.user)

        self.response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )

    def test_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_return_correct_data(self):
        self.expected_data['invest_amount'] = {
            'invest_amount': self.deposit.invest_amount,
            'last_change': self.deposit.last_change
        }
        self.assertJSONEqual(self.response.content, self.expected_data)


class TeamHasDepositGetDepositInfoTests(GetDepositInfoTestCase):
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

    def test_return_correct_data(self):
        self.assertJSONEqual(self.response.content, self.expected_data)
