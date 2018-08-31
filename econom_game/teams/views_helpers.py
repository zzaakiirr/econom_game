from django.core.exceptions import ObjectDoesNotExist
import json

from .models import Team
from cards.models import Card
from banks.models import Bank

import stations.create_station_view_helpers as helpers
import cards.check_card_view_helpers as check_card


def get_create_team_response(request):
    data = json.loads(request.body.decode("utf-8"))

    expected_fields = (
        "name", "owner", "faculty", "group",
        "bank", "card", "card_type"
    )
    not_received_fields = helpers.get_not_recieved_fields(
        data, expected_fields
    )
    if not_received_fields:
        return helpers.get_not_received_all_expected_fields_error_response(
            not_received_fields)

    name = data.get("name")
    owner = data.get("owner")
    faculty = data.get("faculty")
    group = data.get("group")
    bank = data.get("bank")
    card = data.get("card")
    card_type = data.get("card_type")

    error_response = get_error_response(
        name, owner, faculty, group,
        bank, card_type, card
    )
    if error_response:
        error_response['success'] = False
        return error_response

    new_team = create_new_team(
        name, owner, faculty, group,
        bank, card_type, card
    )
    if not new_team._state.db:
        return {
            "success": False,
            "error": "Команда не была добавлена в базу данных"
        }

    return {"success": True}


def get_error_response(name, owner, faculty, group, bank, card_type, card):
    card_error_response = check_card.get_card_error_response(
        card_type, card,
        check_has_card_team=False
    )
    if card_error_response.get('error'):
        return card_error_response

    response = {}
    if not helpers.is_unique_field('name', name, Team):
        response['error'] = 'Команда с именем "%s" уже существует' % name

    elif not helpers.is_value_positive_integer(bank):
        response['error'] = 'Неверный формат банка'

    elif not is_object_exist(object_id=bank, object_model=Bank):
        response['error'] = 'Такого банка не существует'

    if check_card.get_team_by_card(card_type, card):
        response['error'] = 'Команда с такой картой уже существует'

    return response


def is_object_exist(object_id, object_model):
    try:
        object_model.objects.get(id=object_id)
    except ObjectDoesNotExist:
        return False
    else:
        return True


def create_new_team(name, owner, faculty, group, bank, card_type, card):
    card = check_card.get_card_from_db(card_type, card)
    bank = Bank.objects.get(id=bank)
    new_team = Team.objects.create(
        name=name, owner=owner,
        faculty=faculty, group=group,
        bank=bank, card=card
    )
    return new_team
