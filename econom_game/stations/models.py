from django.db import models


class Station(models.Model):
    id = models.PositiveIntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=30)
    owner = models.CharField(max_length=30)
    complexity = models.FloatField()
    min_bet = models.PositiveIntegerField()
    max_bet = models.PositiveIntegerField()

    def __str__(self):
        return self.name
