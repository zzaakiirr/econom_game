from django.core.exceptions import ObjectDoesNotExist
import json

from accounts.models import Operator
from .models import Bank, Deposit

import stations.create_station_view_helpers as helpers
from stations import make_bet_view_helpers
import cards.check_card_view_helpers as check_card
from credits import take_credit_helpers


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
    expected_fields = ('card_type', 'card', 'exclude_amount')
    not_received_fields = helpers.get_not_recieved_fields(
        data, expected_fields
    )
    if not_received_fields:
        return helpers.get_not_received_all_expected_fields_error_response(
            not_received_fields)

    card_type = data.get("card_type")
    card = data.get("card")
    exclude_amount = data.get("exclude_amount")

    response = check_card.get_card_error_response(data)
    if response.get('error'):
        return response

    if not get_team_deposit(data):
        response['error'] = 'У команды нет депозита'

    elif not take_credit_helpers.is_operator_bank_equal_team_bank(
            data, operator):
        response['error'] = 'Команда прикреплена к другому банку'

    elif not helpers.is_value_positive_integer(exclude_amount):
        response['error'] = 'Неверный формат снимаемой суммы'

    elif not is_exclude_amount_less_deposit_invest_amount(
            data, exclude_amount):
        response['error'] = 'Снимаемая сумма превышает сумму инвестиций'

    return response


def get_team_deposit(data):
    team = check_card.get_team_by_card(data)
    try:
        team_deposit = Deposit.objects.get(team=team)
    except ObjectDoesNotExist:
        return None
    return team_deposit


def is_exclude_amount_less_deposit_invest_amount(data, exclude_amount):
    team = check_card.get_team_by_card(data)
    team_card = check_card.get_team_card(team)
    team_deposit = get_team_deposit(data)
    return exclude_amount <= team_deposit.invest_amount


def transfer_exclude_amount_to_team_card(data):
    team = check_card.get_team_by_card(data)
    team_card = check_card.get_team_card(team)
    team_deposit = get_team_deposit(data)
    exclude_amount = data.get('exclude_amount')

    team_card.money_amount += exclude_amount
    team_card.save()

    team_deposit.invest_amount -= exclude_amount
    team_deposit.save()
