import json

from transactions.models import Transaction
from accounts.models import Operator
from stations.models import Station

import stations.create_station_view_helpers as helpers
import cards.check_card_view_helpers as check_card
from stations import make_bet_view_helpers


def is_user_operator(user):
    operators = Operator.objects.all()
    if operators:
        for operator in operators:
            if user == operator.user:
                return True
    return False


def get_team_won_money(data):
    team = check_card.get_team_by_card(data)
    card = check_card.get_team_card(team)
    team_won_money = 0

    for transaction in Transaction.objects.all():
        if transaction.sender == team.id and not transaction.processed:
            if transaction.victory:
                station = Station.objects.get(id=transaction.recipient)
                team_won_money += transaction.amount * station.complexity
            transaction.processed = True
            transaction.save()

    return team_won_money


def transfer_won_money_to_card(request, data, team_won_money):
    team = check_card.get_team_by_card(data)
    card = check_card.get_team_card(team)
    card.money_amount += team_won_money
    card.save()
    return True
