from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from flashcard.views import home, lang_entry, add_entry
from flashcard.models import Entry
from flashcard.forms import NewEntryForm


class HomeTests(TestCase):
    def test_home_view_status_code(self):
        url = reverse('home')  # this is the 'name' field in the urls.py for a url
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)


class EntryPageTests(TestCase):

    def setUp(self):
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        Entry.objects.create(from_lang='english',
                             to_lang='german',
                             from_word='hot',
                             to_word='heiß',
                             from_example='Der Kuchen ist heiß',
                             created_by=user
                             )

    def test_lang_entry_view_success_status_code(self):
        url = reverse('lang_entry', kwargs={'from_lang':'english'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)


    def test_entry_url_resolves_lang_entry_view(self):
        view = resolve('/entry/english/')
        self.assertEquals(view.func, lang_entry)


class EntryFormTests(TestCase):

    def test_entry_form_url_resolves_add_entry_view(self):
        view = resolve('/entry/add/')
        self.assertEquals(view.func, add_entry)


    def test_add_entry_view_status_code(self):
        url = reverse('add_entry')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_contains_form(self):
        url = reverse('add_entry')
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewEntryForm)


