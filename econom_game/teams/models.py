from django.db import models

from banks.models import Bank
from cards.models import Card


class Team(models.Model):
    name = models.CharField(max_length=25, unique=True)
    owner = models.CharField(max_length=25)
    faculty = models.CharField(max_length=25)
    group = models.CharField(max_length=25)
    bank = models.ForeignKey(Bank, related_name='team_bank', default=None)
    card = models.ForeignKey(Card, related_name='team_card', default=None)

    def __str__(self):
        return self.name
