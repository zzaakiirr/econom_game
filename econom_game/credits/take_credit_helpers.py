import json

from accounts.models import Operator
from timings.models import Timing
from .models import Bank, Credit

import stations.create_station_view_helpers as helpers
import cards.check_card_view_helpers as check_card
from credits.get_credit_info_helpers import get_team_credit


def get_take_credit_response(request):
    data = json.loads(request.body.decode("utf-8"))

    expected_fields = ('card_type', 'card', 'credit_amount', 'term')
    not_received_fields = helpers.get_not_recieved_fields(
        data, expected_fields
    )
    if not_received_fields:
        return helpers.get_not_received_all_expected_fields_error_response(
            not_received_fields)

    card_type = data.get("card_type")
    card = data.get("card")
    credit_amount = data.get("credit_amount")
    term = data.get("term")

    card_error_response = check_card.get_card_error_response(card_type, card)
    if card_error_response.get('error'):
        card_error_response['success'] = False
        return card_error_response

    operator = get_operator(request)
    team = check_card.get_team_by_card(card_type, card)
    team_card = check_card.get_team_card(team)

    error_response = get_error_response(
        team, team_card,
        credit_amount, term, operator
    )
    if error_response:
        error_response['success'] = False
        return error_response

    transfer_credit_amount_to_team_card(team_card, credit_amount)
    credit = create_new_credit(team, credit_amount, term)
    if not credit._state.db:
        return {
            "success": False,
            "error": "Кредит не был добавлен в базу данных"
        }

    return {"success": True}


def get_operator(request):
    for operator in Operator.objects.all():
        if operator.user == request.user:
            return operator
    return None


def get_error_response(team, team_card, credit_amount, term, operator):
    response = {}
    if not helpers.is_value_positive_integer(credit_amount):
        response['error'] = 'Неверный формат количества денег'

    elif not is_operator_bank_equal_team_bank(team, operator):
        response['error'] = 'Команда прикреплена к другому банку'

    elif get_team_credit(team):
        response['error'] = 'У команды уже есть кредит'

    elif not is_credit_amount_less_card_half_money_amount(
            team_card, credit_amount):
        response['error'] = 'Сумма кредита более 50% количества денег на карте'

    return response


def is_operator_bank_equal_team_bank(team, operator):
    return team.bank == operator.bank


def is_credit_amount_less_card_half_money_amount(team_card, credit_amount):
    return credit_amount <= team_card.money_amount / 2


def transfer_credit_amount_to_team_card(team_card, credit_amount):
    team_card.money_amount += credit_amount
    team_card.save()


def create_new_credit(team, credit_amount, term):
    new_credit = Credit.objects.create(
        team=team,
        bank=team.bank,
        debt_amount=credit_amount,
        term=term,
    )
    return new_credit
