from django.urls import reverse, resolve
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

from teams.models import Team, Card
from teams.serializers import TeamSerializer
from teams.views import ListTeamsView


class BaseViewTest(APITestCase):
    client = APIClient()

    def setUp(self):
        card = Card.objects.create(id=1000, cvv=999, money_amount=999)
        Team.objects.create(id=1000, name="team_1", login="team_1", card=card)

        url = reverse("all_teams")
        self.response = self.client.get(url)


class GetAllTeamsTest(BaseViewTest):

    def test_get_all_teams_view_success_status_code(self):
        self.assertEquals(self.response.status_code, status.HTTP_200_OK)

    def test_get_all_teams_url_resolves_get_all_team_view(self):
        view = resolve('/api/m=get_all_teams/')
        self.assertEquals(view.func.view_class, ListTeamsView)

    def test_get_all_stations_return_correct_data(self):
        expected = Team.objects.all()
        serialized = TeamSerializer(expected, many=True)
        self.assertEquals(self.response.data, serialized.data)
