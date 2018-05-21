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


def is_valid_bet(bet_amount, station):
    if station.min_bet <= bet_amount <= station.max_bet:
        result = {"status": True}
        return True, result

    if bet_amount < station.min_bet:
        result = {
            "status": False,
            "reason": "Station minimal bet is higher"
        }
    elif bet_amount > station.max_bet:
        result = {
            "status": False,
            "reason": "Your bet is too big"
        }

    return False, result


def make_a_bet_at_the_station(sender_id, recipient_id, bet_amount):
    team = Team.objects.get(id=sender_id)
    station = Station.objects.get(id=recipient_id)
    card = team.card

    is_valid_bet_status, result = is_valid_bet(bet_amount, station)
    if (is_valid_bet_status):
        card.money_amount -= bet_amount
        card.save()

    return result


def get_money_from_station(sender_id, recipient_id, bet_amount):
    station = Station.objects.get(id=sender_id)
    team = Teams.objects.get(id=recipient_id)
    card = team.card
    card.money_amount += bet_amount * station.complexity
    card.save()
    result = {"status": True}

    return result


def get_transaction_result(sender, recipient, bet_amount):
    sender_id = get_transaction_participant_id(sender)
    recipient_id = get_transaction_participant_id(recipient)
    if is_team(sender):
        result = make_a_bet_at_the_station(sender_id, recipient_id, bet_amount)
    else:
        result = get_money_from_station(sender_id, recipient_id, bet_amount)

    return result
