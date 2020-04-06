import json

from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, get_object_or_404
from django_q.tasks import result as async_result, async_task

from api import utils
from predicting import models as prediction, engine


def documentations(request):
    return render(request, 'api-docs.html')


@utils.requires_token
def list_symptoms(request):
    return JsonResponse({symptom.concept.id: symptom.concept.label(language=request.LANGUAGE_CODE)
                         for symptom in prediction.Symptom.objects.all()})


@utils.requires_token
def list_diseases(request):
    return JsonResponse({disease.concept.id: disease.concept.label(language=request.LANGUAGE_CODE)
                         for disease in prediction.Disease.objects.all()})


@utils.requires_token
def info_on_symptom(request, concept_id):
    symptom = get_object_or_404(prediction.Symptom, concept_id=concept_id)
    properties = prediction.InformationProperty.objects.filter(information__concept_id=concept_id, information__language=request.LANGUAGE_CODE)
    payload = {
        'label': symptom.concept.label(request.LANGUAGE_CODE),
        'values': symptom.values
    }
    for symptom_property in properties:
        payload[symptom_property.property.name] = symptom_property.value
    return JsonResponse(payload)


@utils.requires_token
def info_on_disease(request, concept_id):
    disease = get_object_or_404(prediction.Disease, concept_id=concept_id)
    properties = prediction.InformationProperty.objects.filter(information__concept_id=concept_id, information__language=request.LANGUAGE_CODE)
    payload = {
        'label': disease.concept.label(request.LANGUAGE_CODE),
        'type': disease.type.name if disease.type else None,
        'red_flag': disease.red_flag,
        'triage': disease.triage
    }
    for disease_property in properties:
        payload[disease_property.property.name] = disease_property.value
    return JsonResponse(payload)


@utils.requires_token
def predict(request):
    if request.GET:
        if request.GET.get('id'):
            result = async_result(task_id=request.GET.get('id'))
            return JsonResponse({'status': 'completed' if result is not None else 'pending', 'result': result})
    if request.POST:
        symptoms, profile = request.POST.get('symptoms'), request.POST.get('profile')
        symptoms, profile = json.loads(symptoms), json.loads(profile)
        tracking_id = async_task('predicting.engine.predict', symptoms, profile)
        return JsonResponse({'id': tracking_id})
    return HttpResponseBadRequest('Invalid request.')
