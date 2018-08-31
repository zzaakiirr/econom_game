from django.core.management.base import BaseCommand, CommandError

from teams.models import Team
from deposits.models import Deposit
from timings.models import Timing


class Command(BaseCommand):
    help = 'Transfer to teams card percentage of their deposit'

    def handle(self, *args, **options):
        if not Timing.objects.get(id=1).game_started:
            return
        teams = Team.objects.all()
        for team in teams:
            deposit = Deposit.objects.filter(team=team)[0]
            if not deposit or deposit.invest_amount == 0:
                return
            team.card.money_amount += deposit.invest_amount * team.bank.deposit
            team.card.save()
