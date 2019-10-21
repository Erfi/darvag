from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tags')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ("name", "created_by"),
        )

    def get_count(self):
        return self.entries.count()

    @staticmethod
    def get_instances_from_representations(rep_list, user):
        """
        :param user: the logged in user instance
        :param rep_list: list of [__str__, __str__,...]
        :return: [tag-instance, tag-instance] corresponding to the representation
        """
        result = []
        for rep in rep_list:
            result.append(Tag.objects.get(name=rep.split('|')[0].strip(), created_by=user))
        return result

    def __str__(self):
        return f'{self.name} | by: {self.created_by}'
