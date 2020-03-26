from django.http import HttpResponse, HttpResponseBadRequest
from django.utils import timezone

from api import models


def requires_token(view_func):
    def wrapper(request, *args, **kwargs):
        authorization = request.META.get('HTTP_AUTHORIZATION', '')
        if authorization.startswith('Bearer '):
            token = authorization.replace('Bearer ', '')
            if models.Token.objects.filter(token=token, expires__gt=timezone.now()).exists():
                return view_func(request, *args, **kwargs)
            return HttpResponse('Invalid or expired token.', status=401)
        return HttpResponseBadRequest('No bearer token found.')
    return wrapper
