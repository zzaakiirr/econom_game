from django.db import models


class Transaction(models.Model):
    id = models.PositiveIntegerField(primary_key=True, unique=True)

    # TO FIX: Use GenericForeignKey
    # sender =
    # recipient =

    amount = models.PositiveIntegerField()
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id
