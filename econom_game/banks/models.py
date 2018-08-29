from django.db import models

from banks.models import Bank
from teams.models import Team


class Bank(models.Model):
    id = models.PositiveIntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=30, unique=True)
    deposit = models.FloatField()
    credit_for_one_year = models.FloatField()
    credit_for_two_years = models.FloatField()

    def __str__(self):
        return 'bank_%d' % self.id


class Credit(models.Model):
    id = models.PositiveIntegerField(primary_key=True, unique=True)
    team = models.ForeignKey(Team, related_name='credit_team', default=None)
    bank = models.ForeignKey(Bank, related_name='credit_bank', default=None)
    debt_amount = models.PositiveIntegerField(default=0)
    term = models.PositiveIntegerField(default=1)

    def __str__(self):
        return 'credit_%d' % self.id


class Deposit(models.Model):
    id = models.PositiveIntegerField(primary_key=True, unique=True)
    team = models.ForeignKey(Team, related_name='deposit_team', default=None)
    bank = models.ForeignKey(Bank, related_name='deposit_bank', default=None)
    money_amount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return 'deposit_%d' % self.id
