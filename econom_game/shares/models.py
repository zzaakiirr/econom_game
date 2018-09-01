from django.db import models
from teams.models import Team


class ShareRate(models.Model):
    sell_price = models.FloatField()
    buy_price = models.FloatField()
    half_year = models.PositiveIntegerField(default=1)


class ShareType(models.Model):
    name = models.CharField(max_length=30, unique=True)
    amount = models.FloatField()
    stock_price = models.ManyToManyField(ShareRate, related_name='sharetype')

    def __str__(self):
        return 'shareholder_%d' % self.id


class ShareDeal(models.Model):
    team = models.ForeignKey(Team)
    sharetype = models.ForeignKey(ShareType, related_name='share_deal')
    amount = models.FloatField(default=0)

    def __str__(self):
        return 'deal%d' % self.id
