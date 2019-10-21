from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse, resolve

from flashcard.models import Deck, Entry
from flashcard.views import EntryListView
from tags.models import Tag
from tags.forms import TagFilterForm


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
                                           to_word='no', from_example='leider nein', created_by=self.user,
                                           deck=self.deck)
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

    def test_csrf_token(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, TagFilterForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 3)

    def test_listed_entries_no_filter(self):
        """
        All (two) entries should be there
        """
        entries = self.response.context.get('entries')
        self.assertEquals(entries.count(), 2)


class TagFilterPostRequestTests(TagFilterTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.list_entries_url, data={'tag1': True})

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_listed_entries(self):
        """
        Only one entry with 'tag1' should be there
        """
        entries = self.response.context.get('entries')
        self.assertEquals(entries.count(), 1)

    def test_empty_filter_listed_entries(self):
        """
        Pressing the filter button with no tag selected
        should show all (two) the entries
        """
        self.response = self.client.post(self.list_entries_url, data={})
        entries = self.response.context.get('entries')
        self.assertEquals(entries.count(), 2)


class MultipleUsersTagFilterTests(TagFilterTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.username2 = 'jane'
        self.password2 = 'doe_123'
        self.user2 = User.objects.create_user(username=self.username2, password=self.password2, email='jane@doe.com')
        self.tag3 = Tag.objects.create(name='tag1', created_by=self.user2)  # similar tag as the user1
        self.tag4 = Tag.objects.create(name='tag4', created_by=self.user2)
        self.deck2 = Deck.objects.create(from_lang='german', to_lang='english', created_by=self.user2)
        self.entry3 = Entry.objects.create(from_lang=self.deck2.from_lang, to_lang=self.deck2.to_lang, from_word='ja',
                                           to_word='yes', from_example='ja genau', created_by=self.user2,
                                           deck=self.deck2)
        self.entry3.tags.add(self.tag3)

        self.client.login(username=self.username, password=self.password)  # log in as user 1

    def test_tags_shown(self):
        """
        only user's tags should be shown (not all tags in the db)
        """
        response = self.client.get(self.list_entries_url)
        form = response.context.get('form')
        self.assertEquals(len(form.fields), 2)

    def test_multiple_users_with_same_tag_filter(self):
        """
        If two users create two identical tags (same tag name), this should not
        pose any problems when using the filter.
        """
        response = self.client.post(self.list_entries_url, data={'tag1': True})
        self.assertEquals(response.status_code, 200)
        entries = response.context.get('entries')
        self.assertEquals(entries.count(), 1)
