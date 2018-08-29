from django.core.exceptions import ObjectDoesNotExist
import json

from .models import Team
from cards.models import Card
from banks.models import Bank

import stations.create_station_view_helpers as helpers


def get_received_data(request):
    data = json.loads(request.body.decode("utf-8"))

    error_response = get_error_response(data)
    if error_response:
        error_response['success'] = False
        return error_response

    data['success'] = True
    return data


def get_error_response(data):
    expected_fields = (
        "name", "owner", "faculty", "group", "bank", "card", "card_type"
    )

    not_received_fields = helpers.get_not_recieved_fields(
        data, expected_fields
    )
    if not_received_fields:
        return helpers.get_not_received_all_expected_fields_error_response(
            not_received_fields)

    response = {}
    name = data.get("name")
    owner = data.get("owner")
    faculty = data.get("faculty")
    group = data.get("group")
    bank = data.get("bank")
    card = data.get("card")
    card_type = data.get("card_type")

    if not helpers.is_unique_field('name', name, Team):
        response['error'] = 'Команда с именем "%s" уже существует' % name

    elif is_exist_team_with_same_card(card_type, card):
        response['error'] = 'Команда с такой картой уже существует'

    elif not helpers.is_value_positive_integer(bank):
        response['error'] = 'Неверный формат банка'

    elif not is_object_exist(object_id=bank, object_model=Bank):
        response['error'] = 'Такого банка не существует'

    elif not is_value_string_of_positive_integers(card):
        response['error'] = 'Неверный формат карты'

    elif not is_valid_card_type(card_type):
        response['error'] = 'Неверный формат метода карты'

    elif not is_card_exist(card, card_type):
        response['error'] = 'Такой карты не существует'

    return response


def is_exist_team_with_same_card(card_type, card):
    card = get_card(card_type, card)
    for team in Team.objects.all():
        if team.card == card:
            return True
    return False


def is_object_exist(object_id, object_model):
    try:
        object_model.objects.get(id=object_id)
    except ObjectDoesNotExist:
        return False
    else:
        return True


def is_card_exist(received_number, card_type):
    if card_type == 'card_number':
        for card in Card.objects.all():
            if received_number == card.card_number:
                return True
    elif card_type == 'chip_number':
        for card in Card.objects.all():
            if received_number == card.chip_number:
                return True
    return False


def is_valid_card_type(received_card_type):
    card_types = ("card_number", "chip_number")
    for card_type in card_types:
        if received_card_type == card_type:
            return True
    return False


def is_value_string_of_positive_integers(value):
    try:
        int(value)
    except ValueError:
        return False
    else:
        return isinstance(value, str)


def create_new_team(data):
    new_team_id = Team.objects.count() + 1
    card = get_card(data.get('card_type'), data.get('card'))
    bank = Bank.objects.get(id=data.get('bank'))
    new_team = Team.objects.create(
        id=new_team_id, name=data.get('name'), owner=data.get('owner'),
        faculty=data.get('faculty'), group=data.get('group'),
        bank=bank, card=card
    )
    return new_team


def get_card(card_type, received_number):
    if card_type == 'card_number':
        for card in Card.objects.all():
            if received_number == card.card_number:
                return card
    elif card_type == 'chip_number':
        for card in Card.objects.all():
            if received_number == card.chip_number:
                return card
    return None
