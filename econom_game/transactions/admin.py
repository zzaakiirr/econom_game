from django.contrib import admin
from .models import Transaction


class TransactionAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Transaction, TransactionAdmin)
