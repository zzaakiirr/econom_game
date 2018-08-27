from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.core.exceptions import ObjectDoesNotExist
import json

from .models import Card

import stations.views_helpers as helpers
from teams.views_helpers import is_value_string_of_positive_integers


def get_received_data(request):
    data = json.loads(request.body.decode("utf-8"))

    error_response = get_error_response(data)
    if error_response:
        error_response['success'] = False
        return error_response

    data['success'] = True
    return data


def get_error_response(data):
    expected_fields = ("card_number", "chip_number", "money_amount")

    not_received_fields = helpers.get_not_recieved_fields(
        data, expected_fields
    )
    if not_received_fields:
        return helpers.get_not_received_all_expected_fields_error_response(
            not_received_fields)

    response = {}
    card_number = data.get("card_number")
    chip_number = data.get("chip_number")
    money_amount = data.get("money_amount")

    if not helpers.is_unique_field('card_number', card_number, Card):
        response['error'] = 'Карта с номером %s уже существует' % card_number

    elif not helpers.is_unique_field('chip_number', chip_number, Card):
        response['error'] = (
            'Картa с номером чипа "%s" уже существует' % chip_number
        )

    elif not is_value_string_of_positive_integers(card_number):
        response['error'] = 'Неверный формат номера карты'

    elif not is_value_string_of_positive_integers(chip_number):
        response['error'] = 'Неверный формат номера чипа'

    elif not helpers.is_value_positive_integer(money_amount):
        response['error'] = 'Неверный формат количества денег'

    return response


def create_new_card(data):
    new_card_id = Card.objects.count() + 1
    new_card = Card.objects.create(
        id=new_card_id, card_number=data.get('card_number'),
        chip_number=data.get('chip_number'),
        money_amount=data.get('money_amount')
    )
    return new_card
