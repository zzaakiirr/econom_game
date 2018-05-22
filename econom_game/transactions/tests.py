from django.test import TestCase
from django.urls import reverse, resolve

from rest_framework.views import status

from teams.models import Team, Card
from stations.models import Station
from transactions.models import Transaction

from transactions.views import make_transaction


def make_transaction_request_url(sender, recipient, bet_amount):
    url = (
        "{reverse_url}?sender={sender}&recipient={recipient}".format(
                reverse_url=reverse("make_transaction"),
                sender=sender,
                recipient=recipient
            ) + "&amount=%s" % str(bet_amount)
    )
    return url


class MakeTransasctionTests(TestCase):
    def test_make_transaction_url_resolves_make_transaction_view(self):
        view = resolve('/api/m=make_transaction/')
        self.assertEquals(view.func, make_transaction)


class MakeTransactionTestCase(TestCase):
    def setUp(self):
        self.card = Card.objects.create(id=999, cvv=999, money_amount=999)
        self.team = Team.objects.create(
            id=999, name="team_999",
            login="team_999", card=self.card
        )
        self.station = Station.objects.create(
            id=999, name="station_999",
            complexity=2, min_bet=100, max_bet=200
        )


class MakeTransactionFromStationToTeamTests(MakeTransactionTestCase):
    def test_send_money_from_station_to_team_view_success_status_code(self):
        url = make_transaction_request_url(
            sender="station_999",
            recipient="recipient_999",
            bet_amount=100
        )
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)


class MakeTransactionFromTeamToStationTests(MakeTransactionTestCase):
    def setUp(self):
        super().setUp()
        self.url = make_transaction_request_url(
            sender="team_999",
            recipient="recipient_999",
            bet_amount=100
        )
        self.response = self.client.get(self.url)
        self.response_content = str(self.response.content, encoding='utf8')

    def test_make_a_valid_bet_at_the_station_view_success_status_code(self):
        self.assertEquals(self.response.status_code, status.HTTP_200_OK)

    def test_make_a_valid_bet_at_the_station_return_correct_data(self):
        expected_data = {"status": True}
        self.assertJSONEqual(self.response_content, expected_data)

    def test_make_a_bet_when_not_enogh_money_on_the_card_view_success_code(
            self):
        self.card.money_amount = 0
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_make_a_bet_when_not_enogh_money_on_the_card_return_correct_data(
            self):

        # Need to FIX:
        card = Card.objects.create(id=998, cvv=998, money_amount=0)
        team = Team.objects.create(
            id=998, name="team_998", login="team_998", card=card
        )
        url = (
            "%s?sender=team_998&recipient=station_999&amount=100" %
            reverse("make_transaction")
        )
        response = self.client.get(url)
        ############################

        response_content = str(response.content, encoding='utf8')
        expected_data = {
            "status": False,
            "reason": "Your card balance is less than station minimal bet"
        }
        self.assertJSONEqual(response_content, expected_data)

    def test_make_a_bet_less_than_station_min_bet_view_success_status_code(
            self):
        url = make_transaction_request_url(
            sender="team_999",
            recipient="recipient_999",
            bet_amount=0
        )
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_make_a_bet_less_than_station_min_bet_return_correct_data(self):
        url = make_transaction_request_url(
            sender="team_999",
            recipient="recipient_999",
            bet_amount=0
        )
        response = self.client.get(url)
        response_content = str(response.content, encoding='utf8')
        expected_data = {
            "status": False,
            "reason": "Station minimal bet is higher"
        }
        self.assertJSONEqual(response_content, expected_data)

    def test_make_a_bet_higher_than_station_max_bet_view_success_status_code(
            self):
        url = make_transaction_request_url(
            sender="team_999",
            recipient="recipient_999",
            bet_amount=300
        )
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_make_a_bet_higher_than_station_max_bet_return_correct_data(self):
        url = make_transaction_request_url(
            sender="team_999",
            recipient="recipient_999",
            bet_amount=300
        )
        response = self.client.get(url)
        response_content = str(response.content, encoding='utf8')
        expected_data = {
            "status": False,
            "reason": "Your bet is too big"
        }
        self.assertJSONEqual(response_content, expected_data)

# class MakeValidBetAtTheStation(MakeTransactionTestCase):
#     def setUp(self):
#         super().setUp()
#         self.url = (
#             "%s?sender=team_999&recipient=station_999&amount=100" %
#             reverse("make_transaction")
#         )
#         self.response = client.get(self.url)
