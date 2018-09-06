from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

from accounts.models import StationAdmin
from ..models import Station

from ..views import get_station_info

User = get_user_model()


class MakeBetTests(TestCase):
    def test_get_station_info_url_resolves_get_station_info_view(self):
        view = resolve('/api/v1/get_station_info/')
        self.assertEquals(view.func, get_station_info)


class GetStationInfoTestCase(TestCase):
    def setUp(self):
        self.url = reverse("get_station_info")
        self.response = self.client.get(self.url)


class StationAdminGetStationInfoTests(GetStationInfoTestCase):
    def setUp(self):
        super().setUp()
        self.station = Station.objects.create(
            name='test', owner='test',
            complexity=2.5, min_bet=100, max_bet=200
        )
        user = User.objects.create(email='test@test', password='test')
        StationAdmin.objects.create(user=user, station=self.station)
        self.client.force_login(user)

        self.response = self.client.get(self.url)

    def test_return_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

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


class NotStationAdminGetStationInfoTests(GetStationInfoTestCase):
    def setUp(self):
        super().setUp()
        self.response = self.client.get(self.url)

    def test_return_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_return_correct_data(self):
        expected_data = {'success': False, 'error': 'Недостаточно прав'}
        self.assertJSONEqual(self.response.content, expected_data)
