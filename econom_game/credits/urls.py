from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^api/v1/take_credit/$',
        views.take_credit,
        name='take_credit'
    ),
    url(
        r'^api/v1/get_credit_info/$',
        views.get_credit_info,
        name='get_credit_info'
    ),
]
