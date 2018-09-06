from django.core.exceptions import ObjectDoesNotExist
import json

from accounts.models import Operator
from .models import Bank, Deposit

import stations.create_station_view_helpers as helpers
from stations import make_bet_view_helpers
import cards.check_card_view_helpers as check_card
from credits import take_credit_helpers


def fetch_exclude_deposit_money_response(request):
    data = json.loads(request.body.decode("utf-8"))

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

    card_error_response = check_card.get_card_error_response(card_type, card)
    if card_error_response.get('error'):
        card_error_response['success'] = False
        return card_error_response

    operator = take_credit_helpers.get_operator(request)
    team = check_card.get_team_by_card(card_type, card)
    team_card = check_card.get_team_card(team)
    team_deposit = get_team_deposit(team)

    error_response = get_error_response(
        team, team_deposit, exclude_amount, operator
    )
    if error_response:
        error_response['success'] = False
        return error_response

    increase_card_money_amount_to_exclude_amount(team_card, exclude_amount)
    decrease_deposit_invest_amount_to_exclude_amount(
        team_deposit, exclude_amount)
    return {"success": True}


def get_error_response(team, team_deposit, exclude_amount, operator):
    response = {}

    if not team_deposit:
        response['error'] = 'У команды нет депозита'

    elif not take_credit_helpers.is_operator_bank_equal_team_bank(
            team, operator):
        response['error'] = 'Команда прикреплена к другому банку'

    elif not helpers.is_value_positive_integer(exclude_amount):
        response['error'] = 'Неверный формат снимаемой суммы'

    elif not is_exclude_amount_less_deposit_invest_amount(
            team_deposit, exclude_amount):
        response['error'] = 'Снимаемая сумма превышает сумму инвестиций'

    return response


def get_team_deposit(team):
    try:
        team_deposit = Deposit.objects.get(team=team)
    except ObjectDoesNotExist:
        return None
    return team_deposit


def is_exclude_amount_less_deposit_invest_amount(team_deposit, exclude_amount):
    return exclude_amount <= team_deposit.invest_amount


def increase_card_money_amount_to_exclude_amount(team_card, exclude_amount):
    team_card.money_amount += exclude_amount
    team_card.save()


def decrease_deposit_invest_amount_to_exclude_amount(
        team_deposit, exclude_amount):
    team_deposit.invest_amount -= exclude_amount
    team_deposit.save()
