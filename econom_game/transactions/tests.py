from django.test import TestCase
from django.urls import reverse, resolve

from teams.models import Team, Card
from stations.models import Station
from transactions.models import Transaction

from transactions.views import make_transaction

from transactions.tests_helpers import make_transaction_request_url


class MakeTransasctionTests(TestCase):
    def test_make_transaction_url_resolves_make_transaction_view(self):
        view = resolve('/api/v1/make_transaction/')
        self.assertEquals(view.func, make_transaction)


class MakeTransactionTestCase(TestCase):
    def setUp(self):
        self.card = Card.objects.create(id=999, cvv=999, money_amount=999)
        Team.objects.create(
            id=999, name="team_999",
            login="team_999", card=self.card
        )
        Station.objects.create(
            id=999, name="station_999",
            complexity=2, min_bet=100, max_bet=200
        )
        self.old_transactions_count = Transaction.objects.count()


class MakeTransactionFromStationToTeamTests(MakeTransactionTestCase):
    def setUp(self):
        super().setUp()
        url = make_transaction_request_url(
            sender="station_999",
            recipient="team_999",
            bet_amount=100
        )
        self.response = self.client.get(url)

    def test_send_money_from_station_to_team_view_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_send_money_from_station_to_team_add_transaction_to_database(self):
        new_transactions_count = Transaction.objects.count()
        self.assertEqual(new_transactions_count, self.old_transactions_count+1)


class MakeValidBetAtTheStationTests(MakeTransactionTestCase):
    def setUp(self):
        super().setUp()
        url = make_transaction_request_url(
            sender="team_999",
            recipient="recipient_999",
            bet_amount=100
        )
        self.response = self.client.get(url)

    def test_make_valid_bet_at_the_station_view_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_make_valid_bet_at_the_station_return_correct_data(self):
        response_content = str(self.response.content, encoding='utf8')
        expected_data = {"status": True}
        self.assertJSONEqual(response_content, expected_data)

    def test_make_valid_bet_at_the_statin_add_transaction_to_database(self):
        new_transactions_count = Transaction.objects.count()
        self.assertEqual(new_transactions_count, self.old_transactions_count+1)


class MakeBetWhenNotEnoghMoneyOnTheCardTests(MakeTransactionTestCase):
    def setUp(self):
        super().setUp()
        empty_card = Card.objects.create(id=998, cvv=998, money_amount=0)
        team = Team.objects.create(
            id=998, name="team_998", login="team_998", card=empty_card
        )
        url = make_transaction_request_url(
            sender="team_998",
            recipient="station_999",
            bet_amount=100
        )
        self.old_transactions_count = Transaction.objects.count()
        self.response = self.client.get(url)

    def test_make_bet_when_not_enogh_money_on_the_card_view_success_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_make_bet_when_not_enogh_money_on_the_card_return_correct_data(
            self):
        response_content = str(self.response.content, encoding='utf8')
        expected_data = {
            "status": False,
            "reason": "Your card balance is less than station minimal bet"
        }
        self.assertJSONEqual(response_content, expected_data)

    def test_make_bet_when_no_money_do_not_add_transaction_to_database(self):
        new_transactions_count = Transaction.objects.count()
        self.assertEquals(new_transactions_count, self.old_transactions_count)


class MakeBetLessThanStationMinBetTests(MakeTransactionTestCase):
    def setUp(self):
        super().setUp()
        url = make_transaction_request_url(
            sender="team_999",
            recipient="recipient_999",
            bet_amount=0
        )
        self.response = self.client.get(url)

    def test_make_bet_less_than_station_min_bet_view_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_make_bet_less_than_station_min_bet_return_correct_data(self):
        response_content = str(self.response.content, encoding='utf8')
        expected_data = {
            "status": False,
            "reason": "Station minimal bet is higher"
        }
        self.assertJSONEqual(response_content, expected_data)

    def test_make_bet_less_than_min_bet_do_not_add_transaction_to_database(
            self):
        new_transactions_count = Transaction.objects.count()
        self.assertEquals(new_transactions_count, self.old_transactions_count)


class MakeBetHigherThanStationMaxBetTests(MakeTransactionTestCase):
    def setUp(self):
        super().setUp()
        url = make_transaction_request_url(
            sender="team_999",
            recipient="recipient_999",
            bet_amount=300
        )
        self.response = self.client.get(url)

    def test_make_bet_higher_than_station_max_bet_view_success_status_code(
            self):
        self.assertEquals(self.response.status_code, 200)

    def test_make_bet_higher_than_station_max_bet_return_correct_data(self):
        response_content = str(self.response.content, encoding='utf8')
        expected_data = {
            "status": False,
            "reason": "Your bet is too big"
        }
        self.assertJSONEqual(response_content, expected_data)

    def test_make_bet_higher_than_max_bet_do_not_add_transaction_to_database(
            self):
        new_transactions_count = Transaction.objects.count()
        self.assertEquals(new_transactions_count, self.old_transactions_count)
