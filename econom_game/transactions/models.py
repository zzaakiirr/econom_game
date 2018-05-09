from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Transaction(models.Model):
    id = models.PositiveIntegerField(primary_key=True, unique=True)

    sender_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        default=None)
    sender_id = models.PositiveIntegerField(default=None)
    sender = GenericForeignKey('sender_type', 'sender_id')

    amount = models.PositiveIntegerField()
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
