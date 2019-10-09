from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from flashcard.views import home, EntryCreateView
from flashcard.models import Entry, Deck
from flashcard.forms import CreateEntryForm


class HomeTests(TestCase):
    def test_home_view_status_code(self):
        url = reverse('home')  # this is the 'name' field in the urls.py for a url
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)


class LoggedInUserEntryFormTests(TestCase):

    def setUp(self):
        user = User.objects.create_user(username='john',
                                        email='john@snow.com',
                                        password='snow_123')
        self.client.login(username='john', password='snow_123')
        self.deck = Deck.objects.create(from_lang='english', to_lang='spanish', created_by=user)
        self.deck.save()

    def test_entry_form_url_resolves_add_entry_view(self):
        view = resolve('/deck/{}/entry/add/'.format(self.deck.id))
        self.assertEquals(view.func.view_class, EntryCreateView)

    def test_add_entry_view_status_code(self):
        url = reverse('add_entry', kwargs={'deck_id': self.deck.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_contains_form(self):
        url = reverse('add_entry', kwargs={'deck_id': self.deck.id})
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, CreateEntryForm)


class AnonymousUserEntryFormTests(TestCase):

    def test_entry_form_url_resolves_home_view(self):
        view = resolve('/deck/1/entry/add/')
        self.assertEquals(view.func.view_class, EntryCreateView)

    def test_add_entry_view_status_code(self):
        url = reverse('add_entry', kwargs={'deck_id': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)
