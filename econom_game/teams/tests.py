from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from teams.models import Team, Card
from teams.serializers import TeamSerializer


class BaseViewTest(APITestCase):
    client = APIClient()

    def setUp(self):
        card = Card.objects.create(id=1000, cvv=999, money_amount=999)
        Team.objects.create(id=1000, name="team_1", login="team_1", card=card)


class GetAllTeamsTest(BaseViewTest):

    def test_get_all_teams(self):
        """
        This test ensures that all teams added in the setUp method
        exist when we make a GET request to the api/teams/ endpoint
        """
        response = self.client.get(reverse("teams-all"))
        expected = Team.objects.all()
        serialized = TeamSerializer(expected, many=True)

        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
