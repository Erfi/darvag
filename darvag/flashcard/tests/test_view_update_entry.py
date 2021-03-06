from django.test import TestCase
from django.forms import ModelForm
from django.urls import resolve, reverse
from django.contrib.auth.models import User

from flashcard.models import Deck, Entry
from flashcard.views import EntryUpdateView


class EntryUpdateViewTestCase(TestCase):
    """
    Base testcase for all edit_entry tests
    """

    def setUp(self) -> None:
        self.username = 'jane'
        self.email = 'jane@doe.com'
        self.password = 'doe_123'
        self.user = User.objects.create_user(username=self.username,
                                             email=self.email,
                                             password=self.password)
        self.user.save()
        self.deck = Deck(name='deck', created_by=self.user)
        self.deck.save()
        self.entry = Entry(from_word='ja',
                           to_word='ja',
                           from_example='brah',
                           deck=self.deck,
                           created_by=self.user)
        self.entry.save()
        self.url = reverse('edit_entry', kwargs={'deck_id': self.deck.pk, 'entry_id': self.entry.pk})


class LoginRequiredEntryUpdateViewTests(EntryUpdateViewTestCase):
    def test_redirection(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, f'{login_url}?next={self.url}')


class UnauthorizedEntryUpdateViewTests(EntryUpdateViewTestCase):
    def setUp(self) -> None:
        super().setUp()
        user = User.objects.create_user(username='tokhmeh',
                                        email='tokhmeh@bodadeh.com',
                                        password='bodadeh_123')
        self.client.login(username='tokhmeh', password='bodadeh_123')
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 404)


class AuthorizedEntryUpdateViewTests(EntryUpdateViewTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_class(self):
        view = resolve(self.url)
        self.assertEquals(view.func.view_class, EntryUpdateView)

    def test_csrf_token(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contians_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, ModelForm)

    def test_form_inputs(self):
        """
        3 inputs: csrf, from_word, to_word
        1 textarea: from_example
        1 select: tags
        """
        self.assertContains(self.response, '<input', 3)
        self.assertContains(self.response, '<textarea', 1)
        self.assertContains(self.response, '<select', 2)


class SuccessfulEntryUpdateViewTests(EntryUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url,
                                         data={'from_word': 'gol', 'to_word': 'riz', 'deck': self.deck.id, 'example': 'brah'})

    def test_redirection(self):
        deck_view_url = reverse('view_deck', kwargs={'deck_id': self.deck.id})
        self.assertRedirects(self.response, deck_view_url)

    def test_entry_changed(self):
        self.entry.refresh_from_db()
        self.assertEquals(self.entry.from_word, 'gol')


class UnsuccessfulEntryUpdateViewTest(EntryUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, data={})

    def test_status_code(self):
        """
        should stay on the same page
        """
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context['form']
        self.assertTrue(form.errors)
