from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

from accounts.models import Financier
from shares.models import ShareType

from shares.views import get_share_info

User = get_user_model()


class GetShareInfoTests(TestCase):
    def test_get_share_info_url_resolves_get_share_info_view(self):
        view = resolve('/api/v1/get_share_info/')
        self.assertEquals(view.func, get_share_info)


class GetShareInfoTestCase(TestCase):
    def setUp(self):
        self.url = reverse("get_share_info")
        self.response = self.client.get(self.url)
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
        self.station = Station.objects.create(
            name='test', owner='test',
            complexity=2.5, min_bet=100, max_bet=200
        )

        user = User.objects.create(email='test@test', password='test')
        Financier.objects.create(user=user)
        self.client.force_login(user)

        self.url = reverse("make_bet")
        self.data = {
            'card_type': 'card_number', 'card': '1', 'bet_amount': 100
        }

    def test_return_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)


class FinancierGetShareInfoTests(GetShareInfoTestCase):
    def setUp(self):
        super().setUp()
        user = User.objects.create(email='test@test', password='test')
        Financier.objects.create(user=user)
        self.client.force_login(user)

        self.response = self.client.get(self.url)

    def test_return_correct_data(self):
        expected_data = {
            'success': True,
            'station': {
                'id': 1,
                'name': self.station.name,
                'owner': self.station.owner,
                'complexity': self.station.complexity,
                'min_bet': self.station.min_bet,
                'max_bet': self.station.max_bet,
            }
        }
        self.assertJSONEqual(self.response.content, expected_data)


# class NotStationAdminGetShareInfoTests(GetShareInfoTestCase):
#     def setUp(self):
#         super().setUp()
#         self.response = self.client.get(self.url)

#     def test_return_correct_data(self):
#         expected_data = {'success': False, 'error': 'Недостаточно прав'}
#         self.assertJSONEqual(self.response.content, expected_data)
