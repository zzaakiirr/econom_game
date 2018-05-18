from django.shortcuts import render
from django.http import JsonResponse

from stations.models import Station
from teams.models import Team


def get_transaction_participant_id(transaction_participant):
    slash_symbol = transaction_participant.find('_')
    first_digit_of_id = slash_symbol + 1
    transaction_participant_id = transaction_participant[first_digit_of_id:]
    return int(transaction_participant_id)


def is_team(transaction_participant):
    if 'team' in transaction_participant:
        return True
    return False


def get_transaction_result(sender, recipient, bet_amount):
    sender_id = get_transaction_participant_id(sender)
    recipient_id = get_transaction_participant_id(recipient)

    if is_team(sender):
        sender_team = Team.objects.get(id=sender_id)
        recipient_station = Station.objects.get(id=recipient_id)
        team_card = sender_team.card

        if bet_amount < recipient_station.min_bet:
            result = {
                "status": False,
                "reason": "Station minimal bet is higher"
            }
            return result
        elif bet_amount > recipient_station.max_bet:
            result = {
                "status": False,
                "reason": "Team bet for this station is too big"
            }
            return result

        team_card.money_amount -= bet_amount
        team_card.save()
        result = {"status": True}
        return result
    else:
        sender_station = Station.objects.get(id=sender_id)
        recipient_team = Teams.objects.get(id=recipient_id)
        team_card = recipient_team.card
        team_card.money_amount += amount * sender.complexity
        team_card.save()
        result = {"status": True}
        return result


def make_transaction(request):
    sender = request.GET['sender']
    recipient = request.GET['recipient']
    amount = int(request.GET['amount'])

    transaction_result = get_transaction_result(sender, recipient, amount)
    return JsonResponse(transaction_result)
