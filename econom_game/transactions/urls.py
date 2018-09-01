from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^api/v1/confirm_transaction/$',
        views.confirm_transaction,
        name='confirm_transaction'
    ),
    url(
        r'^api/v1/give_money/$',
        views.give_money,
        name='give_money'
    ),
    url(
        r'^api/v1/exclude_money/$',
        views.exclude_money,
        name='exclude_money'
    ),
]
