from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse, resolve

from flashcard.models import Deck, Entry
from flashcard.views import EntryListView
from tags.models import Tag
from tags.forms import TagFilterForm

from time import sleep


class TagFilterTestCase(TestCase):
    def setUp(self) -> None:
        self.username = 'john'
        self.password = 'smith_123'
        self.user = User.objects.create_user(username=self.username, password=self.password, email='john@smith.com')
        self.tag1 = Tag.objects.create(name='tag1', created_by=self.user)
        self.tag2 = Tag.objects.create(name='tag2', created_by=self.user)
        self.deck = Deck.objects.create(from_lang='german', to_lang='english', created_by=self.user)
        self.entry1 = Entry.objects.create(from_lang=self.deck.from_lang, to_lang=self.deck.to_lang, from_word='ja',
                                           to_word='yes', from_example='ja genau', created_by=self.user, deck=self.deck)
        self.entry1.tags.add(self.tag1)
        self.entry2 = Entry.objects.create(from_lang=self.deck.from_lang, to_lang=self.deck.to_lang, from_word='nein',
                                           to_word='no', from_example='leider nein', created_by=self.user, deck=self.deck)
        self.list_entries_url = reverse('view_deck', kwargs={'deck_id': self.deck.id})


class TagFilterGetRequestTests(TagFilterTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.list_entries_url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_class(self):
        view = resolve(self.list_entries_url)
        self.assertEquals(view.func.view_class, EntryListView)

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, TagFilterForm)

    def test_listed_entries_no_filter(self):
        entries = self.response.context.get('entries')
        self.assertEquals(entries.count(), 2)

class TagFilterPostRequestTests(TagFilterTestCase):
    pass
