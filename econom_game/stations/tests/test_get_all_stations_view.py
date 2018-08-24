from django.test import TestCase
from django.urls import reverse, resolve

from ..models import Station

from ..serializers import StationSerializer

from ..views import ListStationsView


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
        view = resolve('/api/v1/get_all_stations/')
        self.assertEquals(view.func.view_class, ListStationsView)

    def test_get_all_stations_return_correct_data(self):
        expected = Station.objects.all()
        serialized = StationSerializer(expected, many=True)
        self.assertEquals(self.response.data, serialized.data)
