from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^api/v1/create_team/$',
        views.create_team,
        name='create_team'
    ),
]
