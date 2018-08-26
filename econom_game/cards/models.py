from django.db import models


class Card(models.Model):
    id = models.PositiveIntegerField(primary_key=True, unique=True)
    card = models.CharField(max_length=25, unique=True)
    pay_pass = models.CharField(max_length=25, unique=True)
    money_amount = models.PositiveIntegerField()

    def __str__(self):
        return 'card_%d' % self.id
