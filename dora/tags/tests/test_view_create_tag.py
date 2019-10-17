from django.test import TestCase
from django.urls import resolve, reverse
from django.contrib.auth.models import User
from django.forms import ModelForm

from tags.models import Tag
from tags.views import TagCreateView
from flashcard.models import Entry, Deck


class TagCreateTestCase(TestCase):
    def setUp(self) -> None:
        self.username = 'jane'
        self.password = 'doe_123'
        user = User.objects.create_user(username=self.username, password=self.password, email='jane@doe.com')
        self.create_url = reverse('create_tag')


class LoggedInUserTagCreateTests(TagCreateTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.create_url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_class(self):
        view = resolve(self.create_url)
        self.assertEquals(view.func.view_class, TagCreateView)

    def test_csrf_token(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, ModelForm)


class SuccessfulTagCreateTests(TagCreateTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.create_url, data={'name': 'testTag'})

    def test_redirection(self):
        list_url = reverse('list_tags')
        self.assertRedirects(self.response, list_url)

    def test_create_tag(self):
        self.assertEquals(Tag.objects.count(), 1)


class AnonymousUserTagCreateTests(TestCase):

    def setUp(self) -> None:
        self.create_url = reverse('create_tag')
        self.response = self.client.get(self.create_url)

    def test_redirection(self):
        login_url = reverse('login')
        self.assertRedirects(self.response, f'{login_url}?next={self.create_url}')
