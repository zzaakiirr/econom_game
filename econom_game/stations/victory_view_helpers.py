import json

from transactions.models import Transaction
from accounts.models import StationAdmin

from . import create_station_view_helpers as helpers
import cards.check_card_view_helpers as check_card
from stations.make_bet_view_helpers import get_station_admin


def fetch_victory_response(request):
    data = json.loads(request.body.decode("utf-8"))

    expected_fields = ('card_type', 'card', 'victory')
    not_received_fields = helpers.get_not_recieved_fields(
        data, expected_fields
    )
    if not_received_fields:
        return helpers.get_not_received_all_expected_fields_error_response(
            not_received_fields)

    card_type = data.get("card_type")
    card = data.get("card")

    card_error_response = check_card.get_card_error_response(card_type, card)
    if card_error_response.get('error'):
        card_error_response['success'] = False
        return card_error_response

    victory = data.get("victory")

    error_response = get_error_response(victory)
    if error_response:
        error_response['success'] = False
        return error_response

    team = check_card.get_team_by_card(card_type, card)
    station_admin = get_station_admin(request)
    station = station_admin.station
    current_transaction = get_current_transaction(team, station)

    if not victory:
        current_transaction.victory = False
        current_transaction.processed = True
    else:
        current_transaction.victory = True
        current_transaction.processed = False

    current_transaction.save()
    return {"success": True}


def get_error_response(victory):
    response = {}

    if not is_valid_victory_format(victory):
        response['error'] = 'Неверный формат поля победы'

    return response


def is_valid_victory_format(victory):
    return isinstance(victory, bool)


def get_current_transaction(team, station):
    current_transaction = Transaction.objects.get(
        sender=team, recipient=station
    )
    return current_transaction
