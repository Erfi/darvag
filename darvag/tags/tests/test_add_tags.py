from django.test import TestCase
from django.contrib.auth.models import User

from flashcard.models import Deck, Entry
from tags.models import Tag


class TagAdditionTests(TestCase):
    def setUp(self) -> None:
        self.username = 'jane'
        self.password = 'doe_123'
        user = User.objects.create_user(username=self.username,
                                        email='jane@doe.com',
                                        password=self.password)
        self.tag1 = Tag.objects.create(created_by=user,
                                       name='tag1')

        self.tag2 = Tag.objects.create(created_by=user,
                                       name='tag2')

        self.deck = Deck.objects.create(created_by=user,
                                        name='deck')

        self.entry1 = Entry.objects.create(created_by=user,
                                           from_word='yes',
                                           to_word='bale',
                                           from_example='yes bale',
                                           deck=self.deck)

        self.entry2 = Entry.objects.create(created_by=user,
                                           from_word='no',
                                           to_word='na',
                                           from_example='no na',
                                           deck=self.deck)

    def test_tag_addition(self):
        self.entry1.tags.add(self.tag1)
        self.entry1.tags.add(self.tag2)
        self.assertEquals(self.entry1.tags.count(), 2)
        self.assertEquals(self.tag1.entries.count(), 1)
