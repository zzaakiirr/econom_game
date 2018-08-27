from django.core.exceptions import ObjectDoesNotExist
import json

from .models import Team
from cards.models import Card
from banks.models import Bank

import stations.views_helpers as helpers


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
        "name", "owner", "faculty", "group", "bank", "card", "card_method"
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
    card_method = data.get("card_method")

    if not helpers.is_unique_field('name', name, Team):
        response['error'] = 'Команда с именем "%s" уже существует' % name

    elif not helpers.is_unique_field('card', card, Team):
        response['error'] = 'Команда с картой "%s" уже существует' % card

    elif not helpers.is_value_positive_integer(bank):
        response['error'] = 'Неверный формат банка'

    elif not is_object_exist(object_id=bank, object_model=Bank):
        response['error'] = 'Такого банка не существует'

    elif not is_value_string_of_positive_integers(card):
        response['error'] = 'Неверный формат карты'

    elif not is_valid_card_method(card_method):
        response['error'] = 'Неверный формат метода карты'

    elif not is_card_exist(card, card_method):
        response['error'] = 'Такой карты не существует'

    return response


def is_object_exist(object_id, object_model):
    try:
        object_model.objects.get(id=object_id)
    except ObjectDoesNotExist:
        return False
    else:
        return True


def is_card_exist(received_number, card_method):
    if card_method == 'card_number':
        for card in Card.objects.all():
            if received_number == card.card_number:
                return True
    elif card_method == 'chip_number':
        for card in Card.objects.all():
            if received_number == card.chip_number:
                return True
    return False


def is_valid_card_method(received_card_method):
    card_methods = ("card_number", "chip_number")
    for card_method in card_methods:
        if received_card_method == card_method:
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
    new_team = Team.objects.create(
        id=new_team_id, name=data.get('name'), owner=data.get('owner'),
        faculty=data.get('faculty'), group=data.get('group'),
        bank=data.get('bank'), card=data.get('card')
    )
    return new_team
