from django.contrib import admin

from .models import Bank


class BankAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Bank, BankAdmin)
