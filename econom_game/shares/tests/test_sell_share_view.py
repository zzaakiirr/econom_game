from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

import json

from accounts.models import Financier
from timings.models import Timing
from shares.models import ShareType, ShareRate, ShareDeal
from banks.models import Bank
from cards.models import Card
from teams.models import Team

from shares.views import sell_share


User = get_user_model()


class SellShareTests(TestCase):
    def test_sell_share_url_resolves_sell_share_view(self):
        view = resolve('/api/v1/sell_share/')
        self.assertEquals(view.func, sell_share)


class SellShareTestCase(TestCase):
    def setUp(self):
        Timing.objects.create(game_start_time='18:00:00', current_half_year=1)
        self.bank = Bank.objects.create(
            name='test', deposit=0,
            credit_for_one_year=0, credit_for_two_years=0
        )
        self.old_card = Card.objects.create(
            card_number='1', chip_number='1', money_amount=1000
        )
        self.team = Team.objects.create(
            name='test', owner='test', faculty='test',
            group='test', bank=self.bank, card=self.old_card
        )

        self.share_rate_1 = ShareRate.objects.create(
            buy_price=100.0, sell_price=100.0, half_year=1
        )
        self.share_rate_2 = ShareRate.objects.create(
            buy_price=200.0, sell_price=300.0, half_year=2
        )
        self.share_type = ShareType.objects.create(
            name='share_test', amount=100,
        )
        self.share_type.stock_price.add(self.share_rate_1, self.share_rate_2)
        self.amount_to_sell = 10

        self.old_deal = ShareDeal.objects.create(
            team=self.team, share_type=self.share_type, amount=10
        )

        user = User.objects.create(email='test@test', password='test')
        Financier.objects.create(user=user)
        self.client.force_login(user)

        self.url = reverse("sell_share")
        self.data = {
            'card_type': 'card_number', 'card': self.old_card.card_number,
            'share_type': self.share_type.name, 'amount': self.amount_to_sell
        }


class TeamHasShareTypeSuccessfulSellShareTests(SellShareTestCase):
    def setUp(self):
        super().setUp()
        self.response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )
        self.changed_card = Card.objects.get(id=self.old_card.id)
        self.changed_deal = ShareDeal.objects.get(
            team=self.team, share_type=self.share_type,
        )

    def test_return_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_team_card_money_amount_increased_to_sold_shares_price(self):
        self.assertEquals(
            self.changed_card.money_amount,
            self.old_card.money_amount + (
                self.amount_to_sell * self.share_rate_1.sell_price
            )
        )

    def test_old_deal_share_type_amont_decreased_to_selled_amount(self):
        self.assertEquals(
            self.old_deal.amount - self.amount_to_sell,
            self.changed_deal.amount
        )

    def test_return_correct_data(self):
        expected_data = {'success': True}
        self.assertJSONEqual(self.response.content, expected_data)


class InvalidShareTypeSellShareTests(SellShareTestCase):
    def setUp(self):
        super().setUp()
        self.data['share_type'] = 'invalid_format'
        self.response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )
        self.changed_card = Card.objects.get(id=self.old_card.id)
        self.changed_deal = ShareDeal.objects.get(
            team=self.team, share_type=self.share_type,
        )

    def test_return_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_team_card_money_amount_not_increased_to_sold_shares_price(self):
        self.assertNotEquals(
            self.changed_card.money_amount,
            self.old_card.money_amount + (
                self.amount_to_sell * self.share_rate_1.sell_price
            )
        )

    def test_old_deal_share_type_amont_decreased_to_selled_amount(self):
        self.assertEquals(
            self.old_deal.amount,
            self.changed_deal.amount
        )

    def test_return_correct_data(self):
        expected_data = {
            'success': False,
            'error': 'Такого типа акций нет'
        }
        self.assertJSONEqual(self.response.content, expected_data)


class NotFinancierSellShareTests(InvalidShareTypeSellShareTests):
    def setUp(self):
        super().setUp()
        user = User.objects.create(email='test_2@test', password='test')
        self.client.force_login(user)

        self.data['share_type'] = self.share_type.name
        self.response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )
        self.changed_card = Card.objects.get(id=self.old_card.id)
        self.changed_deal = ShareDeal.objects.get(
            team=self.team, share_type=self.share_type,
        )

    def test_return_correct_data(self):
        expected_data = {'success': False, 'error': 'Недостаточно прав'}
        self.assertJSONEqual(self.response.content, expected_data)


class InvalidShareAmountToSellTests(InvalidShareTypeSellShareTests):
    def setUp(self):
        super().setUp()
        self.data['amount'] = -10

        self.data['share_type'] = self.share_type.name
        self.response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )
        self.changed_card = Card.objects.get(id=self.old_card.id)
        self.changed_deal = ShareDeal.objects.get(
            team=self.team, share_type=self.share_type,
        )

    def test_return_correct_data(self):
        expected_data = {
            'success': False,
            'error': 'Неверный формат количества акций для продажи'
        }
        self.assertJSONEqual(self.response.content, expected_data)


class ShareAmountToSellGreaterTeamShareTypeAmountTests(
        InvalidShareTypeSellShareTests):
    def setUp(self):
        super().setUp()
        self.old_deal.amount = 0
        self.old_deal.save()

        self.data['share_type'] = self.share_type.name
        self.response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )
        self.changed_card = Card.objects.get(id=self.old_card.id)
        self.changed_deal = ShareDeal.objects.get(
            team=self.team, share_type=self.share_type,
        )

    def test_return_correct_data(self):
        expected_data = {
            'success': False,
            'error': 'У команды нет такого количества акций'
        }
        self.assertJSONEqual(self.response.content, expected_data)


class ShareTypeStockPriceIsNoneSellShare(InvalidShareTypeSellShareTests):
    def setUp(self):
        super().setUp()
        for share_rate in self.share_type.stock_price.all():
            share_rate.delete()

        self.data['share_type'] = self.share_type.name
        self.response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )
        self.changed_card = Card.objects.get(id=self.old_card.id)
        self.changed_deal = ShareDeal.objects.get(
            team=self.team, share_type=self.share_type,
        )

    def test_return_correct_data(self):
        expected_data = {
            'success': False,
            'error': 'У акций не заполнены расценки'
        }
        self.assertJSONEqual(self.response.content, expected_data)
