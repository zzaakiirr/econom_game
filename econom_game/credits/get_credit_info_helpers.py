import json

from .models import Credit

import stations.create_station_view_helpers as helpers
import cards.check_card_view_helpers as check_card


def get_received_data(request):
    data = json.loads(request.body.decode("utf-8"))

    error_response = get_error_response(data)
    if error_response:
        error_response['success'] = False
        return error_response

    data['success'] = True
    return data


def get_error_response(data):
    expected_fields = ('card_type', 'card')
    not_received_fields = helpers.get_not_recieved_fields(
        data, expected_fields
    )
    if not_received_fields:
        return helpers.get_not_received_all_expected_fields_error_response(
            not_received_fields)

    card_type = data.get("card_type")
    card = data.get("card")

    response = check_card.get_card_error_response(data)
    return response


def get_credit_info(data):
    team = check_card.get_team_by_card(data)
    team_credit = get_team_credit(team)
    credit_info = {
        'team_name': team.name,
        'team_owner': team.owner,
        'team_money_amount': team.card.money_amount,
        'team_bank': {
            'bank_id': team.bank.id,
            'bank_name': team.bank.name,
        },
        'team_credit': None
    }
    if team_credit:
        credit_info['team_credit'] = {
            'debt_amount': team_credit.debt_amount,
            'term': team_credit.term,
        }
    return credit_info


def get_team_credit(team):
    for credit in Credit.objects.all():
        if credit.team == team:
            return credit
    return None
