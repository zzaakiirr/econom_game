from django.conf.urls import include, url
from django.contrib import admin

from .empty_view import empty_view


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/get_menu', accounts_views.get_menu, name="get_menu"),
    url(r'', include('accounts.urls')),
    url(r'', include('teams.urls')),
    url(r'', include('stations.urls')),
    url(r'', include('transactions.urls')),

    url(r'^station/$', empty_view, name="station"),
]
