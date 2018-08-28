import json

from transactions.models import Transaction
from accounts.models import StationAdmin

from . import create_station_view_helpers as helpers
import cards.check_card_view_helpers as check_card
import teams.views_helpers as teams_views_helpers
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

    if not check_card.is_valid_card_type(card_type):
        response['error'] = 'Неверный формат типа карты'

    elif not teams_views_helpers.is_value_string_of_positive_integers(card):
        if card_type == 'card_number':
            response['error'] = 'Неверный формат номера карты'
        else:
            response['error'] = 'Неверный формат номера чипа карты'

    elif not check_card.is_card_exist(card_type, card):
        response['error'] = 'Такой карты не существует'

    elif not is_valid_victory_format(victory):
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


def transfer_money_to_card(request, data):
    team = check_card.get_team_by_card(data)
    card = check_card.get_team_card(team)

    station_admin = make_bet_view_helpers.get_station_admin(request)
    station = station_admin.station

    transaction = get_current_transaction(request, data)

    card.money_amount += transaction.amount * station.complexity
    card.save()