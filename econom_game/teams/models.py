from django.db import models
from django.core.validators import MaxValueValidator


class Card(models.Model):
    id = models.PositiveIntegerField(primary_key=True, unique=True)
    cvv = models.PositiveIntegerField(validators=[MaxValueValidator(999)])
    money_amount = models.PositiveIntegerField()

    def __str__(self):
        return 'card_%d' % self.id


class Team(models.Model):
    id = models.PositiveIntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=25)
    owner = models.CharField(max_length=25)
    faculty = models.CharField(max_length=25)
    group = models.CharField(max_length=25)
    bank = models.PositiveIntegerField()
    card = models.CharField(max_length=25)

    def __str__(self):
        return self.name
