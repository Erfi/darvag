from django.db import models
from django.contrib.auth.models import User


class Entry(models.Model):
    from_lang = models.CharField(max_length=45)
    to_lang = models.CharField(max_length=45)
    from_word = models.CharField(max_length=45)
    to_word = models.CharField(max_length=45)
    from_example = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='entries')

    def __str__(self):
        return f'{self.from_word}-->{self.to_word} | by: {self.created_by}'