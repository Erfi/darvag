from django.forms import Form, MultipleChoiceField, SelectMultiple, ModelMultipleChoiceField


# --- customizations ---
class TagModelMultipleChoiceField(ModelMultipleChoiceField):
    def label_from_instance(self, tag):
        return tag.name


# ----------------------

class TagFilterForm(Form):

    def __init__(self, *args, tags_queryset, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'] = TagModelMultipleChoiceField(queryset=tags_queryset, widget=SelectMultiple, required=False)
