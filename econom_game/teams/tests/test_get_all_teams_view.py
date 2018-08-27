from django.urls import reverse, resolve
from django.test import TestCase

from cards.models import Card
from ..models import Team

from ..serializers import TeamSerializer

from ..views import ListTeamsView


class GetAllTeamsTest(TestCase):
    def setUp(self):
        Card.objects.create(
            id=1, card_number='1', chip_number='1', money_amount=0
        )
        Team.objects.create(
            id=1, name="test", owner="test", faculty="test", group="test",
            bank=1, card="1", card_type='card_number'
        )
        url = reverse("all_teams")
        self.response = self.client.get(url)

    def test_get_all_teams_view_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_get_all_teams_url_resolves_get_all_team_view(self):
        view = resolve('/api/v1/get_all_teams/')
        self.assertEquals(view.func.view_class, ListTeamsView)

    def test_get_all_stations_return_correct_data(self):
        expected = Team.objects.all()
        serialized = TeamSerializer(expected, many=True)
        self.assertEquals(self.response.data, serialized.data)
