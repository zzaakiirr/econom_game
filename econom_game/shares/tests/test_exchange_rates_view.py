from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

import json

from accounts.models import Financier
from shares.models import ShareType, ShareRate, ShareDeal
from banks.models import Bank
from cards.models import Card
from teams.models import Team

from shares.views import exchange_rates

User = get_user_model()


class ExchangeRatesTests(TestCase):
    def test_exchange_rates_url_resolves_exchange_rates_view(self):
        view = resolve('/api/v1/exchange_rates/')
        self.assertEquals(view.func, exchange_rates)


class ExchangeRatesTestCase(TestCase):
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

        self.share_rate_1 = ShareRate.objects.create(
            sell_price=100.0, buy_price=100.0, half_year=1
        )
        self.share_rate_2 = ShareRate.objects.create(
            sell_price=200.0, buy_price=300.0, half_year=2
        )
        self.share_type = ShareType.objects.create(
            name='share_test', amount=100,
        )
        self.share_type.stock_price.add(self.share_rate_1, self.share_rate_2)
        self.share_deal = ShareDeal.objects.create(
            team=self.team, share_type=self.share_type, amount=1
        )

        self.url = reverse("exchange_rates")
        self.data = {
            'card_type': 'card_number', 'card': self.old_card.card_number
        }


class FinancierExchangeRatesTests(ExchangeRatesTestCase):
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
            '1': [{
                'share_name': self.share_type.name,
                'share_buy': self.share_rate_1.buy_price,
                'share_sell': self.share_rate_1.sell_price
            }],
            '2': [{
                'share_name': self.share_type.name,
                'share_buy': self.share_rate_2.buy_price,
                'share_sell': self.share_rate_2.sell_price
            }],
        }
        self.assertJSONEqual(self.response.content, expected_data)


class NotFinancierExchangeRatesTests(ExchangeRatesTestCase):
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
