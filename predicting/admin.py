from django.contrib import admin
from django.conf import settings

from predicting import models


class TranslationInline(admin.StackedInline):
    model = models.Translation
    extra = 1


class InformationInline(admin.StackedInline):
    model = models.Information
    extra = 1


class Concept(admin.ModelAdmin):
    inlines = [TranslationInline, InformationInline]
    list_display = ('id', 'type', 'label')
    search_fields = ('id', )

    @staticmethod
    def label(concept):
        try:
            return concept.translation_set.get(language=settings.LANGUAGE_CODE)
        except models.Translation.DoesNotExist:
            return '-'


class AssociationInline(admin.StackedInline):
    model = models.Association
    extra = 1


class ConditionInline(admin.StackedInline):
    model = models.Condition
    extra = 1


class Disease(admin.ModelAdmin):
    inlines = [AssociationInline, ConditionInline]
    list_display = ('concept_id', 'label', 'red_flag', 'triage')
    search_fields = ('concept__id', )

    @staticmethod
    def concept_id(disease):
        return disease.concept

    @staticmethod
    def label(disease):
        try:
            return disease.concept.translation_set.get(language=settings.LANGUAGE_CODE)
        except models.Translation.DoesNotExist:
            return '-'


class Symptom(admin.ModelAdmin):
    list_display = ('concept_id', 'label')
    search_fields = ('concept__id', )

    @staticmethod
    def concept_id(symptom):
        return symptom.concept

    @staticmethod
    def label(symptom):
        try:
            return symptom.concept.translation_set.get(language=settings.LANGUAGE_CODE)
        except models.Translation.DoesNotExist:
            return '-'


class PrimitiveCondition(admin.ModelAdmin):
    list_display = ('label', 'expression')


admin.site.register(models.Concept, Concept)
admin.site.register(models.PrimitiveCondition, PrimitiveCondition)
admin.site.register(models.Disease, Disease)
admin.site.register(models.Symptom, Symptom)
