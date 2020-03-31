import string

from django.db.models import Count, Sum

from predicting import models


def matching_diseases(symptoms):
    matching = models.Association.objects.filter(symptom__concept_id__in=list(symptoms)).values('disease__concept_id', 'weight')
    return matching.annotate(score=Sum('weight')).values_list('disease__concept_id', 'score')


def matching_conditions(profile):
    true_conditions = []
    for condition in models.PrimitiveCondition.objects.all():
        template = string.Template(condition.expression)
        try:
            expression = template.substitute(profile)
        except (KeyError, ValueError):
            is_true = False
        else:
            is_true = eval(expression)
        if is_true:
            true_conditions.append(condition)
    return true_conditions


def sort_diseases(scores, factors):
    diseases = [(disease, scores[disease], factors[disease]) for disease in scores.keys()]
    diseases = sorted(diseases, key=lambda tup: tup[1:], reverse=True)
    return diseases[:10]


def matching_symptoms(diseases, symptoms):
    matching = models.Association.objects.filter(disease__concept_id__in=diseases).exclude(symptom__concept_id__in=symptoms).values('symptom__concept_id')
    matching = matching.annotate(occurrences=Count('symptom__concept_id')).order_by('-occurrences')[:10].values_list('symptom__concept_id', flat=True)
    return list(matching)


def predict(symptoms: dict, profile: dict):
    scores = dict()
    for disease, score in matching_diseases(symptom for symptom, value in symptoms.items() if value > 0):
        scores[disease] = score
    for disease, score in matching_diseases(symptom for symptom, value in symptoms.items() if value < 0):
        current_score = scores.setdefault(disease, 0)
        scores[disease] = current_score - score
    factors = dict()
    conditions = matching_conditions(profile)
    for disease in scores:
        related_conditions = models.Condition.objects.filter(disease__concept_id=disease)
        for condition in conditions:
            related_conditions = related_conditions.filter(required_conditions=condition)
        try:
            applying_condition = related_conditions.get()
        except models.Condition.DoesNotExist:
            applying_condition = None
        except models.Condition.MultipleObjectsReturned:
            max_matches = 0
            applying_condition = None
            for condition in related_conditions:
                condition_matches = len([condition for condition in condition.required_conditions.all() if condition in conditions])
                if condition_matches > max_matches:
                    applying_condition = condition
                    max_matches = condition_matches
        factors[disease] = applying_condition.factor if applying_condition else None
    predictions = sort_diseases(scores, factors)
    suggestions = matching_symptoms(scores.keys(), symptoms.keys())
    return {'predictions': predictions, 'suggestions': suggestions}
