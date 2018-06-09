from django.urls import reverse, resolve
from django.test import TestCase, Client

from teams.tests import SuperUserTestCase

from .models import Station
from .serializers import StationSerializer
from .views import ListStationsView, create_station


class BaseViewTest(TestCase):
    def setUp(self):
        Station.objects.create(
            id=999, name="station_999",
            complexity=2, min_bet=100, max_bet=200,
        )
        url = reverse("all_stations")
        self.response = self.client.get(url)


class GetAllStationsTest(BaseViewTest):
    def test_get_all_stations_view_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_get_all_stations_url_resolves_get_all_stations_view(self):
        view = resolve('/api/m=get_all_stations/')
        self.assertEquals(view.func.view_class, ListStationsView)

    def test_get_all_stations_return_correct_data(self):
        expected = Station.objects.all()
        serialized = StationSerializer(expected, many=True)
        self.assertEquals(self.response.data, serialized.data)


class CreateStationTest(SuperUserTestCase):
    def setUp(self):
        super().setUp()
        url = (
            "%s?id=999&name=station_999&complexity=2&min_bet=0&max_bet=999" %
            reverse("create_station")
        )
        self.response = self.client.get(url)
        self.station = Station.objects.get(id=999)

    def test_create_station_view_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_create_station_url_resolves_create_station_view(self):
        view = resolve('/api/m=create_station/')
        self.assertEquals(view.func, create_station)

    def test_create_station_add_station_to_database(self):
        self.assertTrue(self.station._state.db)

    def test_create_station_return_correct_data(self):
        if self.station._state.db:
            expected_data = {"status": True}
        else:
            expected_data = {"status": False}

        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)
