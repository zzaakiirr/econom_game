from django.core.exceptions import ObjectDoesNotExist
import json

from accounts.models import Operator
from .models import Bank, Credit

import stations.create_station_view_helpers as helpers
from stations import make_bet_view_helpers
import cards.check_card_view_helpers as check_card
from . import take_credit_helpers


def fetch_repay_credit_response(request):
    data = json.loads(request.body.decode("utf-8"))

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

    card_error_response = check_card.get_card_error_response(card_type, card)
    if card_error_response.get('error'):
        card_error_response['success'] = False
        return response

    operator = take_credit_helpers.get_operator(request)
    team = check_card.get_team_by_card(card_type, card)
    team_card = check_card.get_team_card(team)
    team_credit = get_team_credit(team)

    error_response = get_error_response(
        team, team_card, team_credit, repay_amount, operator
    )
    if error_response:
        error_response['success'] = False
        return error_response

    transfer_repay_amount_to_team_credit(team_card, team_credit, repay_amount)
    return {"success": True}


def get_error_response(team, team_card, team_credit, repay_amount, operator):
    response = {}
    if not team_credit:
        response['error'] = 'У команды нет кредита'

    if not take_credit_helpers.is_operator_bank_equal_team_bank(
            team, operator):
        response['error'] = 'Команда прикреплена к другому банку'

    elif not helpers.is_value_positive_integer(repay_amount):
        response['error'] = 'Неверный формат суммы погашения'

    elif not make_bet_view_helpers.is_enough_money_on_card(
            team, repay_amount):
        response['error'] = 'Недостаточно средств на карте'

    return response


def get_team_credit(team):
    try:
        team_credit = Credit.objects.get(team=team)
    except ObjectDoesNotExist:
        return None
    return team_credit


def transfer_repay_amount_to_team_credit(team_card, team_credit, repay_amount):
    if repay_amount >= team_credit.debt_amount:
        team_card.money_amount -= team_credit.debt_amount
        team_credit.debt_amount = 0
    else:
        team_credit.debt_amount -= repay_amount
        team_card.money_amount -= repay_amount
    team_credit.save()
    team_card.save()
