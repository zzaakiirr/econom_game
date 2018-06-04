from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test

from rest_framework import generics
from rest_framework.views import status
from rest_framework.response import Response

from .models import Station
from .serializers import StationSerializer
import views_helpers


class ListStationsView(generics.ListAPIView):
    queryset = Station.objects.all()
    serializer_class = StationSerializer


@user_passes_test(lambda u: u.is_superuser)
def create_station(request):
    id = request.GET['id']
    name = request.GET['name']
    complexity = request.GET['complexity']
    min_bet = request.GET['min_bet']
    max_bet = request.GET['max_bet']

    Station.objects.create(
        id=id, name=name,
        complexity=complexity, min_bet=min_bet, max_bet=max_bet
    )
    new_station = Station.objects.get(id=id)

    if views_helpers.is_in_database(new_station, Station):
        return JsonResponse({"status": True})
    return JsonResponse({"status": False})
