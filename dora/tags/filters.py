class TagFilter:

    def __init__(self, queryset):
        self.queryset = queryset

    def _build_item_ids_list(self, tags):
        """
        for each tag create a tuple (len(items), [list of items for the tag])
        and return the list of tuples: [(), (), (),...]}
        Note: each id list is sorted from small to large
        """
        id_tuples = []
        for tag in tags:
            ids = sorted([item.id for item in self.queryset.filter(tags__in=[tag]).distinct()])
            id_tuples.append((len(ids), ids))
        return id_tuples

    def _intersect(self, list1, list2):
        """
        :param list1: list of ids [1, 2, 5] *sorted list*
        :param list2: list of ids [3, 5, 7] *sorted list*
        :return: intersection of the two lists [5]
        """
        intersection = []
        p1 = p2 = 0
        while p1 < len(list1) and p2 < len(list2):
            if list1[p1] == list2[p2]:
                intersection.append(list1[p1])
                p1 += 1
                p2 += 1
            elif list1[p1] < list2[p2]:
                p1 += 1
            else:
                p2 += 1
        return intersection

    def _intersect_all(self, tags):
        # empty query
        if not tags:
            return self.queryset
        ids_lists = self._build_item_ids_list(tags)
        # sort form smallest to the largest list (optimization)
        ids_lists = sorted(ids_lists, key=lambda x: x[0])

        intersection = ids_lists[0][1]
        for i in range(1, len(ids_lists)):
            intersection = self._intersect(intersection, ids_lists[i][1])
        return intersection

    def filter_entries(self, tags):
        intersecting_ids = self._intersect_all(tags)
        return self.queryset if not tags else self.queryset.filter(id__in=intersecting_ids).distinct()
