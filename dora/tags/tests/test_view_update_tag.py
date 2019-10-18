from django.forms import ModelForm
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve

from tags.models import Tag
from tags.views import TagUpdateView


class TagUpdateViewTestCase(TestCase):
    def setUp(self) -> None:
        self.username = 'jane'
        self.password = 'doe_123'
        self.email = 'jane@doe.com'
        self.user = User.objects.create_user(username=self.username,
                                             email=self.email,
                                             password=self.password)
        self.tag = Tag.objects.create(name='test_tag', created_by=self.user)
        self.update_url = reverse('update_tag', kwargs={'tag_id': self.tag.id})


class AnonymousUserTagUpdateViewTests(TagUpdateViewTestCase):
    def test_redirection(self):
        response = self.client.get(self.update_url)
        login_url = reverse('login')
        self.assertRedirects(response, f'{login_url}?next={self.update_url}')


class UnauthorizedUserTagUpdateViewTests(TagUpdateViewTestCase):
    def setUp(self) -> None:
        super().setUp()
        username = 'bla'
        password = 'foo123'
        user = User.objects.create_user(username=username, password=password)
        self.client.login(username=username, password=password)
        self.response = self.client.get(self.update_url)

    def test_status_code(self):
        """
        Only the owner should be able to update a tag
        """
        self.assertEquals(self.response.status_code, 404)


class TagUpdateViewTests(TagUpdateViewTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.update_url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_class(self):
        view = resolve(self.update_url)
        self.assertEquals(view.func.view_class, TagUpdateView)

    def test_csrf_token(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, ModelForm)

    def test_form_inputs(self):
        """
        2 inputs: csrf token and name field
        """
        self.assertContains(self.response, '<input', 2)


class SuccessfulTagUpdateViewTests(TagUpdateViewTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.update_url, data={'name': 'test_tag_modified'})

    def test_redirection(self):
        tag_list_url = reverse('list_tags')
        self.assertRedirects(self.response, tag_list_url)

    def test_tag_updated(self):
        self.tag.refresh_from_db()
        self.assertEquals(self.tag.name, 'test_tag_modified')


class InvalidTagUpdateViewTests(TagUpdateViewTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.update_url, data={})

    def test_status_code(self):
        """
        Should stay on the same page
        """
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)
