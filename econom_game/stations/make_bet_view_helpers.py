import json

from accounts.models import StationAdmin
from transactions.models import Transaction

from . import create_station_view_helpers as helpers
import cards.check_card_view_helpers as check_card


def fetch_make_bet_response(request):
    data = json.loads(request.body.decode("utf-8"))

    expected_fields = ('card_type', 'card', 'bet_amount')
    not_received_fields = helpers.get_not_recieved_fields(
        data, expected_fields
    )
    if not_received_fields:
        return helpers.get_not_received_all_expected_fields_error_response(
            not_received_fields)

    card_type = data.get("card_type")
    card = data.get("card")
    bet_amount = data.get("bet_amount")

    card_error_response = check_card.get_card_error_response(card_type, card)
    if card_error_response.get('error'):
        card_error_response['success'] = False
        return card_error_response

    station_admin = get_station_admin(request)
    station = station_admin.station
    team = check_card.get_team_by_card(card_type, card)

    error_response = get_error_response(team, station, bet_amount)
    if error_response:
        error_response['success'] = False
        return error_response

    team_card = check_card.get_team_card(team)
    exclude_bet_amount_from_card(team_card, bet_amount)

    transaction = create_new_transaction(team, station, bet_amount)
    if not transaction._state.db:
        return JsonResponse({
            "success": False,
            "error": "Транзакция не была добавлена в базу данных"
        })

    return {"success": True}


def get_error_response(team, station, bet_amount):
    response = {}

    if not is_team_for_first_time_in_station(team, station):
        response['error'] = 'Команда уже проходила станцию'

    elif not helpers.is_value_positive_integer(bet_amount):
        response['error'] = 'Неверный формат ставки'

    elif not is_valid_bet(bet_amount, station):
        response['error'] = 'Ставка меньше минимальной или больше максимальной'

    elif not is_enough_money_on_card(team, bet_amount):
        response['error'] = 'Недостаточно средств на карте'

    return response


def get_station_admin(request):
    for station_admin in StationAdmin.objects.all():
        if request.user == station_admin.user:
            return station_admin
    return None


def is_valid_bet(bet_amount, station):
    return station.min_bet <= bet_amount <= station.max_bet


def is_enough_money_on_card(team, money_amount):
    if team:
        card = check_card.get_team_card(team)
        if card.money_amount < money_amount:
            return False
    return True


def is_team_for_first_time_in_station(team, station):
    transactions = Transaction.objects.all()
    if transactions and team:
        for transaction in transactions:
            if transaction.sender == team and (
                    transaction.recipient == station):
                return False
    return True


def exclude_bet_amount_from_card(team_card, bet_amount):
    team_card.money_amount -= bet_amount
    team_card.save()
    return True


def create_new_transaction(team, station, bet_amount):
    new_transaction = Transaction.objects.create(
        sender=team,
        recipient=station,
        amount=bet_amount,
        victory=False,
        processed=False
    )
    return new_transaction
