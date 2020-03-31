import uuid

from django.db import models


class Token(models.Model):
    label = models.CharField(max_length=64, null=True, blank=True)
    token = models.CharField(max_length=64, null=True, blank=True, unique=True)
    expires = models.DateTimeField()

    def save(self, *args, **kwargs):
        if self.token is None:
            self.token = uuid.uuid4().hex
        super().save(*args, **kwargs)

    def __str__(self):
        return self.label or 'Token' + f' {self.id}'
