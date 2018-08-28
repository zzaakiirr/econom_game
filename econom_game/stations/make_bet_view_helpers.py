from django.contrib.auth import get_user_model
import json

from accounts.models import StationAdmin
from transactions.models import Transaction

from . import create_station_view_helpers as helpers
import cards.check_card_view_helpers as check_card
import teams.views_helpers as teams_views_helpers


User = get_user_model()


def get_received_data(request):
    data = json.loads(request.body.decode("utf-8"))

    station_admin = get_station_admin(request)
    station = station_admin.station
    error_response = get_error_response(data, station)
    if error_response:
        error_response['success'] = False
        return error_response

    data['success'] = True
    return data


def get_error_response(data, station):
    expected_fields = ('bet_amount', 'card_type', 'card')
    not_received_fields = helpers.get_not_recieved_fields(
        data, expected_fields
    )
    if not_received_fields:
        return helpers.get_not_received_all_expected_fields_error_response(
            not_received_fields)

    response = {}
    bet_amount = data.get("bet_amount")
    card_type = data.get("card_type")
    card = data.get("card")

    if not check_card.is_valid_card_type(card_type):
        response['error'] = 'Неверный формат типа карты'

    elif not teams_views_helpers.is_value_string_of_positive_integers(card):
        if card_type == 'card_number':
            response['error'] = 'Неверный формат номера карты'
        else:
            response['error'] = 'Неверный формат номера чипа карты'

    elif not helpers.is_value_positive_integer(bet_amount):
        response['error'] = 'Неверный формат ставки'

    elif not check_card.is_card_exist(card_type, card):
        response['error'] = 'Такой карты не существует'

    elif not is_valid_bet(bet_amount, station):
        response['error'] = 'Ставка меньше минимальной или больше максимальной'

    elif not is_enough_money_on_card(data):
        response['error'] = 'Недостаточно средств на карте'

    elif not is_team_for_first_time_in_station(data, station):
        response['error'] = 'Команда уже проходила станцию'

    return response


def get_station_admin(request):
    for station_admin in StationAdmin.objects.all():
        if request.user == station_admin.user:
            return station_admin
    return None


def is_valid_bet(bet_amount, station):
    return station.min_bet <= bet_amount <= station.max_bet


def is_enough_money_on_card(data):
    team = check_card.get_team_by_card(data)
    bet_amount = data.get('bet_amount')
    if team:
        card = check_card.get_team_card(team)
        if card.money_amount < bet_amount:
            return False
    return True


def is_team_for_first_time_in_station(data, station):
    team = check_card.get_team_by_card(data)
    for transaction in Transaction.objects.all():
        if transaction.sender == team.id and (
                transaction.recipient == station.id):
            return False
    return True


def exclude_bet_amount_from_card(data):
    team = check_card.get_team_by_card(data)
    card = check_card.get_team_card(team)
    bet_amount = data.get('bet_amount')
    card.money_amount -= bet_amount
    card.save()
    return True


def create_new_transaction(request, data):
    new_transaction_id = Transaction.objects.count() + 1
    team = check_card.get_team_by_card(data)
    station = get_station_admin(request).station

    new_transaction = Transaction.objects.create(
        id=new_transaction_id,
        sender=team.id,
        recipient=station.id,
        amount=data.get('bet_amount'),
        victory=False,
        processed=False
    )

    return new_transaction
