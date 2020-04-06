from django.contrib import admin
from django.conf import settings
from django.utils.translation import gettext_lazy as _

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


class AssociationViewingInline(admin.StackedInline):
    model = models.Association
    readonly_fields = ('symptom', )
    extra = 0
    verbose_name_plural = _('Current associations')

    def has_add_permission(self, request, obj):
        return False


class AssociationAddingInline(admin.StackedInline):
    model = models.Association
    extra = 1
    verbose_name_plural = _('Creating a new association')

    def has_change_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return False


class ConditionInline(admin.StackedInline):
    model = models.Condition
    extra = 1


class DiseaseType(admin.ModelAdmin):
    list_display = ('name', 'label')
    search_fields = ('name', 'label')


class Disease(admin.ModelAdmin):
    inlines = [AssociationViewingInline, AssociationAddingInline, ConditionInline]
    list_display = ('concept_id', 'label', 'type', 'red_flag', 'triage')
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
    list_display = ('concept_id', 'label', 'professional')
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
admin.site.register(models.DiseaseType, DiseaseType)
admin.site.register(models.Disease, Disease)
admin.site.register(models.Symptom, Symptom)
