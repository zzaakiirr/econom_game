from django.urls import reverse, resolve
from django.contrib.auth.models import User
from django.test import TestCase
import urllib

from .models import Team, Card
from .serializers import TeamSerializer
from .views import ListTeamsView, create_team, create_card


class GetAllTeamsTest(TestCase):
    def setUp(self):
        card = Card.objects.create(id=999, cvv=999, money_amount=999)
        Team.objects.create(id=999, name="team", login="team_999", card=card)
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


class SuperUserTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_superuser(
            username='test',
            password='test',
            email='test'
        )
        self.client.force_login(user)


class CreateTeamTest(SuperUserTestCase):
    def setUp(self):
        super().setUp()
        Card.objects.create(id=999, cvv=999, money_amount=999)
        url = (
            "%s?id=999&name=team_999&login=team_999&card_id=999" %
            reverse("create_team")
        )
        self.response = self.client.get(url)
        self.team = Team.objects.get(id=999)

    def test_create_team_view_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_create_team_url_resolves_create_team_view(self):
        view = resolve('/api/v1/create_team/')
        self.assertEquals(view.func, create_team)

    def test_create_team_add_team_to_database(self):
        self.assertTrue(self.team._state.db)

    def test_create_team_return_correct_data(self):
        if self.team._state.db:
            expected_data = {"status": True}
        else:
            expected_data = {"status": False}

        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)


class CreateCardTest(SuperUserTestCase):
    def setUp(self):
        super().setUp()
        url = (
            "%s?id=999&cvv=999&money_amount=999" %
            reverse("create_card")
        )
        self.response = self.client.get(url)
        self.card = Card.objects.get(id=999)

    def test_create_team_view_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_create_card_url_resolves_create_card_view(self):
        view = resolve('/api/v1/create_card/')
        self.assertEquals(view.func, create_card)

    def test_create_card_add_card_to_database(self):
        self.assertTrue(self.card._state.db)

    def test_create_card_return_correct_data(self):
        if self.card._state.db:
            expected_data = {"status": True}
        else:
            expected_data = {"status": False}

        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)
