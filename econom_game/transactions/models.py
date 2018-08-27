from django.db import models

from teams.models import Team
from stations.models import Station


class Transaction(models.Model):
    id = models.PositiveIntegerField(primary_key=True, unique=True)
    sender = models.PositiveIntegerField()
    recipient = models.PositiveIntegerField()
    amount = models.PositiveIntegerField()
    victory = models.BooleanField(default=False)
    processed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.victory:
            self.processing = True
        else:
            self.processing = False
        super(Transaction, self).save(*args, **kwargs)

    def __str__(self):
        return 'transaction_%d' % self.id
