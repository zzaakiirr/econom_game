import json

from .models import Credit

import cards.check_card_view_helpers as check_card


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
