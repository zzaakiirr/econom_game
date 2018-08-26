from django.conf.urls import include, url

from .empty_view import empty_view


urlpatterns = [
    url(r"^admin/station/$", empty_view, name='view_station'),
]
