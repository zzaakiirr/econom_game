import json

from transactions.models import Transaction
from accounts.models import StationAdmin

from . import create_station_view_helpers as helpers
import cards.check_card_view_helpers as check_card
from . import make_bet_view_helpers


def get_received_data(request):
    data = json.loads(request.body.decode("utf-8"))

    error_response = get_error_response(data)
    if error_response:
        error_response['success'] = False
        return error_response

    data['success'] = True
    return data


def get_error_response(data):
    expected_fields = ('victory', 'card_type', 'card')
    not_received_fields = helpers.get_not_recieved_fields(
        data, expected_fields
    )
    if not_received_fields:
        return helpers.get_not_received_all_expected_fields_error_response(
            not_received_fields)

    response = {}
    victory = data.get("victory")
    card_type = data.get("card_type")
    card = data.get("card")

    response = check_card.get_card_error_response(data)

    if not is_valid_victory_format(victory):
        response['error'] = 'Неверный формат поля победы'

    return response


def is_valid_victory_format(victory):
    return isinstance(victory, bool)


def change_transaction_processed_status(request, data, status):
    current_transaction = get_current_transaction(request, data)
    current_transaction.processed = status
    current_transaction.save()


def change_victory_status(request, data, status):
    current_transaction = get_current_transaction(request, data)
    current_transaction.victory = status
    current_transaction.save()


def get_current_transaction(request, data):
    team = check_card.get_team_by_card(data)
    station = make_bet_view_helpers.get_station_admin(request).station
    current_transaction = Transaction.objects.get(
        sender=team.id, recipient=station.id
    )
    return current_transaction
