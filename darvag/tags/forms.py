from django.forms import Form, MultipleChoiceField, SelectMultiple


class TagFilterForm(Form):

    def __init__(self, *args, tags_queryset, **kwargs):
        super().__init__(*args, **kwargs)
        tags = self.created_choices_from_tag_queryset(tags_queryset)
        self.fields['tags'] = MultipleChoiceField(choices=tags, widget=SelectMultiple, required=False)

    def created_choices_from_tag_queryset(self, tag_queryset):
        return [(tag, tag.name) for tag in tag_queryset]
