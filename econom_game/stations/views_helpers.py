from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.http import JsonResponse
import json

from .models import Station
from accounts.models import User, StationAdmin


def get_not_recieved_fields(expected_fields, data):
    not_received_fields = []
    for expected_field in expected_fields:
        if not data.get(expected_field):
            not_received_fields.append(expected_field)
    return not_received_fields


def has_received_expected_fields(expected_fields, data):
    for expected_field in expected_fields:
        if not data.get(expected_field):
            return False
    return True


def get_has_not_received_expected_fields_response(not_received_fields):
    response = {"success": False}
    if len(not_received_fields) == 1:
        for not_received_field in not_received_fields:
            response["error"] = "Field %s is empty" % not_received_field
        return response

    elif len(not_received_fields) > 1:
        not_received_fields_string = ""
        for not_received_field in not_received_fields:
            not_received_fields_string += "%s, " % not_received_field
        response["error"] = "Fields [%s] are empty" % (
            not_received_fields_string[:-2])
        return response


def is_unique_station_name(station_name):
    for station in Station.objects.all():
        if station_name == station.name:
            return False
    return True


def get_not_unique_station_name_response(station_name):
    return {
        "status": False,
        "error": 'Station name "%s" already exists' % station_name
    }


def get_is_not_possitive_integer(field_values):
    for field, value in field_values.items():
        if value < 0 or not isinstance(value, int):
            return field
    return None


def get_is_not_possitive_integer_field_response(
        is_not_possitive_integer_field):
    return {
        "success": False,
        "error": 'Invalid "%s" format' % is_not_possitive_integer_field
    }


def is_max_bet_greater_min_bet(max_bet, min_bet):
    return max_bet > min_bet


def get_is_not_max_bet_greater_min_bet():
    return {
        "success": False,
        "error": "max_bet less than min_bet"
    }


def is_not_email_in_use(email):
    for user in User.objects.all():
        if user.email == email:
            return False
    return True


def get_received_data(request):
    response = {"success": False}
    data = json.loads(request.body.decode("utf-8"))

    expected_fields = ["name", "min_bet", "max_bet", "email", "owner"]
    if not has_received_expected_fields(expected_fields, data):
        not_received_fields = get_not_recieved_fields(expected_fields, data)
        return get_has_not_received_expected_fields_response(
            not_received_fields)

    name = data.get("name")
    complexity = data.get("complexity")
    min_bet = data.get("min_bet")
    max_bet = data.get("max_bet")
    email = data.get("email")
    owner = data.get("owner")

    if not is_unique_station_name(name):
        return get_not_unique_station_name_response(name)

    is_not_possitive_integer_field = get_is_not_possitive_integer({
            "complexity": complexity, "min_bet": min_bet, "max_bet": max_bet
        })
    if is_not_possitive_integer_field:
        return get_is_not_possitive_integer_field_response(
            is_not_possitive_integer_field)

    if not is_max_bet_greater_min_bet(max_bet, min_bet):
        response["error"] = "max_bet less than min_bet"
        return response

    if not is_not_email_in_use(email):
        response['error'] = "This email already in use"
        return response

    data['success'] = True
    return data


def create_new_station(data):
    new_station_id = Station.objects.count()+1
    new_station = Station.objects.create(
        id=new_station_id, name=data.get('name'), owner=data.get('owner'),
        complexity=data.get('complexity'), min_bet=data.get('min_bet'),
        max_bet=data.get('max_bet'),
    )
    return new_station


def create_new_station_admin(data, new_station):
    random_password = User.objects.make_random_password()
    user = User.objects.create_user(
        email=data.get('email'), password=random_password,
        first_name=data.get('name')
    )
    new_station_admin = StationAdmin.objects.create(
        station=new_station, user=user)
    return new_station_admin


def add_user_model_permissions_to_user(user, user_model):
    user_model_content_type = ContentType.objects.get_for_model(user_model)
    user_model_permissions = Permission.objects.filter(
        content_type=user_model_content_type)
    for user_model_permission in user_model_permissions:
        user.user_permissions.add(user_model_permission)
