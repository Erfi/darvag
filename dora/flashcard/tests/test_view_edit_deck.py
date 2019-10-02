from django.forms import ModelForm
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve

from flashcard.models import Deck, Entry
from flashcard.views import DeckUpdateView


class DeckUpdateViewTestCase(TestCase):
    """
    Base testcase to be used for all 'DeckUpdateView' view tests
    """

    def setUp(self) -> None:
        self.username = 'jane'
        self.password = 'doe_123'
        self.email = 'jane@doe.com'
        user = User.objects.create_user(username=self.username,
                                        email=self.email,
                                        password=self.password)
        self.deck = Deck(from_lang='kazaki', to_lang='baloochi', created_by=user)
        self.deck.save()
        self.url = reverse('edit_deck', kwargs={'deck_id': self.deck.id})


class LoginRequiredDeckUpdateViewTests(DeckUpdateViewTestCase):
    def test_redirection(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, f'{login_url}?next={self.url}')


class UnauthorizedDeckUpdateViewTests(DeckUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        username = 'kane'
        password = '321'
        user = User.objects.create_user(username=username, email='kane@doe.com', password=password)
        self.client.login(username=username, password=password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        """
        A deck should be edited only by the owener.
        Unautorized user should get a 404 response.
        """
        self.assertEquals(self.response.status_code, 404)


class DeckUpdateViewTests(DeckUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_class(self):
        view = resolve('/deck/1/edit/')
        self.assertEquals(view.func.view_class, DeckUpdateView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, ModelForm)

    def test_form_inputs(self):
        """
        The view must contain three inputs: csrf, from_lang, to_lang
        """
        self.assertContains(self.response, '<input', 3)


class SuccessfulDeckUpdateViewTests(DeckUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {'from_lang': 'narnian', 'to_lang': self.deck.to_lang})

    def test_redirection(self):
        """
        A valid form submission should redirect the user to dashboard
        """
        dashboard_url = reverse('dashboard')
        self.assertRedirects(self.response, dashboard_url)

    def test_post_changed(self):
        self.deck.refresh_from_db()
        self.assertEquals(self.deck.from_lang, 'narnian')


class InvalidDeckUpdateViewTests(DeckUpdateViewTestCase):
    def setUp(self):
        """
        Submit an empty dictionary to the `edit_deck` view
        """
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {})

    def test_status_code(self):
        """
        An invalid form submission should return to the same page
        """
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)
