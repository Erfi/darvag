from django.db import models
from django.contrib.auth.models import User
from django.utils.html import mark_safe
from markdown import markdown
from tags.models import Tag


class Deck(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='decks')

    def get_entry_count(self):
        return self.entries.count()

    def __str__(self):
        return f'{self.name} | by: {self.created_by}'


class Entry(models.Model):
    from_word = models.CharField(max_length=45)
    to_word = models.CharField(max_length=45)
    from_example = models.TextField(max_length=2000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='entries')
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='entries', blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name='entries')

    def get_from_example_as_markdown(self):
        return mark_safe(markdown(self.from_example, extensions=['tables'], safe_mode='escape'))

    def __str__(self):
        return f'{self.from_word}-->{self.to_word} | by: {self.created_by}'
