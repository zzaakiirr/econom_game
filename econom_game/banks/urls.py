from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^api/v1/get_banks_list/$',
        views.get_banks_list,
        name='get_banks_list'
    ),
]
