from django.contrib import admin

from .models import Card


class CardAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Card, CardAdmin)
