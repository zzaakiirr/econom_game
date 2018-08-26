from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.core.exceptions import ObjectDoesNotExist
import json

from .models import Team, Card
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
    expected_fields = ("name", "owner", "faculty", "group", "bank", "card")

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

    if not helpers.is_unique_object_name(name, Team):
        response['error'] = 'Команда с именем "%s" уже существует' % name

    elif not helpers.is_value_positive_integer(bank):
        response['error'] = 'Неверный формат банка'

    elif not is_object_exist(object_id=bank, object_model=Bank):
        response['error'] = 'Такого банка не существует'

    elif not is_value_string_of_positive_integers(card):
        response['error'] = 'Неверный формат карты'

    elif not is_object_exist(object_id=int(card), object_model=Card):
        response['error'] = 'Такой карты не существует'

    return response


def is_object_exist(object_id, object_model):
    try:
        object_model.objects.get(id=object_id)
    except ObjectDoesNotExist:
        return False
    else:
        return True


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
