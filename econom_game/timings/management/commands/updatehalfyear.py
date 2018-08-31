from django.core.management.base import BaseCommand, CommandError
from timings.models import Timing


class Command(BaseCommand):
    help = 'Update current half year in game relative to game start time'

    def handle(self, *args, **options):
        try:
            timing = Timing.objects.get(id=1)
        except ObjectDoesNotExist:
            raise CommandError("No Timing object")
        if not timing.game_started:
            raise CommandError("Game not started")
        timing.current_half_year += 1
        timing.save()
