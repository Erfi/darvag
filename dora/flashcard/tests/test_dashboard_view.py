from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from flashcard.views import DeckListView


class AnonymousUserDashboardTests(TestCase):

    def test_dashboard_url_resolves_dashboard_view(self):
        view = resolve('/user/dashboard/')
        self.assertEquals(view.func.view_class, DeckListView)

    def test_dashboard_view_status_code(self):
        url = reverse('dashboard')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)


class LoggedInUserDashboardTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='jane', email='jane@doe.come', password='doe_123')
        self.client.login(username='jane', password='doe_123')

    def test_dashboard_url_resolves_dashboard_view(self):
        view = resolve('/user/dashboard/')
        self.assertEquals(view.func.view_class, DeckListView)

    def test_dashboard_view_status_code(self):
        url = reverse('dashboard')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
