from django.test import TestCase
from django.urls import reverse, resolve
import json

from shares.views import get_exchange_rates


class ExchangeRatesTests(TestCase):
    def test_exchange_rates_url_resolves_exchange_rates_view(self):
        view = resolve('/api/v1/get_exchange_rates/')
        self.assertEquals(view.func, get_exchange_rates)
