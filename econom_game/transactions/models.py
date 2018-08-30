from django.db import models

from teams.models import Team
from stations.models import Station


class Transaction(models.Model):
    sender = models.ForeignKey(
        Team, related_name='transaction_sender', default=None
    )
    recipient = models.ForeignKey(
        Station, related_name='transaction_recipient', default=None
    )
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
