from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('accounts.urls')),
    url(r'', include('teams.urls')),
    url(r'', include('stations.urls')),
    url(r'', include('transactions.urls')),
]
