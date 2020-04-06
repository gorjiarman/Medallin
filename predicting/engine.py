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
    patients_conditions = matching_conditions(profile)
    for disease in scores:
        related_conditions = models.Condition.objects.filter(disease__concept_id=disease)
        for condition in patients_conditions:
            related_conditions = related_conditions.filter(required_conditions=condition)
        try:
            applying_condition = related_conditions.get()
        except models.Condition.DoesNotExist:
            applying_condition = None
        except models.Condition.MultipleObjectsReturned:
            factors_matches = []
            for condition in related_conditions:
                matching_primitive_conditions = [primitive_condition for primitive_condition in condition.required_conditions.all() if primitive_condition in patients_conditions]
                factors_matches.append((len(matching_primitive_conditions), -condition.factor))
                # When looking for maximum, Python first looks at the first element of the tuple and then if the first
                # element of two tuples matches, the second one. We want it to look for the greatest number of matches
                # but the least value of factor. We can negate the second element and do the whole lookup in one call to
                # the build-in max function.
            applying_condition = factors_matches.index(max(factors_matches))
            applying_condition = related_conditions[applying_condition]
        factors[disease] = applying_condition.factor if applying_condition else None
    predictions = sort_diseases(scores, factors)
    suggestions = matching_symptoms(scores.keys(), symptoms.keys())
    return {'predictions': predictions, 'suggestions': suggestions}
