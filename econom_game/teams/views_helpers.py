from django.core.exceptions import ObjectDoesNotExist
import json

from .models import Team
from cards.models import Card
from banks.models import Bank

import stations.create_station_view_helpers as helpers
import cards.check_card_view_helpers as check_card


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

    response = check_card.get_card_error_response(
        data, check_has_card_team=False
    )
    if response.get('error'):
        return response

    if not helpers.is_unique_field('name', name, Team):
        response['error'] = 'Команда с именем "%s" уже существует' % name

    elif not helpers.is_value_positive_integer(bank):
        response['error'] = 'Неверный формат банка'

    elif not is_object_exist(object_id=bank, object_model=Bank):
        response['error'] = 'Такого банка не существует'

    if check_card.get_team_by_card(data):
        response['error'] = 'Команда с такой картой уже существует'

    return response


def is_object_exist(object_id, object_model):
    try:
        object_model.objects.get(id=object_id)
    except ObjectDoesNotExist:
        return False
    else:
        return True


def create_new_team(data):
    new_team_id = helpers.create_unique_id(Team)
    card = check_card.get_card_from_db(
        data.get('card_type'),
        data.get('card')
    )
    bank = Bank.objects.get(id=data.get('bank'))

    new_team = Team.objects.create(
        id=new_team_id, name=data.get('name'), owner=data.get('owner'),
        faculty=data.get('faculty'), group=data.get('group'),
        bank=bank, card=card
    )
    return new_team
