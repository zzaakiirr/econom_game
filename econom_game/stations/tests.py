from django.urls import reverse, resolve
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

from .models import Station
from .serializers import StationSerializer
from .views import ListStationsView


class BaseViewTest(APITestCase):
    client = APIClient()

    def setUp(self):
        Station.objects.create(
            id=1000, name="station_1",
            complexity=2, min_bet=100, max_bet=200,
        )

        url = reverse("stations-all")
        self.response = self.client.get(url)


class GetAllTeamsTest(BaseViewTest):

    def test_get_all_stations_view_success_status_code(self):
        self.assertEquals(self.response.status_code, status.HTTP_200_OK)

    def test_get_all_stations_url_resolves_get_all_stations_view(self):
        view = resolve('/api/stations/')
        self.assertEquals(view.func.view_class, ListStationsView)

    def test_get_all_stations_return_correct_data(self):
        expected = Station.objects.all()
        serialized = StationSerializer(expected, many=True)
        self.assertEquals(self.response.data, serialized.data)
