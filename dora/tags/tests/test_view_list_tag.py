from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User

from tags.views import TagListView


class TagListViewTestCase(TestCase):
    def setUp(self) -> None:
        self.username = 'john'
        self.password = 'doe'
        self.user = User.objects.create_user(username=self.username, password=self.password, email='john@doe.com')
        self.list_url = reverse('list_tags')


class AnonymousUserTagViewTests(TagListViewTestCase):

    def test_redirection(self):
        login_url = reverse('login')
        response = self.client.get(self.list_url)
        self.assertRedirects(response, f'{login_url}?next={self.list_url}')


class TagListViewTests(TagListViewTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.list_url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_class(self):
        view = resolve(self.list_url)
        self.assertEquals(view.func.view_class, TagListView)

