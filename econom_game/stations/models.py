from django.db import models


class Station(models.Model):
    name = models.CharField(max_length=30)
    owner = models.CharField(max_length=30)
    complexity = models.FloatField()
    min_bet = models.FloatField()
    max_bet = models.FloatField()

    def __str__(self):
        return self.name
