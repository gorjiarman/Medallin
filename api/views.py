import json

from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
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
