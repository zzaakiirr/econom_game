from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^api/v1/get_all_stations/$',
        views.ListStationsView.as_view(),
        name='all_stations'
    ),
    url(
        r'^api/v1/create_station/$',
        views.create_station,
        name='create_station'
    ),
]
