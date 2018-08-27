from django.core.exceptions import ObjectDoesNotExist
import json

from teams.models import Team
from .models import Card

import stations.views_helpers as helpers
from teams.views_helpers import is_value_string_of_positive_integers
from teams.views_helpers import is_valid_card_type


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

    elif not is_card_exist(card_type, card):
        response['error'] = 'Такой карты не существует'

    return response


def is_card_exist(card_type, card):
    if card_type == 'card_number':
        try:
            Card.objects.get(card_number=card)
        except ObjectDoesNotExist:
            return False
    else:
        try:
            Card.objects.get(chip_number=card)
        except ObjectDoesNotExist:
            return False
    return True


def get_team_by_card(data):
    card = data.get('card')
    for team in Team.objects.all():
        team_card = get_team_card(team)
        if card == team_card.card_number or card == team_card.chip_number:
            return team
    return None


def get_team_card(team):
    try:
        team_card = get_team_card_by_card_number(team)
    except ObjectDoesNotExist:
        team_card = get_team_card_by_chip_number(team)
    return team_card


def get_team_card_by_card_number(team):
    team_card = Card.objects.get(card_number=team.card)
    return team_card


def get_team_card_by_chip_number(team):
    team_card = Card.objects.get(chip_number=team.card)
    return team_card
