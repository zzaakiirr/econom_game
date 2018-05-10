from django.contrib import admin
from stations.models import Station
from teams.models import Team, Card
from transactions.models import Transaction


admin.site.register(Station)
admin.site.register(Team)
admin.site.register(Card)
admin.site.register(Transaction)
