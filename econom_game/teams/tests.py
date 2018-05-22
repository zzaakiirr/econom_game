from django.urls import reverse, resolve
from django.test import TestCase, Client
import urllib

from .models import Team, Card
from .serializers import TeamSerializer
from .views import ListTeamsView, create_team, create_card


class BaseViewTest(TestCase):
    def setUp(self):
        card = Card.objects.create(id=1000, cvv=999, money_amount=999)
        Team.objects.create(id=1000, name="team_1", login="team_1", card=card)

        url = reverse("all_teams")
        self.response = self.client.get(url)


class GetAllTeamsTest(BaseViewTest):
    def test_get_all_teams_view_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_get_all_teams_url_resolves_get_all_team_view(self):
        view = resolve('/api/m=get_all_teams/')
        self.assertEquals(view.func.view_class, ListTeamsView)

    def test_get_all_stations_return_correct_data(self):
        expected = Team.objects.all()
        serialized = TeamSerializer(expected, many=True)
        self.assertEquals(self.response.data, serialized.data)


class CreateTeamTest(TestCase):
    card_create_for_test = Card.objects.create(
        id=999, cvv=990, money_amount=999)
    client = Client()
    client.login(username='admin', password='password123')
    url = (
        "%s?id=898&name=team_999&login=team_997&card_id=999" %
        reverse("create_team")
    )
    response = client.get(url)

    def test_create_team_view_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_create_team_url_resolves_create_team_view(self):
        view = resolve('/api/m=create_team/')
        self.assertEquals(view.func, create_team)

    card_create_for_test.delete()


class CreateCardTest(TestCase):
    client = Client()
    client.login(username='admin', password='password123')
    url = (
        "%s?id=999&cvv=999&money_amount=999" %
        reverse("create_card")
    )
    response = client.get(url)

    def test_create_team_view_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_create_card_url_resolves_create_card_view(self):
        view = resolve('/api/m=create_card/')
        self.assertEquals(view.func, create_card)

    card_created_for_test = Card.objects.get(id=999)
    card_created_for_test.delete()
