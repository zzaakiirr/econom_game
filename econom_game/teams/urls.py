from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^api/v1/get_all_teams/$',
        views.ListTeamsView.as_view(),
        name='all_teams'
    ),
    url(
        r'^api/v1/create_team/$',
        views.create_team,
        name='create_team'
    ),
    url(
        r'^api/v1/create_card/$',
        views.create_card,
        name='create_card'
    ),
]
