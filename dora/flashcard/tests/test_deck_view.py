from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from flashcard.views import DeckCreateView
from flashcard.forms import CreateDeckForm
from flashcard.models import Deck


class DeckFormTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='jane', email='jane@doe.come', password='doe_123')
        self.client.login(username='jane', password='doe_123')
        url = reverse('add_deck')
        self.response = self.client.get(url)

    def test_add_deck_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_add_deck_url_resolves_add_deck_view(self):
        view = resolve('/deck/add/')
        self.assertEquals(view.func.view_class, DeckCreateView)

    def test_contains_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, CreateDeckForm)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_form_inputs(self):
        """
        The view must contain three inputs: csrf, from_lang, to_lang
        """
        self.assertContains(self.response, '<input', 3)
        self.assertContains(self.response, 'type="text"', 2)


class SuccessfulDeckCreationTests(TestCase):
    def setUp(self):
        User.objects.create_user(username='jane', email='jane@doe.come', password='doe_123')
        self.client.login(username='jane', password='doe_123')
        url = reverse('add_deck')
        data = {'from_lang': 'farsi',
                'to_lang': 'english'}
        self.response = self.client.post(url, data)

    def test_successful_deck_creation_redirects_to_dashboard(self):
        dashboard_url = reverse('dashboard')
        self.assertRedirects(self.response, dashboard_url)

    def test_deck_creation(self):
        self.assertEquals(Deck.objects.count(), 1)
