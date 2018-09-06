from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.db.models import Max
from django.contrib.auth import get_user_model
import json

from .models import Station
from accounts.models import StationAdmin

from . import accounts_database_helpers


User = get_user_model()


def fetch_create_station_response(request):
    data = json.loads(request.body.decode("utf-8"))

    expected_fields = (
        "name", "complexity", "min_bet", "max_bet", "email", "owner"
    )
    not_received_fields = get_not_recieved_fields(data, expected_fields)
    if not_received_fields:
        return get_not_received_all_expected_fields_error_response(
            not_received_fields)

    name = data.get("name")
    owner = data.get("owner")
    complexity = data.get("complexity")
    min_bet = data.get("min_bet")
    max_bet = data.get("max_bet")
    email = data.get("email")

    error_response = get_error_response(
        name, complexity, min_bet, max_bet, email
    )
    if error_response:
        error_response['success'] = False
        return error_response

    new_station = create_new_station(name, owner, complexity, min_bet, max_bet)
    if not new_station._state.db:
        return {
            "success": False,
            "error": "Станция не была добавлена в базу данных"
        }

    new_station_admin = create_new_station_admin(email, new_station)
    if not new_station_admin._state.db:
        return {
            "success": False,
            "error": "Держатель станции не был добавлен в базу данных"
        }

    add_user_model_permissions_to_user(
        user=new_station_admin.user,
        user_model=StationAdmin
    )
    return {"success": True}


def get_error_response(name, complexity, min_bet, max_bet, email):
    response = {}

    if not is_unique_field(field_name='name', field_value=name, model=Station):
        response['error'] = 'Станция с именем "%s" уже существует' % name

    elif not complexity > 0:
        response['error'] = "Неверный формат множителя"

    elif not is_value_positive_integer(min_bet):
        response['error'] = 'Неверный формат минимальной ставки'

    elif not is_value_positive_integer(max_bet):
        response['error'] = 'Неверный формат максимальной ставки'

    elif not is_max_bet_greater_min_bet(max_bet, min_bet):
        response["error"] = "Максимальная ставка меньше минимальной ставки"

    elif is_email_in_use(email):
        response['error'] = 'email "%s" уже занят' % email

    return response


def get_not_recieved_fields(data, expected_fields):
    not_received_fields = []
    for expected_field in expected_fields:
        if data.get(expected_field) is None:
            not_received_fields.append(expected_field)
    return not_received_fields


def get_not_received_all_expected_fields_error_response(
        not_received_fields):
    response = {'success': False}

    if len(not_received_fields) == 1:
        for not_received_field in not_received_fields:
            response["error"] = "Поле %s пустое" % not_received_field

    elif len(not_received_fields) > 1:
        not_received_fields_string = ""
        for not_received_field in not_received_fields:
            not_received_fields_string += "%s, " % not_received_field
        response["error"] = "Поля [%s] пустые" % (
            not_received_fields_string[:-2])

    return response


def is_unique_field(field_name, field_value, model):
    for object_instance in model.objects.values():
        if field_value == object_instance.get(field_name):
            return False
    return True


def is_value_positive_integer(value):
    return isinstance(value, int) and value >= 0


def is_max_bet_greater_min_bet(max_bet, min_bet):
    return max_bet >= min_bet


def is_email_in_use(email):
    for user in User.objects.all():
        if user.email == email:
            return True
    return False


def create_new_station(name, owner, complexity, min_bet, max_bet):
    new_station = Station.objects.create(
        name=name, owner=owner,
        complexity=complexity, min_bet=min_bet, max_bet=max_bet,
    )
    return new_station


def create_new_station_admin(email, new_station):
    user = User.objects.create_user(email=email, password=email)
    new_station_admin = StationAdmin.objects.create(
        station=new_station, user=user
    )
    accounts_database_helpers.load_account_to_db(email=email, password=email)
    return new_station_admin


def add_user_model_permissions_to_user(user, user_model):
    user_model_content_type = ContentType.objects.get_for_model(user_model)
    user_model_permissions = Permission.objects.filter(
        content_type=user_model_content_type
    )
    for user_model_permission in user_model_permissions:
        user.user_permissions.add(user_model_permission)
