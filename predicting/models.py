from django.db import models
from django.utils.safestring import mark_safe


class Concept(models.Model):
    concept = models.CharField(max_length=16, primary_key=True, verbose_name='شناسه')

    class Meta:
        abstract = True


class Disease(Concept):
    class Meta:
        verbose_name = 'بیماری'
        verbose_name_plural = 'بیماری‌ها'

    def persian_name(self):
        return DiseaseName.objects.get(disease=self, locale='fa-ir').string if DiseaseName.objects.filter(disease=self, locale='fa-ir').exists() else None

    def related_symptoms_(self):
        return mark_safe('<br>'.join(str(item) for item in self.diseasesymptom.symptoms.all()))

    def related_conditions_count(self):
        return self.diseasecondition_set.count()

    persian_name.short_description = 'نام فارسی'
    related_symptoms_.short_description = 'علائم مرتبط'
    related_conditions_count.short_description = 'تعداد شرایط تعریف‌شده'

    def __str__(self):
        return f'{self.concept} ({self.persian_name()})' if self.persian_name() else self.concept


class Symptom(Concept):
    class Meta:
        verbose_name = 'علامت'
        verbose_name_plural = 'علائم'

    def __str__(self):
        return f'{self.concept} ({self.persian_name()})' if self.persian_name() else self.concept

    def persian_name(self):
        return SymptomName.objects.get(symptom=self, locale='fa-ir').string if SymptomName.objects.filter(symptom=self, locale='fa-ir').exists() else None

    persian_name.short_description = 'نام فارسی'


class DiseaseSymptom(models.Model):
    disease = models.OneToOneField(to=Disease, on_delete=models.CASCADE)
    symptoms = models.ManyToManyField(to=Symptom, verbose_name='علامت‌های مرتبط')

    class Meta:
        verbose_name = 'علائم بیماری'
        verbose_name_plural = 'علائم بیماری'


class Condition(models.Model):
    label = models.CharField(max_length=256, verbose_name='برچسب')
    expression = models.TextField(verbose_name='عبارت', help_text='متن وارد‌شده می‌بایست یک Expression معتبر پایتونی باشد. متغیر‌ها می‌بایست درون { } قرار گیرند.')

    class Meta:
        verbose_name = 'شرایط'
        verbose_name_plural = 'شرایط'

    def __str__(self):
        return self.label


class DiseaseCondition(models.Model):
    disease = models.ForeignKey(to=Disease, on_delete=models.CASCADE)
    conditions = models.ManyToManyField(to=Condition, verbose_name='شرایط لازمه')
    factor = models.FloatField(verbose_name='ضریب تاثیر')

    class Meta:
        verbose_name = 'شرایط بیماری'
        verbose_name_plural = 'شرایط بیماری‌ها'


class Name(models.Model):
    locales = {'en-us': 'English (United States)', 'fa-ir': 'فارسی (ایران)'}
    locale = models.CharField(max_length=5, choices=tuple(locales.items()), verbose_name='زبان')
    string = models.CharField(max_length=256, verbose_name='رشته')

    class Meta:
        abstract = True
        verbose_name = 'عنوان'
        verbose_name_plural = 'عناوین'


class DiseaseName(Name):
    disease = models.ForeignKey(to=Disease, on_delete=models.CASCADE)


class SymptomName(Name):
    symptom = models.ForeignKey(to=Symptom, on_delete=models.CASCADE)
