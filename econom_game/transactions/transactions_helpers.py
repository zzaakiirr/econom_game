from stations.models import Station
from teams.models import Team
from transactions.models import Transaction


def get_transaction_participant_id(transaction_participant):
    slash_symbol_index = transaction_participant.find('_')
    first_digit_of_id = slash_symbol_index + 1
    transaction_participant_id = transaction_participant[first_digit_of_id:]
    return int(transaction_participant_id)


def is_team(transaction_participant):
    if 'team' in transaction_participant:
        return True
    return False


def is_valid_bet(bet_amount, station):
    if station.min_bet <= bet_amount <= station.max_bet:
        return True
    return False


def is_enough_money_on_the_card(station, card):
    if card.money_amount >= station.min_bet:
        return True


def make_a_bet_at_the_station(sender_id, recipient_id, bet_amount):
    team = Team.objects.get(id=sender_id)
    station = Station.objects.get(id=recipient_id)
    card = team.card

    if not is_enough_money_on_the_card(station, card):
        result = {
            "status": False,
            "reason": "Your card balance is less than station minimal bet"
        }
        return result

    if is_valid_bet(bet_amount, station):
        card.money_amount -= bet_amount
        card.save()
        result = {"status": True}

    if bet_amount < station.min_bet:
        result = {
            "status": False,
            "reason": "Station minimal bet is higher"
        }
    if bet_amount > station.max_bet:
        result = {
            "status": False,
            "reason": "Your bet is too big"
        }

    return result


def get_money_from_station(sender_id, recipient_id, bet_amount):
    station = Station.objects.get(id=sender_id)
    team = Team.objects.get(id=recipient_id)
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

    if result['status']:
        add_transaction_to_database(sender, recipient, bet_amount)

    return result


def add_transaction_to_database(sender, recipient, bet_amount):
    last_transaction_id = Transaction.objects.count()
    sender_id = get_transaction_participant_id(sender)
    recipient_id = get_transaction_participant_id(recipient)

    if is_team(sender):
        sender = Team.objects.get(id=sender_id)
        recipient = Station.objects.get(id=recipient_id)
    else:
        sender = Station.objects.get(id=sender_id)
        recipient = Team.objects.get(id=recipient_id)

    transaction = Transaction(
        id=last_transaction_id+1,
        sender=sender,
        sender_id=sender_id,
        recipient=recipient,
        recipient_id=recipient_id,
        amount=bet_amount
    )
    transaction.save()
