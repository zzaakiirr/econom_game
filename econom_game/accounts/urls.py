from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    url(r'^api/v1/get_menu/$', views.get_menu, name="get_menu"),
    url(r'^api/v1/login/$', views.login_user, name='login'),
    url(r'^api/v1/logout/$', views.logout_user, name='logout'),
    url(r'^api/v1/is_logged_in/$', views.is_logged_in, name='is_logged_in'),
]
