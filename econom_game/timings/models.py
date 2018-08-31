from django.db import models


class Timing(models.Model):
    game_start_time = models.TimeField()
    current_half_year = models.PositiveIntegerField(default=0)
    game_started = models.BooleanField(default=False)
