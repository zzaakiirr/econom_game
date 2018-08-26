from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^api/v1/create_card/$',
        views.create_card,
        name='create_card'
    ),
]
