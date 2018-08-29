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


class SuccessfulMakeBetTestCase(TestCase):
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


class SuccessfulMakeBetTests(SuccessfulMakeBetTestCase):
    def setUp(self):
        super().setUp()
        self.response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )
        self.transaction = Transaction.objects.get(
            sender=self.team.id, recipient=self.station.id
        )

    def test_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_add_transaction_to_database(self):
        self.assertTrue(self.transaction._state.db)

    def test_return_correct_data(self):
        expected_data = {"success": True}
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)


class NotStationAdminMakeBetTests(TestCase):
    def setUp(self):
        url = reverse("make_bet")
        data = {'card_type': 'card_number', 'card': '1', 'bet_amount': 100}
        self.response = self.client.post(
            url, json.dumps(data), content_type="application/json"
        )

    def test_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_not_add_transaction_to_database(self):
        self.assertEquals(Transaction.objects.count(), 0)

    def test_return_correct_data(self):
        expected_data = {'success': False, 'error': 'Недостаточно прав'}
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)


class NotGivedOneRequiredFieldMakeBetTests(SuccessfulMakeBetTestCase):
    def setUp(self):
        super().setUp()
        data = {'card': '1', 'bet_amount': 0}
        self.response = self.client.post(
            self.url, json.dumps(data), content_type="application/json"
        )

    def test_return_correct_data(self):
        expected_data = {'success': False, 'error': 'Поле card_type пустое'}
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)


class NotGivedManyRequiredFieldsMakeBetTests(SuccessfulMakeBetTestCase):
    def setUp(self):
        super().setUp()
        data = {'bet_amount': 0}
        self.response = self.client.post(
            self.url, json.dumps(data), content_type="application/json"
        )

    def test_return_correct_data(self):
        expected_data = {
            'success': False, 'error': 'Поля [card_type, card] пустые'
        }
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)


class MakeInvalidBetForStationTests(SuccessfulMakeBetTests):
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

    def test_return_correct_data(self):
        expected_data = {
            'success': False,
            'error': 'Ставка меньше минимальной или больше максимальной'
        }
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)


class MakeBetNotForFirstTimeInStation(SuccessfulMakeBetTestCase):
    def setUp(self):
        super().setUp()
        send_first_time_response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )
        self.response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )
        self.transaction = Transaction.objects.get(
            sender=self.team.id, recipient=self.station.id
        )

    def test_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_not_add_transaction_to_database(self):
        self.assertTrue(self.transaction._state.db)

    def test_return_correct_data(self):
        expected_data = {
            'success': False,
            'error': 'Команда уже проходила станцию'
        }
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)
