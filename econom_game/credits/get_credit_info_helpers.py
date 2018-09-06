import json

from .models import Credit

import cards.check_card_view_helpers as check_card
import stations.create_station_view_helpers as helpers


def fetch_credit_info_response(request):
    data = json.loads(request.body.decode("utf-8"))
    card_type = data.get("card_type")
    card = data.get("card")

    expected_fields = ("card_type", "card")
    not_received_fields = helpers.get_not_recieved_fields(
        data, expected_fields
    )
    if not_received_fields:
        return helpers.get_not_received_all_expected_fields_error_response(
            not_received_fields)

    card_error_response = check_card.get_card_error_response(card_type, card)
    if card_error_response.get('error'):
        card_error_response['success'] = False
        return card_error_response

    credit_info = get_credit_info(card_type, card)
    return credit_info


def get_credit_info(card_type, card):
    team = check_card.get_team_by_card(card_type, card)
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
    team_credit = get_team_credit(team)
    if team_credit:
        credit_info['team_credit'] = {
            'debt_amount': team_credit.debt_amount,
            'term': team_credit.term,
            'last_change': team_credit.last_change
        }
    return credit_info


def get_team_credit(team):
    for credit in Credit.objects.all():
        if credit.team == team:
            return credit
    return None
