from django.core.exceptions import ObjectDoesNotExist
import json

from accounts.models import Operator
from timings.models import Timing
from .models import Bank, Deposit

import stations.create_station_view_helpers as helpers
import cards.check_card_view_helpers as check_card
import credits.take_credit_helpers as take_credit
import stations.make_bet_view_helpers as make_bet
from .get_deposit_info_helpers import get_team_deposit


def get_invest_money_response(request):
    data = json.loads(request.body.decode("utf-8"))

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

    card_error_response = check_card.get_card_error_response(card_type, card)
    if card_error_response.get('error'):
        card_error_response['success'] = False
        return card_error_response

    operator = take_credit.get_operator(request)
    team = check_card.get_team_by_card(card_type, card)
    team_card = check_card.get_team_card(team)

    error_response = get_error_response(team, invest_amount, operator)
    if error_response:
        error_response['success'] = False
        return error_response

    decrease_team_card_money_amount_to_invest_amount(team_card, invest_amount)

    team_deposit = get_team_deposit(team)
    if not team_deposit:
        team_deposit = create_new_deposit(team, invest_amount)
    else:
        team_deposit.invest_amount += invest_amount
        team_deposit.save()

    if not team_deposit._state.db:
        return {
            "success": False,
            "error": "Депозит не был добавлен в базу данных"
        }

    return {"success": True}


def get_error_response(team, invest_amount, operator):
    response = {}

    if not helpers.is_value_positive_integer(invest_amount):
        response['error'] = 'Неверный формат инвестируемой суммы'

    elif not take_credit.is_operator_bank_equal_team_bank(team, operator):
        response['error'] = 'Команда прикреплена к другому банку'

    elif not make_bet.is_enough_money_on_card(team, invest_amount):
        response['error'] = 'Недостаточно средств на карте'

    return response


def decrease_team_card_money_amount_to_invest_amount(team_card, invest_amount):
    team_card.money_amount -= invest_amount
    team_card.save()


def create_new_deposit(team, invest_amount):
    current_half_year = Timing.objects.get(id=1).current_half_year
    new_deposit = Deposit.objects.create(
        team=team,
        bank=team.bank,
        invest_amount=invest_amount,
        half_year=current_half_year
    )
    return new_deposit
