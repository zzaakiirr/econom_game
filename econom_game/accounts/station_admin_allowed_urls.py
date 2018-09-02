from django.conf.urls import include, url

from accounts.views import index_view


urlpatterns = [
    url(r"^admin/station/$", index_view, name='view_station'),
]
