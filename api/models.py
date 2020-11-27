import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Token(models.Model):
    label = models.CharField(max_length=64, null=True, blank=True, verbose_name=_('Label'))
    token = models.CharField(max_length=64, null=True, blank=True, unique=True, verbose_name=_('Token'))
    expires = models.DateTimeField(verbose_name=_('Expires at'))

    class Meta:
        verbose_name = _('Token')
        verbose_name_plural = _('Tokens')

    def save(self, *args, **kwargs):
        if self.token is None:
            self.token = uuid.uuid4().hex
        super().save(*args, **kwargs)

    def __str__(self):
        return self.label or self.id
