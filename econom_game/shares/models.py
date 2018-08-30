from django.db import models
from teams.models import Team


class ShareRate(models.Model):
    sell_price = models.FloatField()
    buy_price = models.FloatField()
    term = models.PositiveIntegerField()


class ShareType(models.Model):
    name = models.CharField(max_length=30, unique=True)
    amount = models.FloatField()
    stock_price = models.ManyToManyField(ShareRate, related_name='share_type')

    def __str__(self):
        return 'shareholder_%d' % self.id


class ShareDeal(models.Model):
    team = models.ForeignKey(Team)
    sharetype = models.ForeignKey(ShareType)
    amount = models.FloatField()
    price = models.FloatField()
    action = models.Charfield(choices=('BUY', 'SELL'))

    def __str__(self):
        return 'deal%d' % self.id
