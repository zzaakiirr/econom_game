from django.urls import reverse, resolve
from django.test import TestCase
from django.contrib.auth import get_user_model

import json

from cards.models import Card
from ..models import Team
from banks.models import Bank

from ..views import create_team


User = get_user_model()


class CreateTeamTests(TestCase):
    def test_create_team_url_resolves_create_team_view(self):
        view = resolve('/api/v1/create_team/')
        self.assertEquals(view.func, create_team)


class SuccessfulCreateTeamTest(TestCase):
    def setUp(self):
        Bank.objects.create(
            id=1, name='test', deposit=0,
            credit_for_one_year=0, credit_for_two_years=0
        )
        Card.objects.create(
            id=1, card_number='1', chip_number='1', money_amount=0
        )
        url = reverse("create_team")
        data = {
            'name': 'test', 'owner': 'test', 'faculty': 'test',
            'group': 'test', 'bank': 1, 'card_type': 'chip_number',
            'card': '1'
        }
        self.response = self.client.post(
            url, json.dumps(data), content_type="application/json"
        )
        self.team = Team.objects.get(id=1)

    def test_successul_create_team_view_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_successful_create_team_add_team_to_database(self):
        self.assertTrue(self.team._state.db)

    def test_successful_create_team_return_correct_data(self):
        expected_data = {"success": True}
        self.assertJSONEqual(self.response.content, expected_data)


class InvalidBankFormatCreateTeamTests(TestCase):
    def setUp(self):
        self.url = reverse("create_team")
        self.bank = Bank.objects.create(
            id=1, name='test', deposit=0,
            credit_for_one_year=0, credit_for_two_years=0
        )
        self.card = Card.objects.create(
            id=1, card_number='1', chip_number='1', money_amount=0
        )
        data = {
            'name': 'test', 'owner': 'test', 'faculty': 'test',
            'group': 'test', 'bank': -1, 'card': '1',
            'card_type': 'chip_number'
        }
        self.response = self.client.post(
            self.url, json.dumps(data), content_type="application/json"
        )

    def test_success_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_do_not_add_team_to_database(self):
        self.assertEquals(Team.objects.count(), 0)

    def test_return_correct_data(self):
        expected_data = {
            'success': False,
            'error': 'Неверный формат банка'
        }
        self.assertJSONEqual(self.response.content, expected_data)


class NotGivedOneRequiredFieldCreateTeamTests(
        InvalidBankFormatCreateTeamTests):
    def setUp(self):
        super().setUp()
        data = {
            'owner': 'test', 'faculty': 'test', 'group': 'test',
            'bank': 1, 'card': '1', 'card_type': 'chip_number'
        }
        self.response = self.client.post(
            self.url, json.dumps(data), content_type="application/json"
        )

    def test_return_correct_data(self):
        expected_data = {'success': False, 'error': 'Поле name пустое'}
        self.assertJSONEqual(self.response.content, expected_data)


class NotGivedManyRequiredFieldsCreateTeamTests(
        InvalidBankFormatCreateTeamTests):
    def setUp(self):
        super().setUp()
        data = {
            'faculty': 'test', 'group': 'test',
            'bank': 1, 'card': '1', 'card_type': 'chip_number'
        }
        self.response = self.client.post(
            self.url, json.dumps(data), content_type="application/json"
        )

    def test_return_correct_data(self):
        expected_data = {
            'success': False, 'error': 'Поля [name, owner] пустые'
        }
        self.assertJSONEqual(self.response.content, expected_data)


class NotUniqueNameCreateTeamTests(InvalidBankFormatCreateTeamTests):
    def setUp(self):
        super().setUp()
        self.name = 'test'
        new_card = Card.objects.create(
            id=2, card_number='2', chip_number='2', money_amount=0
        )
        Team.objects.create(
            id=1, name=self.name, owner='test', faculty='test',
            group='test', bank=self.bank, card=self.card
        )
        data = {
            'name': self.name, 'owner': 'test', 'faculty': 'test',
            'group': 'test', 'bank': 1, 'card': new_card.chip_number,
            'card_type': 'chip_number'
        }
        self.response = self.client.post(
            self.url, json.dumps(data), content_type="application/json"
        )

    def test_do_not_add_team_to_database(self):
        self.assertEquals(Team.objects.count(), 1)

    def test_return_correct_data(self):
        expected_data = {
            'success': False,
            'error': 'Команда с именем "%s" уже существует' % self.name
        }
        self.assertJSONEqual(self.response.content, expected_data)


class NotUniqueCardCreateTeamTests(InvalidBankFormatCreateTeamTests):
    def setUp(self):
        super().setUp()
        self.card_id = '1'
        Team.objects.create(
            id=1, name='test', owner='test', faculty='test',
            group='test', bank=self.bank, card=self.card
        )
        data = {
            'name': 'test_2', 'owner': 'test', 'faculty': 'test',
            'group': 'test', 'bank': 1, 'card': self.card_id,
            'card_type': 'chip_number'
        }
        self.response = self.client.post(
            self.url, json.dumps(data), content_type="application/json"
        )

    def test_do_not_add_team_to_database(self):
        self.assertEquals(Team.objects.count(), 1)

    def test_return_correct_data(self):
        expected_data = {
            'success': False,
            'error': 'Команда с такой картой уже существует'
        }
        self.assertJSONEqual(self.response.content, expected_data)


class BankDoesNotExistCreateTeamTests(InvalidBankFormatCreateTeamTests):
    def setUp(self):
        super().setUp()
        data = {
            'name': 'test', 'owner': 'test', 'faculty': 'test',
            'group': 'test', 'bank': 2, 'card': '1',
            'card_type': 'chip_number'
        }
        self.response = self.client.post(
            self.url, json.dumps(data), content_type="application/json"
        )

    def test_return_correct_data(self):
        expected_data = {
            'success': False,
            'error': 'Такого банка не существует'
        }
        self.assertJSONEqual(self.response.content, expected_data)
