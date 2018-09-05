from django.urls import reverse, resolve
from django.test import TestCase
from django.contrib.auth import get_user_model
import json

from accounts.models import StationAdmin
from banks.models import Bank
from teams.models import Team
from cards.models import Card
from transactions.models import Transaction
from ..models import Station

from ..views import make_bet


User = get_user_model()


class MakeBetTests(TestCase):
    def test_make_bet_url_resolves_make_bet_view(self):
        view = resolve('/api/v1/make_bet/')
        self.assertEquals(view.func, make_bet)


class MakeBetTestCase(TestCase):
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
        self.station = Station.objects.create(
            id=1, name='test', owner='test',
            complexity=2.5, min_bet=100, max_bet=200
        )

        user = User.objects.create(email='test@test', password='test')
        StationAdmin.objects.create(user=user, station=self.station)
        self.client.force_login(user)

        self.url = reverse("make_bet")
        self.data = {
            'card_type': 'card_number', 'card': '1', 'bet_amount': 100
        }


class SuccessfulMakeBetTests(MakeBetTestCase):
    def setUp(self):
        super().setUp()
        self.response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )
        self.transaction = Transaction.objects.get(
            sender=self.team, recipient=self.station
        )
        self.changed_card = Card.objects.get(id=self.old_card.id)

    def test_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_bet_amount_excluded_from_card_money_amount(self):
        self.assertEquals(
            self.changed_card.money_amount,
            self.old_card.money_amount - self.data.get('bet_amount')
        )

    def test_add_transaction_to_database(self):
        self.assertTrue(self.transaction._state.db)

    def test_return_correct_data(self):
        expected_data = {"success": True}
        self.assertJSONEqual(self.response.content, expected_data)


class MakeInvalidBetForStationTests(MakeBetTestCase):
    def setUp(self):
        super().setUp()
        data = {
            'card_type': 'card_number',
            'card': '1',
            'bet_amount': 0
        }
        self.response = self.client.post(
            self.url, json.dumps(data), content_type="application/json"
        )
        self.changed_card = Card.objects.get(id=self.old_card.id)

    def test_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_bet_amount_not_excluded_from_card_money_amount(self):
        self.assertEquals(
            self.changed_card.money_amount,
            self.old_card.money_amount
        )

    def test_not_add_transaction_to_database(self):
        self.assertEquals(Transaction.objects.count(), 0)

    def test_return_correct_data(self):
        expected_data = {
            'success': False,
            'error': 'Ставка меньше минимальной или больше максимальной'
        }
        self.assertJSONEqual(self.response.content, expected_data)


class NotStationAdminMakeBetTests(MakeInvalidBetForStationTests):
    def setUp(self):
        super().setUp()
        user = User.objects.create(email='test_2@test', password='test')
        self.client.force_login(user)

        data = {'card_type': 'card_number', 'card': '1', 'bet_amount': 100}
        self.response = self.client.post(
            self.url, json.dumps(data), content_type="application/json"
        )
        self.changed_card = Card.objects.get(id=self.old_card.id)

    def test_return_correct_data(self):
        expected_data = {'success': False, 'error': 'Недостаточно прав'}
        self.assertJSONEqual(self.response.content, expected_data)


class NotGivedOneRequiredFieldMakeBetTests(MakeInvalidBetForStationTests):
    def setUp(self):
        super().setUp()
        data = {'card': '1', 'bet_amount': 0}
        self.response = self.client.post(
            self.url, json.dumps(data), content_type="application/json"
        )
        self.changed_card = Card.objects.get(id=self.old_card.id)

    def test_return_correct_data(self):
        expected_data = {'success': False, 'error': 'Поле card_type пустое'}
        self.assertJSONEqual(self.response.content, expected_data)


class NotGivedManyRequiredFieldsMakeBetTests(MakeInvalidBetForStationTests):
    def setUp(self):
        super().setUp()
        data = {'bet_amount': 0}
        self.response = self.client.post(
            self.url, json.dumps(data), content_type="application/json"
        )
        self.changed_card = Card.objects.get(id=self.old_card.id)

    def test_return_correct_data(self):
        expected_data = {
            'success': False, 'error': 'Поля [card_type, card] пустые'
        }
        self.assertJSONEqual(self.response.content, expected_data)


class MakeBetNotForFirstTimeInStation(MakeBetTestCase):
    def setUp(self):
        super().setUp()
        send_first_time_response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )
        self.response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )
        self.transaction = Transaction.objects.get(
            sender=self.team, recipient=self.station
        )
        self.changed_card = Card.objects.get(id=self.old_card.id)

    def test_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_bet_amount_excluded_from_card_money_amount_only_one_time(self):
        self.assertEquals(
            self.changed_card.money_amount,
            self.old_card.money_amount - self.data.get('bet_amount')
        )

    def test_add_only_one_transaction_to_database(self):
        self.assertTrue(Transaction.objects.count(), 1)

    def test_return_correct_data(self):
        expected_data = {
            'success': False,
            'error': 'Команда уже проходила станцию'
        }
        self.assertJSONEqual(self.response.content, expected_data)


class NotEnoughMoneyOnCardMakeBetTests(MakeInvalidBetForStationTests):
    def setUp(self):
        super().setUp()
        self.old_card.money_amount = 0
        self.old_card.save()

        data = {'card_type': 'card_number', 'card': '1', 'bet_amount': 100}
        self.response = self.client.post(
            self.url, json.dumps(data), content_type="application/json"
        )
        self.changed_card = Card.objects.get(id=self.old_card.id)

    def test_return_correct_data(self):
        expected_data = {
            'success': False,
            'error': 'Недостаточно средств на карте'
        }
        self.assertJSONEqual(self.response.content, expected_data)
