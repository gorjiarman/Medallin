from django.contrib import admin
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from predicting import models, utils


class TranslationInline(admin.StackedInline):
    model = models.Translation
    extra = 1


class Concept(admin.ModelAdmin):
    inlines = [TranslationInline]
    list_display = ('id', 'type', 'label')
    search_fields = ('id', )

    @staticmethod
    def label(concept):
        try:
            return concept.translation_set.get(language=settings.LANGUAGE_CODE)
        except models.Translation.DoesNotExist:
            return '-'


class Property(admin.ModelAdmin):
    list_display = ('name', 'label')


class InformationPropertyInline(admin.StackedInline):
    model = models.InformationProperty
    extra = 1


class Information(admin.ModelAdmin):
    inlines = [InformationPropertyInline]
    list_display = ('information_concept_id', 'concept_label', 'language', 'properties')
    list_filter = ('language', )
    autocomplete_fields = ('concept', )
    search_fields = ('concept_id', )

    def get_search_results(self, request, queryset, search_term):
        concepts = models.Concept.objects.filter(id__contains=search_term)
        translations = models.Translation.objects.filter(string__contains=search_term).values('concept_id')
        concepts = concepts | models.Concept.objects.filter(id__in=translations)
        results = models.Information.objects.filter(concept__in=concepts)
        return results, False

    @staticmethod
    def information_concept_id(information):
        return information.concept.id

    @staticmethod
    def concept_label(information):
        return information.concept.label()

    @staticmethod
    def properties(information):
        return models.InformationProperty.objects.filter(information=information).count()


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
    autocomplete_fields = ('symptom', )
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

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        matching_concepts = utils.search_within_translations(search_term)
        return queryset | models.Disease.objects.filter(concept_id__in=matching_concepts), use_distinct


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

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        matching_concepts = utils.search_within_translations(search_term)
        return queryset | models.Symptom.objects.filter(concept_id__in=matching_concepts), use_distinct


class PrimitiveCondition(admin.ModelAdmin):
    list_display = ('label', 'expression')


admin.site.register(models.Concept, Concept)
admin.site.register(models.Property, Property)
admin.site.register(models.Information, Information)
admin.site.register(models.PrimitiveCondition, PrimitiveCondition)
admin.site.register(models.DiseaseType, DiseaseType)
admin.site.register(models.Disease, Disease)
admin.site.register(models.Symptom, Symptom)
