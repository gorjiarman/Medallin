from django.db import models
from django.conf import settings


class Concept(models.Model):
    concept_types = {'disease': 'بیماری', 'symptom': 'علامت'}
    id = models.CharField(max_length=16, primary_key=True, verbose_name='شناسه')
    type = models.CharField(max_length=16, choices=tuple(concept_types.items()), verbose_name='نوع شناسه')

    class Meta:
        verbose_name = 'شناسه'
        verbose_name_plural = 'شناسه‌ها'

    def __str__(self):
        string_representation = self.translation()
        return f'{self.id} ({string_representation})' if string_representation else self.id

    def translation(self):
        try:
            return Translation.objects.get(concept=self, locale=settings.LANGUAGE_CODE).string
        except Translation.DoesNotExist:
            return None
    translation.short_description = 'ترجمه (به زبان سیستم)'


class Translation(models.Model):
    locales = {'en-us': 'English (United States)', 'fa-ir': 'فارسی (ایران)'}
    concept = models.ForeignKey(to=Concept, on_delete=models.CASCADE, verbose_name='شناسه')
    locale = models.CharField(max_length=5, choices=tuple(locales.items()), verbose_name='زبان')
    string = models.CharField(max_length=128, verbose_name='رشته')

    class Meta:
        verbose_name = 'ترجمه'
        verbose_name_plural = 'ترجمه‌ها'


class DiseaseFrequency(models.Model):
    concept = models.ForeignKey(to=Concept, on_delete=models.CASCADE, limit_choices_to=models.Q(type='disease'), verbose_name='شناسه')
    frequency = models.PositiveIntegerField(verbose_name='فراوانی')

    class Meta:
        verbose_name = 'فراوانی بیماری'
        verbose_name_plural = 'فراوانی‌های بیماری‌ها'


class Condition(models.Model):
    concept = models.ForeignKey(to=Concept, on_delete=models.CASCADE, limit_choices_to=models.Q(type='disease'), verbose_name='شناسه')
    condition = models.TextField(verbose_name='شرط')
    factor = models.FloatField(verbose_name='ضریب')

    class Meta:
        verbose_name = 'شرط'
        verbose_name_plural = 'شرایط'
