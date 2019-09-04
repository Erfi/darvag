from django import forms
from flashcard.models import Entry


class NewEntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['from_lang', 'to_lang', 'from_word', 'to_word', 'from_example']


