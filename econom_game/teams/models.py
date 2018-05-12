from django.db import models
from django.core.validators import MaxValueValidator


class Card(models.Model):
    id = models.PositiveIntegerField(primary_key=True, unique=True)
    cvv = models.PositiveIntegerField(
        validators=[MaxValueValidator(999)],
        unique=True
    )
    money_amount = models.PositiveIntegerField()

    def __str__(self):
        return 'card_%d' % self.id


class Team(models.Model):
    id = models.PositiveIntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=25)
    login = models.CharField(max_length=25, unique=True)
    card = models.ForeignKey(Card, related_name='card', default=None)

    def __str__(self):
        return self.name
