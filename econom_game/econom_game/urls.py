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
from django.contrib.auth import views as auth_views

from accounts import views as accounts_views
from teams import views as teams_views
from stations import views as stations_views
from transactions import views as transactions_views


urlpatterns = [
    url(r'^login/$', accounts_views.login_user, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^admin/', admin.site.urls),
    url(
        r'^api/v1/get_all_teams/$',
        teams_views.ListTeamsView.as_view(),
        name='all_teams'
    ),
    url(
        r'^api/v1/get_all_stations/$',
        stations_views.ListStationsView.as_view(),
        name='all_stations'
    ),
    url(
        r'^api/v1/create_station/$',
        stations_views.create_station,
        name='create_station'
    ),
    url(
        r'^api/v1/create_team/$',
        teams_views.create_team,
        name='create_team'
    ),
    url(
        r'^api/v1/create_card/$',
        teams_views.create_card,
        name='create_card'
    ),
    url(
        r'^api/v1/make_transaction/$',
        transactions_views.make_transaction,
        name='make_transaction'
    )
]
