from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^api/v1/make_transaction/$',
        views.make_transaction,
        name='make_transaction'
    ),
]
