import json

import stations.create_station_view_helpers as helpers
import cards.check_card_view_helpers as check_card


def fetch_transfer_money_response(request, give_money):
    data = json.loads(request.body.decode("utf-8"))

    expected_fields = ("card_type", "card", "money_amount")
    not_received_fields = helpers.get_not_recieved_fields(
        data, expected_fields
    )
    if not_received_fields:
        return helpers.get_not_received_all_expected_fields_error_response(
            not_received_fields)

    card_type = data.get('card_type')
    card = data.get('card')
    money_amount = data.get('money_amount')

    card_error_response = check_card.get_card_error_response(card_type, card)
    if card_error_response:
        card_error_response['success'] = False
        return card_error_response

    error_response = get_error_response(money_amount)
    if error_response:
        error_response['success'] = False
        return error_response

    team = check_card.get_team_by_card(card_type, card)
    team_card = check_card.get_team_card(team)

    if give_money:
        team_card.money_amount += money_amount
    else:
        team_card.money_amount -= money_amount

    team_card.save()
    return {"success": True}


def get_error_response(money_amount):
    response = {}

    if not helpers.is_value_positive_integer(money_amount):
        response['error'] = 'Неверный формат денежной суммы'

    return response
