import uuid

from django.db import models


class Token(models.Model):
    label = models.CharField(max_length=64, null=True, blank=True, verbose_name='برچسب')
    token = models.CharField(max_length=64, null=True, blank=True, unique=True, verbose_name='توکن', help_text='به صورت خودکار تکمیل خواهد شد.')
    expires = models.DateTimeField(verbose_name='تاریخ انقضا')

    class Meta:
        verbose_name = 'توکن'
        verbose_name_plural = 'توکن‌ها'

    def save(self, *args, **kwargs):
        if self.token is None:
            self.token = uuid.uuid4().hex
        super().save(*args, **kwargs)

    def __str__(self):
        return self.label or 'توکن' + f' {self.id}'
