from django.db import models
from django.core.validators import RegexValidator


class Station(models.Model):
    station_id = models.PositiveIntegerField(primary_key=True, unique=True)
    station_name = models.CharField(max_length=30)
    complexity = models.CharField(
        max_length=1,
        validators=[RegexValidator(r'^\d{2,3}$')]
    )
    min_bet = models.PositiveIntegerField()
    max_bet = models.PositiveIntegerField()
