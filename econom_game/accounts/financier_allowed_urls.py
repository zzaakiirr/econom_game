from django.conf.urls import include, url

from accounts.views import index_view


urlpatterns = [
    url(r"^admin/shares/$", index_view, name='view_shares'),
]
