from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Transaction(models.Model):
    id = models.PositiveIntegerField(primary_key=True, unique=True)

    Team_or_Station = (
        models.Q(app_label='teams', model='team') |
        models.Q(app_label='stations', model='station')
    )

    sender_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE,
        default=None, related_name='sender',
        limit_choices_to=Team_or_Station,
    )

    sender_id = models.PositiveIntegerField(default=None)
    sender = GenericForeignKey('sender_type', 'sender_id')

    recipient_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE,
        default=None, related_name='recipient',
        limit_choices_to=Team_or_Station,
    )
    recipient_id = models.PositiveIntegerField(default=None)
    recipient = GenericForeignKey('recipient_type', 'recipient_id')

    amount = models.PositiveIntegerField()
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'transaction_%d' % self.id
