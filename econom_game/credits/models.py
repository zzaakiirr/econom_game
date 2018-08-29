from django.db import models

from banks.models import Bank
from teams.models import Team


class Credit(models.Model):
    id = models.PositiveIntegerField(primary_key=True, unique=True)
    team = models.ForeignKey(Team, related_name='credit_team', default=None)
    bank = models.ForeignKey(Bank, related_name='credit_bank', default=None)
    debt_amount = models.PositiveIntegerField(default=0)
    term = models.PositiveIntegerField(default=1)

    def __str__(self):
        return 'credit_%d' % self.id
