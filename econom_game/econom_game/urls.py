from django.conf.urls import include, url
from django.contrib import admin

from accounts import views as accounts_views


urlpatterns = [
    url(r'^django_admin/', admin.site.urls),
    url(r'', include('accounts.urls')),
    url(r'', include('teams.urls')),
    url(r'', include('stations.urls')),
    url(r'', include('banks.urls')),
    url(r'', include('cards.urls')),
    url(r'', include('credits.urls')),
    url(r'', include('deposits.urls')),
    url(r'', include('shares.urls')),
    url(r'', include('transactions.urls')),

    url(r'', include('accounts.super_user_allowed_urls')),
    url(r'', include('accounts.station_admin_allowed_urls')),
    url(r'', include('accounts.operator_allowed_urls')),
    url(r'', include('accounts.financier_allowed_urls')),
]

urlpatterns += [
    url(r'^.*/$', accounts_views.index_view, name='index_view'),
]
