from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.views import status
from rest_framework.response import Response

from .models import Station
from .serializers import StationSerializer


class ListStationsView(generics.ListAPIView):
    queryset = Station.objects.all()
    serializer_class = StationSerializer


def create_station(request):
    id = request.GET['id']
    name = request.GET['name']
    complexity = request.GET['complexity']
    min_bet = request.GET['min_bet']
    max_bet = request.GET['max_bet']

    old_stations_count = Station.objects.count()
    new_station = Station.objects.create(
        id=id, name=name,
        complexity=complexity, min_bet=min_bet, max_bet=max_bet
    )
    new_station.save()
    new_stations_count = Station.objects.count()
    if new_stations_count == old_stations_count + 1:
        return JsonResponse({"status": True})
