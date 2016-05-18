from django.db import models
from django.contrib.auth.models import User


class File(models.Model):
    name = models.CharField(max_length=200)
    revision = models.IntegerField(default=1)
    hash_sum = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, related_name='files')

    def __str__(self):
        return "{}#{}".format(self.name, self.revision)
