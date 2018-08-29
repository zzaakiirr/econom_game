from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^api/v1/make_transaction/$',
        views.make_transaction,
        name='make_transaction'
    ),
    url(
        r'^api/v1/confirm_transaction/$',
        views.confirm_transaction,
        name='confirm_transaction'
    ),
]
