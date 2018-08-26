from django.db import models


class Card(models.Model):
    id = models.PositiveIntegerField(primary_key=True, unique=True)
    card_number = models.CharField(max_length=25, unique=True)
    chip_number = models.CharField(max_length=25, unique=True)
    money_amount = models.PositiveIntegerField()

    def __str__(self):
        return 'card_%d' % self.id
