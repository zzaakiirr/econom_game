import json

from .models import Deposit

import cards.check_card_view_helpers as check_card


def get_deposit_info(data):
    team = check_card.get_team_by_card(data)
    deposit_info = {
        'team_name': team.name,
        'team_owner': team.owner,
        'team_money_amount': team.card.money_amount,
        'team_bank': {
            'bank_id': team.bank.id,
            'bank_name': team.bank.name,
        },
        'invest_amount': None
    }
    team_deposit = get_team_deposit(team)
    if team_deposit:
        deposit_info['invest_amount'] = team_deposit.invest_amount
    return deposit_info


def get_team_deposit(team):
    for deposit in Deposit.objects.all():
        if deposit.team == team:
            return deposit
    return None
