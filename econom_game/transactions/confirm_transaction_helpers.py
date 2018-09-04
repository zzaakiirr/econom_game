from accounts.models import Operator
from stations.models import Station
from transactions.models import Transaction

import json

import cards.check_card_view_helpers as check_card


def fetch_confirm_transaction_response(request):
    check_card_response = check_card.fetch_check_card_response(request)
    if not check_card_response.get('success'):
        return check_card_response

    data = json.loads(request.body.decode("utf-8"))
    card_type = data.get('card_type')
    card = data.get('card')

    team = check_card.get_team_by_card(card_type, card)
    team_card = check_card.get_team_card(team)

    won_money_amount = get_team_won_money(team)
    if not won_money_amount:
        return {
            'success': False,
            'won_money_amount': 0
        }

    transfer_won_money_to_card(team_card, won_money_amount)
    return {
        'success': True,
        'won_money_amount': won_money_amount
    }


def is_user_operator(user):
    operators = Operator.objects.all()
    return user in [operator.user for operator in operators]


def get_team_won_money(team):
    won_money_amount = 0
    team_transactions_with_station = Transaction.objects.filter(
        sender=team, processed=False
    )

    for transaction in team_transactions_with_station:
        if transaction.victory:
            station = transaction.recipient
            won_money_amount += transaction.amount * station.complexity
        transaction.processed = True
        transaction.save()

    return won_money_amount


def transfer_won_money_to_card(team_card, won_money_amount):
    team_card.money_amount += won_money_amount
    team_card.save()
