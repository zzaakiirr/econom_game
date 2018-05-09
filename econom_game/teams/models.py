from django.db import models
from django.core.validators import RegexValidator


class Card(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    cvv = models.CharField(
        max_length=3,
        validators=[RegexValidator(r'^\d{1,10}$')]
    )
    money_amount = models.PositiveIntegerField()

    def __str__(self):
        return self.id


class Team(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=25)
    login = models.CharField(max_length=25)
    card = models.ForeignKey(Card, related_name='card')

    def __str__(self):
        return self.name
