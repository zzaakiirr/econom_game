from django.db import models
from django.core.validators import MaxValueValidator


class Team(models.Model):
    id = models.PositiveIntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=25)
    login = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class Card(models.Model):
    id = models.PositiveIntegerField(primary_key=True, unique=True)
    cvv = models.PositiveIntegerField(validators=[MaxValueValidator(999)])
    money_amount = models.PositiveIntegerField()
    team = models.ForeignKey(Team, related_name='team', default=None)

    def __str__(self):
        return str(self.id)
