from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from rest_framework import generics

from accounts.models import StationAdmin
from .models import Station

from .serializers import StationSerializer

from . import create_station_view_helpers
from . import make_bet_view_helpers
from . import victory_view_helpers
from .get_station_info_helpers import get_station_dict


class ListStationsView(generics.ListAPIView):
    queryset = Station.objects.all()
    serializer_class = StationSerializer


@csrf_exempt
def create_station(request):
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})

    received_data = create_station_view_helpers.get_received_data(request)
    if not received_data['success']:
        return JsonResponse(received_data)

    new_station = create_station_view_helpers.create_new_station(received_data)
    if not new_station._state.db:
        return JsonResponse({
            "success": False,
            "error": "Станция не была добавлена в базу данных"
        })

    new_station_admin = create_station_view_helpers.create_new_station_admin(
        received_data, new_station)
    if not new_station_admin._state.db:
        return JsonResponse({
            "success": False,
            "error": "Держатель станции не был добавлен в базу данных"
        })

    create_station_view_helpers.add_user_model_permissions_to_user(
        user=new_station_admin.user, user_model=StationAdmin)

    return JsonResponse({"success": True})


@csrf_exempt
def make_bet(request):
    if not make_bet_view_helpers.get_station_admin(request):
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})

    received_data = make_bet_view_helpers.get_received_data(request)
    if not received_data['success']:
        return JsonResponse(received_data)

    make_bet_view_helpers.exclude_bet_amount_from_card(received_data)

    transaction = make_bet_view_helpers.create_new_transaction(
        request, received_data
    )
    if not transaction._state.db:
        return JsonResponse({
            "success": False,
            "error": "Транзакция не была добавлена в базу данных"
        })

    return JsonResponse({"success": True})


@csrf_exempt
def victory(request):
    if not make_bet_view_helpers.get_station_admin(request):
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
    station_admin = make_bet_view_helpers.get_station_admin(request)
    if not station_admin:
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})

    station_dict = get_station_dict(station_admin)
    response = {
        'success': True,
        'station': station_dict
    }
    return JsonResponse(response)
