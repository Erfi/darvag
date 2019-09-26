from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from flashcard.views import add_deck
from flashcard.forms import NewDeckForm


class DeckViewTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='jane', email='jane@doe.come', password='doe_123')
        self.client.login(username='jane', password='doe_123')
        url = reverse('add_deck')
        self.response = self.client.get(url)

    def test_add_deck_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_add_deck_url_resolves_add_deck_view(self):
        view = resolve('/deck/add/')
        self.assertEquals(view.func, add_deck)

    def test_contains_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, NewDeckForm)
