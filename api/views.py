import json

from django.http import HttpResponseBadRequest, JsonResponse
from django_q.tasks import result as async_result, async_task

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
            result = async_result(task_id=request.GET.get('id'))
            return JsonResponse({'status': 'completed' if result is not None else 'pending', 'result': result})
    if request.POST:
        symptoms, profile = request.POST.get('symptoms'), request.POST.get('profile')
        symptoms, profile = json.loads(symptoms), json.loads(profile)
        tracking_id = async_task('api.services.make_prediction', symptoms, profile)
        return JsonResponse({'id': tracking_id})
    return HttpResponseBadRequest('Invalid request.')
