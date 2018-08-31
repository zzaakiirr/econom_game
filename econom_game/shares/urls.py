from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^api/v1/exchange_rates/$',
        views.exchange_rates,
        name='exchange_rates'
    ),
    url(
        r'^api/v1/sell_share/$',
        views.sell_share,
        name='sell_share'
    ),
    url(
        r'^api/v1/buy_share/$',
        views.buy_share,
        name='buy_share'
    ),
    url(
        r'^api/v1/share_info/$',
        views.share_info,
        name='share_info'
    ),
]
