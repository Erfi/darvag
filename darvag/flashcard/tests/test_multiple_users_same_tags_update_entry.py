from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from tags.models import Tag
from flashcard.models import Deck, Entry


class MultipleUsersEntryUpdateViewTestCase(TestCase):
    def setUp(self) -> None:
        self.username1 = 'john'
        self.password1 = 'smith_123'
        self.email1 = 'john@smith.com'
        self.username2 = 'jane'
        self.password2 = 'doe_123'
        self.email2 = 'jane@doe.com'
        self.user1 = User.objects.create_user(username=self.username1, password=self.password1, email=self.email1)
        self.user2 = User.objects.create_user(username=self.username2, password=self.password2, email=self.email2)
        self.tag1 = Tag.objects.create(name='tagname', created_by=self.user1)
        self.tag2 = Tag.objects.create(name='tagname', created_by=self.user2)  # same tag name as user1's

        self.deck1 = Deck.objects.create(name='deck1', created_by=self.user1)
        self.entry1 = Entry.objects.create(from_word='ja',
                                           to_word='yes', created_by=self.user1, deck=self.deck1)

        self.update_entry_url = reverse('edit_entry', kwargs={'entry_id': self.entry1.id, 'deck_id': self.deck1.id})

    def test_add_same_tag_as_other_user(self):
        self.client.login(username=self.username1, password=self.password1)
        response = self.client.post(self.update_entry_url, data={'from_word': 'crazy',
                                                                 'to_word': 'divooneh',
                                                                 'deck': self.deck1.id,
                                                                 'from_example': 'kholi?',
                                                                 'tags': [self.tag1.id]})
        self.entry1.refresh_from_db()
        self.assertEquals(self.entry1.tags.count(), 1)
