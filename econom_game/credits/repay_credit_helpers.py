import json

from accounts.models import Operator
from .models import Bank, Credit

import stations.create_station_view_helpers as helpers
from stations import make_bet_view_helpers
import cards.check_card_view_helpers as check_card
from . import take_credit_helpers


def get_received_data(request):
    data = json.loads(request.body.decode("utf-8"))

    operator = take_credit_helpers.get_operator(request)
    error_response = get_error_response(data, operator)
    if error_response:
        error_response['success'] = False
        return error_response

    data['success'] = True
    return data


def get_error_response(data, operator):
    expected_fields = ('card_type', 'card', 'repay_amount')
    not_received_fields = helpers.get_not_recieved_fields(
        data, expected_fields
    )
    if not_received_fields:
        return helpers.get_not_received_all_expected_fields_error_response(
            not_received_fields)

    card_type = data.get("card_type")
    card = data.get("card")
    repay_amount = data.get("repay_amount")

    response = check_card.get_card_error_response(data)
    if response.get('error'):
        return response

    if not get_team_credit(data):
        response['error'] = 'У команды нет кредита'

    if not take_credit_helpers.is_credit_bank_equal_team_bank(data, operator):
        response['error'] = 'Команда прикреплена к другому банку'

    elif not helpers.is_value_positive_integer(repay_amount):
        response['error'] = 'Неверный формат суммы погашения'

    elif not make_bet_view_helpers.is_enough_money_on_card(data, repay_amount):
        response['error'] = 'Недостаточно средств на карте'

    return response


def get_team_credit(data):
    team = check_card.get_team_by_card(data)
    team_credit = Credit.objects.get(team=team)
    return team_credit


def transfer_repay_amount_to_team_credit(data):
    team = check_card.get_team_by_card(data)
    team_card = check_card.get_team_card(team)
    team_credit = get_team_credit(data)
    repay_amount = data.get('repay_amount')

    if repay_amount >= team_credit.debt_amount:
        team_credit.debt_amount = 0
        team_card.money_amount -= team_credit.debt_amount
    else:
        team_credit.debt_amount -= repay_amount
        team_card.money_amount -= repay_amount

    team_credit.save()
    team_card.save()
