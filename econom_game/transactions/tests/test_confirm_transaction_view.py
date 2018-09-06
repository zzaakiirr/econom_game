from django.urls import reverse, resolve
from django.test import TestCase
from django.contrib.auth import get_user_model
import json

from accounts.models import Operator
from banks.models import Bank
from teams.models import Team
from cards.models import Card
from transactions.models import Transaction
from ..models import Station

from ..views import confirm_transaction


User = get_user_model()


class ConfirmTransactionTests(TestCase):
    def test_confirm_transaction_url_resolves_confirm_transaction_view(self):
        view = resolve('/api/v1/confirm_transaction/')
        self.assertEquals(view.func, confirm_transaction)


class ConfirmTransactionTestCase(TestCase):
    def setUp(self):
        self.bank = Bank.objects.create(
            name='test', deposit=0,
            credit_for_one_year=0, credit_for_two_years=0
        )
        self.old_card = Card.objects.create(
            card_number='1', chip_number='1', money_amount=100
        )
        team = Team.objects.create(
            name='test', owner='test', faculty='test',
            group='test', bank=self.bank, card=self.old_card
        )
        self.station = Station.objects.create(
            name='test', owner='test',
            complexity=2.5, min_bet=100, max_bet=200
        )
        self.old_transaction = Transaction.objects.create(
            sender=team,
            recipient=self.station,
            amount=100,
            victory=True,
            processed=False
        )
        self.old_transaction.save()

        self.url = reverse("confirm_transaction")
        self.data = {'card_type': 'card_number', 'card': '1'}


class TeamHasVictoryTrueTransactionTests(ConfirmTransactionTestCase):
    def setUp(self):
        super().setUp()
        user = User.objects.create(email='test@test', password='test')
        Operator.objects.create(user=user, bank=self.bank)
        self.client.force_login(user)

        self.response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )

        station = self.old_transaction.recipient
        self.won_money_amount = (
            self.old_transaction.amount * station.complexity
        )
        self.changed_transaction = Transaction.objects.get(
            id=self.old_transaction.id
        )
        self.changed_card = Card.objects.get(id=self.old_card.id)

    def test_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_won_money_transfered_to_team_card(self):
        self.assertEquals(
            self.changed_card.money_amount,
            self.old_card.money_amount + self.won_money_amount
        )

    def test_transaction_processed_is_true(self):
        self.assertTrue(self.changed_transaction.processed)

    def test_return_correct_data(self):
        expected_data = {
            "success": True,
            'won_money_amount': self.won_money_amount
        }
        self.assertJSONEqual(self.response.content, expected_data)


class NotOperatorConfirmTransactionTests(ConfirmTransactionTestCase):
    def setUp(self):
        super().setUp()
        self.response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )
        self.changed_transaction = Transaction.objects.get(
            id=self.old_transaction.id
        )
        self.changed_card = Card.objects.get(id=self.old_card.id)

    def test_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_won_money_not_transfered_to_team_card(self):
        self.assertEquals(
            self.changed_card.money_amount,
            self.old_card.money_amount
        )

    def test_transaction_processed_is_false(self):
        self.assertFalse(self.changed_transaction.processed)

    def test_return_correct_data(self):
        expected_data = {'success': False, 'error': 'Недостаточно прав'}
        self.assertJSONEqual(self.response.content, expected_data)


class TeamHasVictoryFalseTransactionTests(ConfirmTransactionTestCase):
    def setUp(self):
        super().setUp()
        self.old_transaction.victory = False
        self.old_transaction.save()

        user = User.objects.create(email='test@test', password='test')
        Operator.objects.create(user=user, bank=self.bank)
        self.client.force_login(user)

        self.response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )
        self.changed_transaction = Transaction.objects.get(
            id=self.old_transaction.id
        )
        self.changed_card = Card.objects.get(id=self.old_card.id)

    def test_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_won_money_not_transfered_to_team_card(self):
        self.assertEquals(
            self.changed_card.money_amount,
            self.old_card.money_amount
        )

    def test_transaction_processed_is_true(self):
        self.assertTrue(self.changed_transaction.processed)

    def test_return_correct_data(self):
        expected_data = {
            "success": False,
            'won_money_amount': 0
        }
        self.assertJSONEqual(self.response.content, expected_data)
