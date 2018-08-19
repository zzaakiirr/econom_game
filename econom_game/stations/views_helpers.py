from django.http import JsonResponse
import json

from .models import Station


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
        if station_name in station.name:
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


def fetch_response(request):
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

    return {"success": True}
