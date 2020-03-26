from django.contrib import admin

from predicting import models


class InlineDiseaseSymptom(admin.TabularInline):
    model = models.DiseaseSymptom


class InlineDiseaseCondition(admin.StackedInline):
    model = models.DiseaseCondition
    extra = 1


class InlineDiseaseName(admin.StackedInline):
    model = models.DiseaseName
    extra = 1


class InlineSymptomName(admin.StackedInline):
    model = models.SymptomName
    extra = 1


class DiseaseAdmin(admin.ModelAdmin):
    inlines = (InlineDiseaseName, InlineDiseaseSymptom, InlineDiseaseCondition)
    list_display = ('concept', 'persian_name', 'related_symptoms_', 'related_conditions_count')


class SymptomAdmin(admin.ModelAdmin):
    list_display = ('concept', 'persian_name')
    inlines = (InlineSymptomName, )


class ConditionAdmin(admin.ModelAdmin):
    list_display = ('label', 'expression')


admin.site.register(models.Disease, DiseaseAdmin)
admin.site.register(models.Symptom, SymptomAdmin)
admin.site.register(models.Condition, ConditionAdmin)
