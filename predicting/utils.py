from predicting import models


def search_within_translations(search_term):
    matching = models.Translation.objects.filter(string__contains=search_term)
    return matching.values_list('concept_id', flat=True)
