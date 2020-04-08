from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


API_LANGUAGES = {'en': 'English', 'fa': 'فارسی'}


class Concept(models.Model):
    id = models.CharField(max_length=16, primary_key=True, verbose_name=_('ID'))

    class Meta:
        verbose_name = _('Concept')
        verbose_name_plural = _('Concepts')

    def __str__(self):
        return self.id

    def label(self, language=None):
        language = language or settings.LANGUAGE_CODE
        return self.translation_set.get(language=language).string if self.translation_set.filter(language=language).exists() else None
    label.short_description = _('Label')

    def type(self):
        return 'Disease' if Disease.objects.filter(concept=self).exists() \
            else 'Symptom' if Symptom.objects.filter(concept=self).exists() \
            else 'Unknown'
    type.short_description = _('Type')


class Translation(models.Model):
    concept = models.ForeignKey(to=Concept, on_delete=models.CASCADE, verbose_name=_('Concept'))
    language = models.CharField(max_length=2, choices=tuple(API_LANGUAGES.items()), verbose_name=_('Language'))
    string = models.TextField(verbose_name=_('String'))

    class Meta:
        verbose_name = _('Translation')
        verbose_name_plural = _('Translations')
        unique_together = ('concept', 'language')

    def __str__(self):
        return self.string


class Property(models.Model):
    name = models.CharField(max_length=128, verbose_name=_('Name'))
    label = models.CharField(max_length=128, verbose_name=_('Label'), help_text=_('Shown in admin only.'))

    class Meta:
        verbose_name = _('Property')
        verbose_name_plural = _('Properties')

    def __str__(self):
        return self.label


class Information(models.Model):
    concept = models.ForeignKey(to=Concept, on_delete=models.CASCADE, verbose_name=_('Concept'))
    language = models.CharField(max_length=2, choices=tuple(API_LANGUAGES.items()), verbose_name=_('Language'))

    class Meta:
        verbose_name = _('Information')
        verbose_name_plural = _('Information')
        unique_together = ('concept', 'language')


class InformationProperty(models.Model):
    information = models.ForeignKey(to=Information, on_delete=models.CASCADE)
    property = models.ForeignKey(to=Property, on_delete=models.CASCADE)
    value = models.TextField()

    class Meta:
        verbose_name = _('Information Property')
        verbose_name_plural = _('Information Properties')


class DiseaseType(models.Model):
    name = models.CharField(max_length=256, verbose_name=_('Name'))
    label = models.CharField(max_length=256, verbose_name=_('Label'), help_text=_('Only shown in admin.'))

    class Meta:
        verbose_name = _('Disease Type')
        verbose_name_plural = _('Disease Types')

    def __str__(self):
        return self.label


class Disease(models.Model):
    concept = models.OneToOneField(to=Concept, on_delete=models.CASCADE, verbose_name=_('Concept'))
    type = models.ForeignKey(to=DiseaseType, on_delete=models.SET_NULL, null=True, blank=True)
    red_flag = models.BooleanField(default=False, verbose_name=_('Red Flag'))
    triage = models.CharField(max_length=6, choices=(('low', 'کم‌خطر'), ('medium', 'متوسط'), ('high', 'پر‌خطر')), null=True, blank=True, verbose_name=_('Triage'))

    class Meta:
        verbose_name = _('Disease')
        verbose_name_plural = _('Diseases')

    def __str__(self):
        return self.concept.label() or self.concept_id


class Symptom(models.Model):
    concept = models.OneToOneField(to=Concept, on_delete=models.CASCADE, verbose_name=_('Concept'))
    values = models.CharField(max_length=16, choices=(('[-1, 1]', '[-1, 1]'), ('[0, 1]', '[0, 1]'), ('-1, 0, 1', '-1, 0, 1')), verbose_name=_('Values'))
    professional = models.BooleanField(default=False, verbose_name=_('Professional'))

    class Meta:
        verbose_name = _('Symptom')
        verbose_name_plural = _('Symptoms')

    def __str__(self):
        return self.concept.label() or self.concept_id


class Association(models.Model):
    disease = models.ForeignKey(to=Disease, on_delete=models.CASCADE, verbose_name=_('Disease'))
    symptom = models.ForeignKey(to=Symptom, on_delete=models.CASCADE, verbose_name=_('Symptom'))
    weight = models.FloatField(default=1, verbose_name=_('Weight'))

    class Meta:
        verbose_name = _('Association')
        verbose_name_plural = _('Associations')
        unique_together = ('disease', 'symptom')


class PrimitiveCondition(models.Model):
    label = models.CharField(max_length=256, verbose_name=_('Label'))
    expression = models.TextField(verbose_name=_('Expression'))

    class Meta:
        verbose_name = _('Primitive Condition')
        verbose_name_plural = _('Primitive Conditions')

    def __str__(self):
        return self.label


class Condition(models.Model):
    disease = models.ForeignKey(to=Disease, on_delete=models.CASCADE, verbose_name=_('Disease'))
    required_conditions = models.ManyToManyField(to=PrimitiveCondition, related_name='required_condition', verbose_name=_('Required Conditions'))
    factor = models.FloatField(verbose_name=_('Factor'))

    class Meta:
        verbose_name = _('Condition')
        verbose_name_plural = _('Conditions')
