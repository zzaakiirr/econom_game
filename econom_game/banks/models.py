from django.db import models


class Bank(models.Model):
    name = models.CharField(max_length=30, unique=True)
    deposit = models.FloatField()
    credit_for_one_year = models.FloatField()
    credit_for_two_years = models.FloatField()

    def __str__(self):
        return 'bank_%d' % self.id
