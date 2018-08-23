from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.http import JsonResponse
import json

from .models import Station
from accounts.models import User, StationAdmin

from . import accounts_database_helpers


def get_not_recieved_fields(data, expected_fields):
    not_received_fields = []
    for expected_field in expected_fields:
        if not data.get(expected_field):
            not_received_fields.append(expected_field)
    return not_received_fields


def get_not_received_all_expected_fields_error_response(
        not_received_fields):
    response = {}

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


def is_unique_station_name(station_name):
    for station in Station.objects.all():
        if station_name == station.name:
            return False
    return True


def is_value_positive_float(value):
    return value > 0 and isinstance(value, float)


def is_value_positive_integer(value):
    return value > 0 and isinstance(value, int)


def is_max_bet_greater_min_bet(max_bet, min_bet):
    return max_bet >= min_bet


def is_email_in_use(email):
    for user in User.objects.all():
        if user.email == email:
            return True
    return False


def get_error_response(data):
    expected_fields = (
        "name", "complexity", "min_bet", "max_bet", "email", "owner"
    )
    not_received_fields = get_not_recieved_fields(data, expected_fields)
    if not_received_fields:
        return get_not_received_all_expected_fields_error_response(
            not_received_fields)

    response = {}
    name = data.get("name")
    complexity = data.get("complexity")
    min_bet = data.get("min_bet")
    max_bet = data.get("max_bet")
    email = data.get("email")

    if not is_unique_station_name(name):
        response['error'] = 'Станция с именем "%s" уже существует' % name

    elif not is_value_positive_float(complexity):
        response['error'] = 'Неверный формат множителя'

    elif not is_value_positive_integer(min_bet):
        response['error'] = 'Неверный формат минимальной ставки'

    elif not is_value_positive_integer(max_bet):
        response['error'] = 'Неверный формат максимальной ставки'

    elif not is_max_bet_greater_min_bet(max_bet, min_bet):
        response["error"] = "Максимальная ставка меньше минимальной ставки"

    elif is_email_in_use(email):
        response['error'] = 'email "%s" уже занят' % email

    return response


def get_received_data(request):
    data = json.loads(request.body.decode("utf-8"))

    error_response = get_error_response(data)
    if error_response:
        error_response['success'] = False
        return error_response

    data['success'] = True
    return data


def create_new_station(data):
    new_station_id = Station.objects.count() + 1
    new_station = Station.objects.create(
        id=new_station_id, name=data.get('name'), owner=data.get('owner'),
        complexity=data.get('complexity'), min_bet=data.get('min_bet'),
        max_bet=data.get('max_bet'),
    )
    return new_station


def create_new_station_admin(data, new_station):
    password = User.objects.make_random_password()
    email = data.get('email')

    user = User.objects.create_user(
        email=email, password=password,
        first_name=data.get('name')
    )
    new_station_admin = StationAdmin.objects.create(
        station=new_station, user=user)
    accounts_database_helpers.load_account_to_db(email, password)

    return new_station_admin


def add_user_model_permissions_to_user(user, user_model):
    user_model_content_type = ContentType.objects.get_for_model(user_model)
    user_model_permissions = Permission.objects.filter(
        content_type=user_model_content_type)
    for user_model_permission in user_model_permissions:
        user.user_permissions.add(user_model_permission)
