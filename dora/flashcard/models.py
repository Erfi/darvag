from django.db import models
from django.contrib.auth.models import User


class Entry(models.Model):
    from_lang = models.CharField(max_length=45)
    to_lang = models.CharField(max_length=45)
    from_word = models.CharField(max_length=45)
    to_word = models.CharField(max_length=45)
    from_example = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='entries')

