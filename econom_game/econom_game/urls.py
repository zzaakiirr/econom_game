from django.conf.urls import include, url
from django.contrib import admin

from accounts import views as accounts_views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/get_menu', accounts_views.get_menu, name="get_menu"),
    url(r'', include('accounts.urls')),
    url(r'', include('teams.urls')),
    url(r'', include('stations.urls')),
    url(r'', include('banks.urls')),
    url(r'', include('cards.urls')),
    url(r'', include('transactions.urls')),

    url(r'', include('accounts.station_admin_allowed_urls')),
    url(r'', include('accounts.super_user_allowed_urls')),
]
