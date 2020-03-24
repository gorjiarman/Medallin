from django.contrib import admin

from predicting import models


class InlineTranslationAdmin(admin.TabularInline):
    model = models.Translation
    extra = 1


class ConceptAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'translation')
    list_filter = ('type', )
    inlines = (InlineTranslationAdmin, )


class DiseaseFrequencyAdmin(admin.ModelAdmin):
    list_display = ('concept', 'frequency')
    list_editable = ('frequency', )


class ConditionAdmin(admin.ModelAdmin):
    list_display = ('concept', 'condition', 'factor')
    list_editable = ('factor', )
    search_fields = ('concept__id', )


admin.site.register(models.Concept, ConceptAdmin)
admin.site.register(models.DiseaseFrequency, DiseaseFrequencyAdmin)
admin.site.register(models.Condition, ConditionAdmin)
