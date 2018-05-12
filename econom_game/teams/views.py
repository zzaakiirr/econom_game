from django.shortcuts import render
from rest_framework import generics

from .models import Team
from .serializers import TeamSerializer


class ListTeamsView(generics.ListAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
