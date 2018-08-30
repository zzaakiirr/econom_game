from django.forms.models import model_to_dict


def get_station_dict(station_admin):
    station_dict = model_to_dict(station_admin.station)
    return station_dict
