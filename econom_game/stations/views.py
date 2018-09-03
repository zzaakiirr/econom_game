from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from rest_framework import generics

from accounts.models import StationAdmin
from .models import Station

from .serializers import StationSerializer

from . import victory_view_helpers
from .get_station_info_helpers import get_station_dict
from .create_station_view_helpers import fetch_create_station_response
from .make_bet_view_helpers import fetch_make_bet_response, get_station_admin


class ListStationsView(generics.ListAPIView):
    queryset = Station.objects.all()
    serializer_class = StationSerializer


@csrf_exempt
def create_station(request):
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})

    response = fetch_create_station_response(request)
    return JsonResponse(response)


@csrf_exempt
def make_bet(request):
    if not get_station_admin(request):
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})

    response = fetch_make_bet_response(request)
    return JsonResponse(response)


@csrf_exempt
def victory(request):
    if not get_station_admin(request):
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})

    received_data = victory_view_helpers.get_received_data(request)
    if not received_data['success']:
        return JsonResponse(received_data)

    if not received_data['victory']:
        victory_view_helpers.change_victory_status(
            request, received_data, False
        )
        victory_view_helpers.change_transaction_processed_status(
            request, received_data, True
        )
    else:
        victory_view_helpers.change_victory_status(
            request, received_data, True
        )
        victory_view_helpers.change_transaction_processed_status(
            request, received_data, False
        )

    return JsonResponse({"success": True})


@csrf_exempt
def get_station_info(request):
    station_admin = get_station_admin(request)
    if not station_admin:
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})

    station_dict = get_station_dict(station_admin)
    response = {
        'success': True,
        'station': station_dict
    }
    return JsonResponse(response)
