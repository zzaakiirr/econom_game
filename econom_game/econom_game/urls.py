"""econom_game URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from teams import views as teams_views
from stations import views as stations_views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(
        r'^api/m=get_all_teams/$',
        teams_views.ListTeamsView.as_view(),
        name='all_teams'
    ),
    url(
        r'^api/m=get_all_stations/$',
        stations_views.ListStationsView.as_view(),
        name='all_stations'
    ),
    url(
        r'^api/m=create_station/$',
        stations_views.create_station,
        name='create_station'
    ),
    url(
        r'^api/m=create_team/$',
        teams_views.create_team,
        name='create_team'
    ),
]
