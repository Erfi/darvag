from django.test import TestCase
from django.urls import resolve, reverse
from django.contrib.auth.models import User
from django.forms import ModelForm

from tags.models import Tag
from tags.views import TagDeleteView


class TagDeleteTestCase(TestCase):
    def setUp(self) -> None:
        self.username = 'jane'
        self.password = 'doe_123'
        self.user = User.objects.create_user(username=self.username, password=self.password, email='jane@doe.com')
        self.tag = Tag.objects.create(name='test_tag', created_by=self.user)
        self.delete_url = reverse('delete_tag', kwargs={'tag_id': self.tag.id})


class AnonymousUserDeleteTagTests(TagDeleteTestCase):
    def test_redirection(self):
        login_url = reverse('login')
        response = self.client.get(self.delete_url)
        self.assertRedirects(response, f'{login_url}?next={self.delete_url}')


class UnauthorizedUserDeleteTagTests(TagDeleteTestCase):
    def setUp(self) -> None:
        super().setUp()
        user = User.objects.create_user(username='john',
                                        email='john@smith.com',
                                        password='smith_123')
        self.client.login(username='john', password='smith_123')
        self.response = self.client.get(self.delete_url)

    def test_status_code(self):
        """
        Deck can only be deleted by the owner.
        Unauthorized user should get a 404 error.
        """
        self.assertEquals(self.response.status_code, 404)


class LoggedInUserDeleteTagTests(TagDeleteTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.delete_url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_url_resolves_delete_view(self):
        view = resolve(self.delete_url)
        self.assertEquals(view.func.view_class, TagDeleteView)

    def test_csrf_token(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_inputs(self):
        """
        csrf-token and confirm button inputs
        """
        self.assertContains(self.response, '<input', 2)


class SuccessfulDeleteTagTests(TagDeleteTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.delete_url, data={})

    def test_redirect(self):
        redirect_url = reverse('list_tags')
        self.assertRedirects(self.response, redirect_url)

    def test_deck_deleted(self):
        self.assertEquals(Tag.objects.count(), 0)
