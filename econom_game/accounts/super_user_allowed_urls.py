from django.conf.urls import include, url

from accounts.views import index_view


urlpatterns = [
    url(
        r'^admin/add_station/$',
        index_view,
        name='add_station'
    ),
    url(
        r'^admin/add_group/$',
        index_view,
        name='add_group'
    ),
    url(
        r'^admin/shares/$',
        index_view,
        name='view_shares'
    ),
    url(
        r'^admin/give_money/$',
        index_view,
        name='give_money'
    ),
    url(
        r'^admin/confirm_transaction/$',
        index_view,
        name='confirm_transaction'
    ),
    url(
        r'^admin/exclude_money/$',
        index_view,
        name='exclude_money'
    ),
]
