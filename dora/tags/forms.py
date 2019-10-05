from django.forms import Form, BooleanField


class TagFilterForm(Form):

    def __init__(self, *args, tags_queryset, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields = {}
        for tag in tags_queryset:
            self.fields[tag.name] = BooleanField(initial=False, label=tag.name, required=False)




