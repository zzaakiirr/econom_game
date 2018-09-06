from django.core.management.base import BaseCommand, CommandError

from teams.models import Team
from shares.models import ShareDeal
from timings.models import Timing

from timings.management.commands.increasehalfyear import get_timing


class Command(BaseCommand):
    help = 'Transfer to teams card percentage of their shares'

    def handle(self, *args, **options):
        timing = get_timing()
        if not timing.game_started:
            return
        current_half_year = timing.current_half_year
        teams = Team.objects.all()
        for team in teams:
            share_deals = ShareDeal.objects.filter(team=team)
            for share_deal in share_deals:
                share_current_half_year_price = (
                    share_deal.share_type.stock_price.filter(
                        half_year=current_half_year)[0].buy_price
                )
                team.card.money_amount += (
                    share_deal.amount * share_current_half_year_price * 0.1
                )
                team.card.save()
