from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist

from timings.models import Timing


class Command(BaseCommand):
    help = 'Increase current half year in game relative to game start time'

    def handle(self, *args, **options):
        timing = get_timing()
        if not timing.game_started:
            raise CommandError("Game not started")
        timing.current_half_year += 1
        timing.save()


def get_timing():
    try:
        timing = Timing.objects.get(id=1)
    except ObjectDoesNotExist:
        raise CommandError("No Timing object")
    return timing
