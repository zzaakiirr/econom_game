from django.db import models

from teams.models import Team
from banks.models import Bank


class Deposit(models.Model):
    id = models.PositiveIntegerField(primary_key=True, unique=True)
    team = models.ForeignKey(Team, related_name='deposit_team', default=None)
    bank = models.ForeignKey(Bank, related_name='deposit_bank', default=None)
    invest_amount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return 'deposit_%d' % self.id
