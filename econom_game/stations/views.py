from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import status
from rest_framework.response import Response

from .models import Station
from .serializers import StationSerializer


class ListStationsView(generics.ListAPIView):
    queryset = Station.objects.all()
    serializer_class = StationSerializer

        # return Response(serialized.data, status=status.HTTP_201_CREATED)
    # else:
    #     return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


def create_station(request):
    id = request.GET['id']
    stations_count = Station.objects.count()
    new_station = Station.objects.create(
        id=id, name="station_2",
        complexity=2, min_bet=1, max_bet=2
    )
    new_station.save()
    if(Station.objects.count() == stations_count + 1):
        return Response({"status": True}, status=status.HTTP_201_CREATED)
    return {"status": False}
