import json

from accounts.models import Operator
from transactions.models import Transaction

from . import create_station_view_helpers as helpers
import cards.check_card_view_helpers as check_card


def get_received_data(request):
    data = json.loads(request.body.decode("utf-8"))

    operator = get_operator(request)
    error_response = get_error_response(data, operator)
    if error_response:
        error_response['success'] = False
        return error_response

    data['success'] = True
    return data


def get_operator(request):
    for operator in Operator.objects.all():
        if operator.user == request.user:
            return operator
    return None


def get_error_response(data, operator):
    expected_fields = ('card_type', 'card', 'credit_amount', 'term', 'year')
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

    response = check_card.get_card_error_response(data)

    if not helpers.is_value_positive_integer(credit_amount):
        response['error'] = 'Неверный формат количества денег'

    elif not is_operator_bank_equal_team_bank(data, operator):
        response['error'] = 'Команда прикреплена к другому банку'

    elif not is_team_take_credit_for_first_time(data):
        response['error'] = 'У команды уже есть кредит'

    elif not is_credit_amount_less_card_half_money_amount(data, credit_amount):
        response['error'] = 'Сумма кредита более 50% количества денег на карте'

    return response


def is_operator_bank_equal_team_bank(data, operator):
    team = check_card.get_team_by_card(data)
    return team.bank == operator.bank


def is_team_take_credit_for_first_time(data):
    team = check_card.get_team_by_card(data)
    for credit in Credit.objects.all():
        if credit.team == team:
            return False
    return True


def is_credit_amount_less_card_half_credit_amount(data, credit_amount):
    team = check_card.get_team_by_card(data)
    card = check_card.get_team_card(team)
    return credit_amount < card.money_amount / 2


def create_new_credit(data):
    team = check_card.get_team_by_card(data)
    bank = Bank.objects.get(id=team.bank)

    new_credit = Credit.objects.create(
        team=team,
        bank=bank,
        debt_amount=credit_amount,
        term=data.get('term'),
    )

    return new_credit
