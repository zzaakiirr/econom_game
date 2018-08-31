import json

from transactions.models import Transaction
from accounts.models import Operator
from stations.models import Station

import stations.create_station_view_helpers as helpers
import cards.check_card_view_helpers as check_card
from stations import make_bet_view_helpers


def get_confirm_transaction_response(request):
    check_card_response = check_card.get_check_card_response(request)
    if not check_card_response.get('success'):
        return check_card_response

    team = check_card.get_team_by_card(data)
    card = check_card.get_team_card(team)

    won_money_amount = get_team_won_money(team)
    if not won_money_amount:
        return {
            'success': False,
            'won_money_amount': 0
        }

    transfer_won_money_to_card(card, won_money_amount)
    return {
        'success': True,
        'won_money_amount': won_money_amount
    }


def is_user_operator(user):
    operators = Operator.objects.all()
    if operators:
        for operator in operators:
            if user == operator.user:
                return True
    return False


def get_team_won_money(team):
    team_won_money = 0
    for transaction in Transaction.objects.all():
        if transaction.sender == team and not transaction.processed:
            if transaction.victory:
                station = Station.objects.get(id=transaction.recipient.id)
                team_won_money += transaction.amount * station.complexity
            transaction.processed = True
            transaction.save()

    return team_won_money


def transfer_won_money_to_card(card, won_money):
    card.money_amount += won_money
    card.save()
