from django import forms
from flashcard.models import Deck, Entry


# --- customizations ---
class EntryModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, deck):
        return deck.name


class EntryModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, tag):
        return tag.name


# ----------------------


class CreateEntryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        tags = kwargs.pop('tag_queryset', None)
        decks = kwargs.pop('deck_queryset', None)
        super().__init__(*args, **kwargs)
        self.fields['tags'] = EntryModelMultipleChoiceField(queryset=tags, widget=forms.SelectMultiple, required=False)
        self.fields['deck'] = EntryModelChoiceField(queryset=decks, widget=forms.Select, required=True)

    class Meta:
        model = Entry
        fields = ['from_word', 'to_word', 'from_example', 'deck', 'tags']


class UpdateEntryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        tags = kwargs.pop('tag_queryset', None)
        decks = kwargs.pop('deck_queryset', None)
        super().__init__(*args, **kwargs)
        self.fields['tags'] = EntryModelMultipleChoiceField(queryset=tags, widget=forms.SelectMultiple, required=False)
        self.fields['deck'] = EntryModelChoiceField(queryset=decks, widget=forms.Select, required=True)

    class Meta:
        model = Entry
        fields = ['from_word', 'to_word', 'from_example', 'deck', 'tags']
