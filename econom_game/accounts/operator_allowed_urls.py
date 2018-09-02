from django.conf.urls import include, url

from accounts.views import index_view


urlpatterns = [
    url(r"^admin/deposit/$", index_view, name='view_deposit'),
    url(r"^admin/credit/$", index_view, name='view_credit'),
]
