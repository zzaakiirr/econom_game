from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^api/v1/invest_money/$',
        views.invest_money,
        name='invest_money'
    ),
    url(
        r'^api/v1/get_deposit_info/$',
        views.get_deposit_info,
        name='get_deposit_info'
    ),
]
