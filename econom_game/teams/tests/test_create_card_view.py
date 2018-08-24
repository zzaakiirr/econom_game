from django.urls import reverse, resolve
from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import Card

from ..views import create_card


User = get_user_model()


class SuperUserTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_superuser(
            email='test',
            password='test',
        )
        self.client.force_login(user)


class CreateCardTest(SuperUserTestCase):
    def setUp(self):
        super().setUp()
        url = (
            "%s?id=999&cvv=999&money_amount=999" %
            reverse("create_card")
        )
        self.response = self.client.get(url)
        self.card = Card.objects.get(id=999)

    def test_create_team_view_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_create_card_url_resolves_create_card_view(self):
        view = resolve('/api/v1/create_card/')
        self.assertEquals(view.func, create_card)

    def test_create_card_add_card_to_database(self):
        self.assertTrue(self.card._state.db)

    def test_create_card_return_correct_data(self):
        if self.card._state.db:
            expected_data = {"status": True}
        else:
            expected_data = {"status": False}

        response_content = str(self.response.content, encoding='utf8')
        self.assertJSONEqual(response_content, expected_data)
