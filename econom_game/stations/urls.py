from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^api/v1/create_station/$',
        views.create_station,
        name='create_station'
    ),
    url(
        r'^api/v1/make_bet/$',
        views.make_bet,
        name='make_bet'
    ),
    url(
        r'^api/v1/victory/$',
        views.victory,
        name='victory'
    ),
    url(
        r'^api/v1/get_station_info/$',
        views.get_station_info,
        name='get_station_info'
    ),
]
