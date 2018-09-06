from django.contrib import admin

from .models import Deposit


class DepositAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'last_change')

admin.site.register(Deposit, DepositAdmin)
