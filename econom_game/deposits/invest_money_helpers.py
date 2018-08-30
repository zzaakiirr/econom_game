import json

from accounts.models import Operator
from .models import Bank, Deposit

import stations.create_station_view_helpers as helpers
import cards.check_card_view_helpers as check_card
import credits.take_credit_helpers as take_credit
import stations.make_bet_view_helpers as make_bet


def get_received_data(request):
    data = json.loads(request.body.decode("utf-8"))

    operator = take_credit.get_operator(request)
    error_response = get_error_response(data, operator)
    if error_response:
        error_response['success'] = False
        return error_response

    data['success'] = True
    return data


def get_error_response(data, operator):
    expected_fields = ('card_type', 'card', 'invest_amount')
    not_received_fields = helpers.get_not_recieved_fields(
        data, expected_fields
    )
    if not_received_fields:
        return helpers.get_not_received_all_expected_fields_error_response(
            not_received_fields)

    card_type = data.get("card_type")
    card = data.get("card")
    invest_amount = data.get("invest_amount")

    response = check_card.get_card_error_response(data)
    if response.get('error'):
        return response

    if not helpers.is_value_positive_integer(invest_amount):
        response['error'] = 'Неверный формат инвестируемой суммы'

    elif not take_credit.is_operator_bank_equal_team_bank(data, operator):
        response['error'] = 'Команда прикреплена к другому банку'

    elif not make_bet.is_enough_money_on_card(data, invest_amount):
        response['error'] = 'Недостаточно средств на карте'

    return response


def decrease_team_card_money_amount_to_invest_amount(data):
    team = check_card.get_team_by_card(data)
    card = check_card.get_team_card(team)
    card.money_amount -= data.get('invest_amount')
    card.save()


def create_new_deposit(data):
    team = check_card.get_team_by_card(data)

    new_deposit = Deposit.objects.create(
        team=team,
        bank=team.bank,
        invest_amount=data.get('invest_amount'),
    )

    return new_deposit
