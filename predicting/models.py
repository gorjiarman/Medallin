from django.db import models
from django.conf import settings
from django.utils.functional import cached_property


API_LANGUAGES = {'en': 'English', 'fa': 'فارسی'}


class Concept(models.Model):
    id = models.CharField(max_length=16, primary_key=True)

    def __str__(self):
        return self.id

    def label(self, language=None):
        language = language or settings.LANGUAGE_CODE
        return self.translation_set.get(language=language).string if self.translation_set.filter(language=language).exists() else None

    def type(self):
        return 'Disease' if Disease.objects.filter(concept=self).exists() \
            else 'Symptom' if Symptom.objects.filter(concept=self).exists() \
            else 'Unknown'


class Translation(models.Model):
    concept = models.ForeignKey(to=Concept, on_delete=models.CASCADE)
    language = models.CharField(max_length=2, choices=tuple(API_LANGUAGES.items()))
    string = models.TextField()

    class Meta:
        unique_together = ('concept', 'language')

    def __str__(self):
        return self.string


class Information(models.Model):
    concept = models.ForeignKey(to=Concept, on_delete=models.CASCADE)
    language = models.CharField(max_length=2, choices=tuple(API_LANGUAGES.items()))
    string = models.TextField()

    class Meta:
        unique_together = ('concept', 'language')


class Disease(models.Model):
    concept = models.OneToOneField(to=Concept, on_delete=models.CASCADE)
    red_flag = models.BooleanField(default=False)
    triage = models.CharField(max_length=6, choices=(('low', 'کم‌خطر'), ('medium', 'متوسط'), ('high', 'پر‌خطر')), null=True, blank=True)

    def __str__(self):
        return self.concept_id


class Symptom(models.Model):
    concept = models.OneToOneField(to=Concept, on_delete=models.CASCADE)

    def __str__(self):
        return self.concept.label() or self.concept_id


class Association(models.Model):
    disease = models.ForeignKey(to=Disease, on_delete=models.CASCADE)
    symptom = models.ForeignKey(to=Symptom, on_delete=models.CASCADE)
    weight = models.IntegerField(default=1)

    class Meta:
        unique_together = ('disease', 'symptom')


class PrimitiveCondition(models.Model):
    label = models.CharField(max_length=256)
    expression = models.TextField()

    def __str__(self):
        return self.label


class Condition(models.Model):
    disease = models.ForeignKey(to=Disease, on_delete=models.CASCADE)
    required_conditions = models.ManyToManyField(to=PrimitiveCondition, related_name='required_condition')
    factor = models.FloatField()

    def __str__(self):
        return ' + '.join(self.required_conditions.values_list('label', flat=True))
