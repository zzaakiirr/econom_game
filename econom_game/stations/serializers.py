from rest_framework import serializers

from .models import Station


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ("id", "name", "complexity", "min_bet", "max_bet")
