from django.urls import reverse, resolve
from django.test import TestCase
from django.contrib.auth import get_user_model
import json

from banks.models import Bank
from teams.models import Team
from cards.models import Card

from ..views import exclude_money


User = get_user_model()


class ExcludeMoneyTests(TestCase):
    def test_exclude_money_url_resolves_exclude_money_view(self):
        view = resolve('/api/v1/exclude_money/')
        self.assertEquals(view.func, exclude_money)


class ExcludeMoneyTestCase(TestCase):
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

        user = User.objects.create_superuser(
            email='test@test', password='test'
        )
        self.client.force_login(user)

        self.url = reverse("exclude_money")
        self.money_amount = 100
        self.data = {
            'card_type': 'card_number', 'card': '1',
            'money_amount': self.money_amount
        }


class InvalidMoneyAmountFormatExcludeMoneyTests(ExcludeMoneyTestCase):
    def setUp(self):
        super().setUp()
        self.data = {
            'card_type': 'card_number', 'card': '1',
            'money_amount': 'invalid_format',
        }
        self.response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )
        self.changed_card = Card.objects.get(id=self.old_card.id)

    def test_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_money_not_transfered_from_team_card(self):
        self.assertEquals(
            self.changed_card.money_amount,
            self.old_card.money_amount
        )

    def test_return_correct_data(self):
        expected_data = {
            'success': False,
            'error': 'Неверный формат денежной суммы'
        }
        self.assertJSONEqual(self.response.content, expected_data)


class NotSuperUserExcludeMoneyTests(InvalidMoneyAmountFormatExcludeMoneyTests):
    def setUp(self):
        super().setUp()
        user = User.objects.create(email='test_2@test', password='test')
        self.client.force_login(user)

        self.data['money_amount'] = 100
        self.response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )
        self.changed_card = Card.objects.get(id=self.old_card.id)

    def test_return_correct_data(self):
        expected_data = {'success': False, 'error': 'Недостаточно прав'}
        self.assertJSONEqual(self.response.content, expected_data)


class SuccessfulExcludeMoneyTests(ExcludeMoneyTestCase):
    def setUp(self):
        super().setUp()
        self.response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )
        self.changed_card = Card.objects.get(id=self.old_card.id)

    def test_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_money_transfered_from_team_card(self):
        self.assertEquals(
            self.changed_card.money_amount,
            self.old_card.money_amount - self.money_amount
        )

    def test_return_correct_data(self):
        expected_data = {'success': True}
        self.assertJSONEqual(self.response.content, expected_data)
