from django.core.management.base import BaseCommand, CommandError

from credits.models import Credit
from timings.models import Timing

from timings.management.commands.increasehalfyear import get_timing


class Command(BaseCommand):
    help = 'Increase teams credit debt amount'

    def handle(self, *args, **options):
        if not Timing.objects.get(id=1).game_started:
            return
        credits = Credit.objects.all()
        for credit in credits:
            if is_credit_overdue(credit):
                credit.debt_amount += credit.debt_amount / 2
                credit.save()
                return

            if credit.term == 1:
                credit.debt_amount += (
                    credit.bank.credit_for_one_year * credit.debt_amount
                )
            else:
                credit.debt_amount += (
                    credit.bank.credit_for_two_years * credit.debt_amount
                )

            credit.save()


def is_credit_overdue(credit):
    current_half_year = Timing.objects.get(id=1).current_half_year
    return credit.half_year + credit.term * 2 < current_half_year
