from django.contrib import admin

from .models import Credit


class CreditAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Credit, CreditAdmin)
