from django.shortcuts import render
from rest_framework import generics

from .models import Station
from .serializers import StationSerializer


class ListStationsView(generics.ListAPIView):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
