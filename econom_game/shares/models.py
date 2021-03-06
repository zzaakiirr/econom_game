from django.db import models
from teams.models import Team


class ShareRate(models.Model):
    sell_price = models.FloatField()
    buy_price = models.FloatField()
    half_year = models.PositiveIntegerField(default=1)

    def __str__(self):
        return 'share_rate_%d' % self.id


class ShareType(models.Model):
    name = models.CharField(max_length=30, unique=True)
    amount = models.FloatField()
    stock_price = models.ManyToManyField(ShareRate, related_name='share_type')

    def __str__(self):
        return 'shareholder_%d' % self.id


class ShareDeal(models.Model):
    team = models.ForeignKey(Team)
    share_type = models.ForeignKey(ShareType, related_name='share_deal')
    amount = models.FloatField(default=0)

    def __str__(self):
        return 'deal_%d' % self.id
