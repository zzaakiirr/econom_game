from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

import json

from accounts.models import Financier
from shares.models import ShareType, ShareRate, ShareDeal
from banks.models import Bank
from cards.models import Card
from teams.models import Team

from shares.views import share_info

User = get_user_model()


class GetShareInfoTests(TestCase):
    def test_get_share_info_url_resolves_get_share_info_view(self):
        view = resolve('/api/v1/share_info/')
        self.assertEquals(view.func, share_info)


class GetShareInfoTestCase(TestCase):
    def setUp(self):
        self.bank = Bank.objects.create(
            name='test', deposit=0,
            credit_for_one_year=0, credit_for_two_years=0
        )
        self.old_card = Card.objects.create(
            card_number='1', chip_number='1', money_amount=100
        )
        self.team = Team.objects.create(
            name='test', owner='test', faculty='test',
            group='test', bank=self.bank, card=self.old_card
        )

        self.share_rate = ShareRate.objects.create(
            sell_price=100, buy_price=100, half_year=1
        )
        self.share_type = ShareType.objects.create(
            name='share_test', amount=100,
        )
        self.share_type.stock_price.add(self.share_rate)
        self.share_deal = ShareDeal.objects.create(
            team=self.team, share_type=self.share_type, amount=1
        )

        self.url = reverse("share_info")
        self.data = {
            'card_type': 'card_number', 'card': self.old_card.card_number
        }


class FinancierGetShareInfoTests(GetShareInfoTestCase):
    def setUp(self):
        super().setUp()
        user = User.objects.create(email='test@test', password='test')
        Financier.objects.create(user=user)
        self.client.force_login(user)

        self.response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )

    def test_return_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_return_correct_data(self):
        expected_data = {
            'team_name': self.team.name,
            'team_owner': self.team.owner,
            'team_money_amount': self.team.card.money_amount,
            'team_bank': {
                'bank_id': self.team.bank.id,
                'bank_name': self.team.bank.name,
            },
            'team_shares': [
                {
                    'share_name': self.share_type.name,
                    'share_amount': self.share_deal.amount,
                },
            ],
        }
        self.assertJSONEqual(self.response.content, expected_data)


class NotFinancierGetShareInfoTests(GetShareInfoTestCase):
    def setUp(self):
        super().setUp()
        self.response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )

    def test_return_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_return_correct_data(self):
        expected_data = {'success': False, 'error': 'Недостаточно прав'}
        self.assertJSONEqual(self.response.content, expected_data)
