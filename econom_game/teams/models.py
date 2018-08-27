from django.db import models


class Team(models.Model):
    id = models.PositiveIntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=25, unique=True)
    owner = models.CharField(max_length=25)
    faculty = models.CharField(max_length=25)
    group = models.CharField(max_length=25)
    bank = models.PositiveIntegerField()
    card = models.CharField(max_length=25, unique=True)
    card_type = models.CharField(max_length=25)

    def __str__(self):
        return self.name
