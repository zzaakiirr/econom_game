from django.contrib import admin
from .models import Station


class StationAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Station, StationAdmin)
