from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^api/v1/take_credit/$',
        views.take_credit,
        name='take_credit'
    ),
]
