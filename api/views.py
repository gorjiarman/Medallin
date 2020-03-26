import json

from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404

from api import models, utils
from predicting import models as prediction


@utils.requires_token
def list_symptoms(request):
    symptoms = prediction.SymptomName.objects.filter(locale=request.LANGUAGE_CODE).order_by('string')
    return JsonResponse({it.symptom_id: it.string for it in symptoms})


@utils.requires_token
def list_diseases(request):
    diseases = prediction.DiseaseName.objects.filter(locale=request.LANGUAGE_CODE).order_by('string')
    return JsonResponse({it.disease_id: it.string for it in diseases})


@utils.requires_token
def predict(request):
    if request.GET:
        if request.GET.get('id'):
            prediction_id = request.GET['id']
            prediction = get_object_or_404(models.Prediction, id=int(prediction_id))
            prediction_result = prediction.result
            return JsonResponse({'status': prediction_result is not None, 'result': prediction_result})
    if request.POST:
        symptoms, profile = request.POST.get('symptoms'), request.POST.get('profile')
        symptoms, profile = json.loads(symptoms), json.loads(profile)
        # TODO: Enqueue the prediction.
        return JsonResponse({'id': None})
    return HttpResponseBadRequest('Invalid request.')
