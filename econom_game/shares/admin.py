from django.contrib import admin

from .models import ShareRate, ShareType, ShareDeal


class ShareAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(ShareRate, ShareAdmin)
admin.site.register(ShareType)
admin.site.register(ShareDeal)
