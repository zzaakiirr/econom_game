from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from rest_framework import generics

from accounts.models import StationAdmin
from .models import Station

from .serializers import StationSerializer

from . import views_helpers


class ListStationsView(generics.ListAPIView):
    queryset = Station.objects.all()
    serializer_class = StationSerializer


@csrf_exempt
def create_station(request):
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})

    received_data = views_helpers.get_received_data(request)
    if not received_data['success']:
        return JsonResponse(received_data)

    new_station = views_helpers.create_new_station(received_data)
    if not new_station._state.db:
        return JsonResponse({
            "success": False,
            "error": "Станция не была добавлена в базу данных"
        })

    new_station_admin = views_helpers.create_new_station_admin(
        received_data, new_station)
    if not new_station_admin._state.db:
        return JsonResponse({
            "success": False,
            "error": "Держатель станции не был добавлен в базу данных"
        })

    views_helpers.add_user_model_permissions_to_user(
        user=new_station_admin.user, user_model=StationAdmin)

    return JsonResponse({"success": True})


@csrf_exempt
def make_bet(request):
    if not make_bet_view_helpers.get_station_admin(request):
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})

    received_data = make_bet_view_helpers.get_received_data(request)
    if not received_data['success']:
        return JsonResponse(received_data)

    if not make_bet_view_helpers.exclude_bet_amount_from_card(received_data):
        return JsonResponse({
            "success": False,
            "error": "Не удалось снять средства со счета"
        })

    transaction = make_bet_view_helpers.create_new_transaction(
        request, received_data
    )
    if not transaction._state.db:
        return JsonResponse({
            "success": False,
            "error": "Транзакция не была добавлена в базу данных"
        })

    return JsonResponse({"success": True})
