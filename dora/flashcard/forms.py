from django import forms
from flashcard.models import Deck, Entry


class NewEntryForm(forms.ModelForm):
    def __init__(self, *args, tags_queryset, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'] = forms.MultipleChoiceField(choices=self.created_choices_from_tag_queryset(tags_queryset),
                                                        widget=forms.SelectMultiple, required=False)

    def created_choices_from_tag_queryset(self, tag_queryset):
        return [(tag, tag.name) for tag in tag_queryset]

    class Meta:
        model = Entry
        fields = ['from_word', 'to_word', 'from_example', 'tags']


class EditEntryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        tags = self.created_choices_from_tag_queryset(kwargs['tag_queryset'])
        kwargs.pop('tag_queryset', None)
        super().__init__(*args, **kwargs)
        self.fields['tags'] = forms.MultipleChoiceField(choices=tags,
                                                        widget=forms.SelectMultiple, required=False)

    def created_choices_from_tag_queryset(self, tag_queryset):
        return [(tag, tag.name) for tag in tag_queryset]

    class Meta:
        model = Entry
        fields = ['from_word', 'to_word', 'from_example', 'tags']


class NewDeckForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ['from_lang', 'to_lang']
