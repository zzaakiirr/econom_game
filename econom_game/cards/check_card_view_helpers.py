from django.core.exceptions import ObjectDoesNotExist
import json

from teams.models import Team
from .models import Card

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
    expected_fields = ("card_type", "card")

    not_received_fields = helpers.get_not_recieved_fields(
        data, expected_fields
    )
    if not_received_fields:
        return helpers.get_not_received_all_expected_fields_error_response(
            not_received_fields)

    error_response = get_card_error_response(data)
    if error_response:
        return error_response
    return None


def get_card_error_response(data, check_has_card_team=True):
    response = {}
    card_type = data.get("card_type")
    card = data.get("card")

    if not is_valid_card_type(card_type):
        response['error'] = 'Неверный формат типа карты'

    elif not is_value_string_of_positive_integers(card):
        if card_type == 'card_number':
            response['error'] = 'Неверный формат номера карты'
        else:
            response['error'] = 'Неверный формат номера чипа карты'

    elif not get_card_from_db(card_type, card):
        response['error'] = 'Такой карты не существует'

    if not response and check_has_card_team:
        if not get_team_by_card(data):
            response['error'] = 'У этой карты нет команды'

    return response


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


def get_card_from_db(card_type, card):
    if card_type == 'card_number':
        try:
            card = Card.objects.get(card_number=card)
        except ObjectDoesNotExist:
            return None
    else:
        try:
            card = Card.objects.get(chip_number=card)
        except ObjectDoesNotExist:
            return None
    return card


def get_team_by_card(data):
    card = data.get('card')
    card_type = data.get('card_type')
    for team in Team.objects.all():
        team_card = get_team_card(team)
        if team_card:
            if card_type == 'card_number':
                if card == team_card.card_number:
                    return team
            else:
                if card == team_card.chip_number:
                    return team
    return None


def get_team_card(team):
    team_card = get_team_card_by_card_number(team)
    if team_card:
        return team_card
    team_card = get_team_card_by_chip_number(team)
    return team_card


def get_team_card_by_card_number(team):
    try:
        team_card = Card.objects.get(card_number=team.card.card_number)
    except ObjectDoesNotExist:
        return None
    return team_card


def get_team_card_by_chip_number(team):
    try:
        team_card = Card.objects.get(chip_number=team.card.chip_number)
    except ObjectDoesNotExist:
        return None
    return team_card
