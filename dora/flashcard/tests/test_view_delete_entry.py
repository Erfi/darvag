from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse, resolve

from flashcard.models import Deck, Entry
from flashcard.views import EntryDeleteView


class DeleteEntryTestCase(TestCase):
    def setUp(self) -> None:
        self.username = 'jane'
        self.password = 'doe_123'
        self.user = User.objects.create_user(username=self.username,
                                             email='jane@doe.com',
                                             password=self.password)
        self.deck = Deck.objects.create(created_by=self.user,
                                        from_lang='farsi',
                                        to_lang='english')
        self.entry = Entry.objects.create(created_by=self.user,
                                          from_lang=self.deck.from_lang,
                                          to_lang=self.deck.to_lang,
                                          from_example='this is an example',
                                          deck=self.deck)
        self.url = reverse('delete_entry', kwargs={'deck_id': self.deck.id, 'entry_id': self.entry.id})


class AnonymousUserDeleteEntryTests(DeleteEntryTestCase):
    def test_redirection(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, f'{login_url}?next={self.url}')


class UnauthorizedUserDeleteEntryTests(DeleteEntryTestCase):
    def setUp(self) -> None:
        super().setUp()
        user = User.objects.create_user(username='john',
                                        email='john@smith.com',
                                        password='smith_123')
        self.client.login(username='john', password='smith_123')
        self.response = self.client.get(self.url)

    def test_status_code(self):
        """
        Deck can only be deleted by the owner.
        Unauthorized user should get a 404 error.
        """
        self.assertEquals(self.response.status_code, 404)


class LoggedInUserDeleteEntryTests(DeleteEntryTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_url_resolves_delete_view(self):
        view = resolve(self.url)
        self.assertEquals(view.func.view_class, EntryDeleteView)

    def test_csrf_token(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_inputs(self):
        """
        csrf-token and confirm button inputs
        """
        self.assertContains(self.response, '<input', 2)


class SuccessfulDeleteEntryTests(DeleteEntryTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, data={})

    def test_redirect(self):
        redirect_url = reverse('view_deck', kwargs={'deck_id':self.deck.id})
        self.assertRedirects(self.response, redirect_url)

    def test_deck_deleted(self):
        self.assertEquals(Entry.objects.count(), 0)
