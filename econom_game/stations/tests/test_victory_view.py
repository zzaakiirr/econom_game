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

from ..views import victory


User = get_user_model()


class VictoryTests(TestCase):
    def test_victory_url_resolves_victory_view(self):
        view = resolve('/api/v1/victory/')
        self.assertEquals(view.func, victory)


class VictoryTestCase(TestCase):
    def setUp(self):
        Bank.objects.create(
            id=1, name='test', deposit=0,
            credit_for_one_year=0, credit_for_two_years=0
        )
        self.old_card = Card.objects.create(
            id=1, card_number='1', chip_number='1', money_amount=100
        )
        team = Team.objects.create(
            id=1, name='test', owner='test', faculty='test',
            group='test', bank=1, card='1', card_type='card_number'
        )
        self.station = Station.objects.create(
            id=1, name='test', owner='test',
            complexity=2.5, min_bet=100, max_bet=200
        )

        self.bet_amount = 100
        self.old_card.money_amount -= self.bet_amount
        self.old_card.save()

        self.old_transaction = Transaction.objects.create(
            id=1,
            sender=team.id,
            recipient=self.station.id,
            amount=self.bet_amount,
            victory=False,
            processed=False
        )
        self.old_transaction.save()

        self.url = reverse("victory")
        self.data = {'card_type': 'card_number', 'card': '1', 'victory': True}


class VictoryTrueTests(VictoryTestCase):
    def setUp(self):
        super().setUp()

        user = User.objects.create(email='test@test', password='test')
        StationAdmin.objects.create(user=user, station=self.station)
        self.client.force_login(user)

        self.response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )

        self.changed_transaction = Transaction.objects.get(id=1)
        self.changed_card = Card.objects.get(id=1)

    def test_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_transaction_victory_field_true(self):
        self.assertTrue(self.changed_transaction.victory)

    def test_transaction_processed_is_false(self):
        self.assertFalse(self.changed_transaction.processed)

    def test_return_correct_data(self):
        expected_data = {"success": True}
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)


class NotStationAdminVictoryTests(VictoryTestCase):
    def setUp(self):
        super().setUp()

        self.response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )

        self.changed_transaction = Transaction.objects.get(id=1)
        self.changed_card = Card.objects.get(id=1)

    def test_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_transaction_victory_field_false(self):
        self.assertFalse(self.changed_transaction.victory)

    def test_transaction_processed_is_false(self):
        self.assertFalse(self.changed_transaction.processed)

    def test_money_not_transfered_to_card(self):
        self.assertNotEquals(
            self.changed_card.money_amount,
            self.old_card.money_amount + (
                self.station.complexity * self.bet_amount
            )
        )

    def test_return_correct_data(self):
        expected_data = {'success': False, 'error': 'Недостаточно прав'}
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)


class VictoryFalseTests(VictoryTestCase):
    def setUp(self):
        super().setUp()

        user = User.objects.create(email='test@test', password='test')
        StationAdmin.objects.create(user=user, station=self.station)
        self.client.force_login(user)

        self.data = {'card_type': 'card_number', 'card': '1', 'victory': False}
        self.response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )
        self.changed_transaction = Transaction.objects.get(id=1)
        self.changed_card = Card.objects.get(id=1)

    def test_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_transaction_victory_field_false(self):
        self.assertFalse(self.changed_transaction.victory)

    def test_transaction_processed_is_true(self):
        self.assertTrue(self.changed_transaction.processed)

    def test_money_not_transfered_to_card(self):
        self.assertEquals(
            self.old_card.money_amount,
            self.changed_card.money_amount
        )

    def test_return_correct_data(self):
        expected_data = {'success': True}
        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)
