from django.conf.urls import include, url

from .empty_view import empty_view


urlpatterns = [
    url(
        r'^admin/add_station/$',
        empty_view,
        name='add_station'
    ),
    url(
        r'^admin/add_group/$',
        empty_view,
        name='add_group'
    ),
    url(
        r'^admin/shares/$',
        empty_view,
        name='view_shares'
    ),
    url(
        r'^admin/give_money/$',
        empty_view,
        name='give_money'
    ),
    url(
        r'^admin/confirm_transaction/$',
        empty_view,
        name='confirm_transaction'
    ),
    url(
        r'^admin/exclude_money/$',
        empty_view,
        name='exclude_money'
    ),
]
