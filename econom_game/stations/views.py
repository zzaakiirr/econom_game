from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from rest_framework import generics

from .models import Station
from .serializers import StationSerializer

from .views_helpers import fetch_response


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

    response = fetch_response(request)
    if not response['success']:
        return JsonResponse(response)
    # new_station = Station.objects.create(
    #     id=id, name=name,
    #     complexity=complexity, min_bet=min_bet, max_bet=max_bet
    # )

    # if new_station._state.db:
    #     return JsonResponse({"status": True})
    return JsonResponse({"status": True})
