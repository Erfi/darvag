from tags.models import Tag


class TagFilter:

    def __init__(self, queryset):
        self.queryset = queryset

    def filter_entries(self, cleaned_data, user):
        tags_list = []
        for tag, value in cleaned_data.items():
            if value:
                tag_instance = Tag.objects.get(name=tag, created_by=user)
                tags_list.append(tag_instance)

        return self.queryset if not tags_list else self.queryset.filter(tags__in=tags_list).distinct()
