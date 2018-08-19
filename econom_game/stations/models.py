from django.db import models


class Station(models.Model):
    id = models.PositiveIntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=30)
    owner = models.CharField(max_length=30, default=None)

    LOW = 2
    NORMAL = 2.5
    HIGH = 3
    COMPLEXITY_CHOICES = (
        (LOW, 'Low'),
        (NORMAL, 'Normal'),
        (HIGH, 'High'),
    )

    complexity = models.PositiveIntegerField(choices=COMPLEXITY_CHOICES)
    min_bet = models.PositiveIntegerField()
    max_bet = models.PositiveIntegerField()

    def __str__(self):
        return self.name
