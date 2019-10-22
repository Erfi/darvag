class TagFilter:

    def __init__(self, queryset):
        self.queryset = queryset

    def filter_entries(self, tags):
        return self.queryset if not tags else self.queryset.filter(tags__in=tags).distinct()
