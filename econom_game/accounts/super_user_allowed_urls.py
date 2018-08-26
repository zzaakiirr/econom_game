from django.conf.urls import include, url

from .empty_view import empty_view


urlpatterns = [
    url(
        r'^admin/add_station/$',
        empty_view,
        name='add_station'
    ),
    url(
        r'^admin/add_team/$',
        empty_view,
        name='add_team'
    ),
    url(
        r'^admin/shares_list/$',
        empty_view,
        name='view_shares_list'
    ),
    url(
        r'^admin/confirm_transaction/$',
        empty_view,
        name='confirm_transaction'
    ),
    url(
        r'^admin/shadow_economy/$',
        empty_view,
        name='view_shadow_economy'
    ),
    url(
        r'^admin/station_transactions/$',
        empty_view,
        name='view_station_transactions'
    ),
    url(
        r'^admin/debit_list/$',
        empty_view,
        name='view_debit_list'
    ),
    url(
        r'^admin/credit_list/$',
        empty_view,
        name='view_credit_list'
    ),
    url(
        r'^admin/start/$',
        empty_view,
        name='view_start'
    ),
]
