from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from rest_framework import generics

from .models import Station
from .serializers import StationSerializer

from . import views_helpers


class ListStationsView(generics.ListAPIView):
    queryset = Station.objects.all()
    serializer_class = StationSerializer


@csrf_exempt
def create_station(request):
    # if not request.user.is_superuser:
    #     return JsonResponse({'success': False, 'error': 'Permission denied'})

    if request.method == 'GET':
        return JsonResponse(
            {'success': False, 'error': 'This is not POST request'}
        )

    received_data = views_helpers.get_received_data(request)
    if not received_data.get('success'):
        return JsonResponse(received_data)

    new_station = views_helpers.create_new_station(received_data)
    if not new_station._state.db:
        return JsonResponse({
            "status": False, "error": "Station does not in database"
        })

    new_station_admin = views_helpers.create_new_station_admin(
        received_data, new_station)
    if not new_station_admin._state.db:
        return JsonResponse({
            "status": False, "error": "Station does not in database"
        })

    return JsonResponse({"status": True})
