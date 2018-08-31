import json

from .models import Card

import stations.create_station_view_helpers as helpers
from .check_card_view_helpers import is_value_string_of_positive_integers


def get_create_card_response(request):
    data = json.loads(request.body.decode("utf-8"))

    expected_fields = ("card_number", "chip_number", "money_amount")
    not_received_fields = helpers.get_not_recieved_fields(
        data, expected_fields
    )
    if not_received_fields:
        return helpers.get_not_received_all_expected_fields_error_response(
            not_received_fields)

    card_number = data.get("card_number")
    chip_number = data.get("chip_number")
    money_amount = data.get("money_amount")

    error_response = get_error_response(card_number, chip_number, money_amount)
    if error_response:
        error_response['success'] = False
        return error_response

    new_card = create_new_card(card_number, chip_number, money_amount)
    if not new_card._state.db:
        return {
            "success": False,
            "error": "Карта не была добавлена в базу данных"
        }

    return {"success": True}


def get_error_response(card_number, chip_number, money_amount):
    response = {}

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


def create_new_card(card_number, chip_number, money_amount):
    new_card = Card.objects.create(
        card_number=card_number,
        chip_number=chip_number,
        money_amount=money_amount
    )
    return new_card
