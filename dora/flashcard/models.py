from django.db import models
from django.contrib.auth.models import User


class Deck(models.Model):
    from_lang = models.CharField(max_length=20)
    to_lang = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='decks')

    def __str__(self):
        return f'{self.from_lang}-->{self.to_lang}'


class Entry(models.Model):
    from_lang = models.CharField(max_length=45)
    to_lang = models.CharField(max_length=45)
    from_word = models.CharField(max_length=45)
    to_word = models.CharField(max_length=45)
    from_example = models.TextField(max_length=500)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='entries', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='entries')

    def __str__(self):
        return f'{self.from_word}-->{self.to_word} | by: {self.created_by}'
