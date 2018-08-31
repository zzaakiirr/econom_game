from django.conf.urls import include, url

from .empty_view import empty_view


urlpatterns = [
    url(r"^admin/deposit/$", empty_view, name='view_deposit'),
    url(r"^admin/credit/$", empty_view, name='view_credit'),
]
