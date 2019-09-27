from django import forms
from flashcard.models import Deck, Entry


class NewEntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['from_word', 'to_word', 'from_example']


class NewDeckForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ['from_lang', 'to_lang']
