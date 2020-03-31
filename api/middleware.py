from django.middleware.locale import LocaleMiddleware
from django.conf import settings


class ModifiedLocaleMiddleware(LocaleMiddleware):

    def process_request(self, request):
        if request.path.startswith('/admin'):
            request.LANGUAGE_CODE = settings.LANGUAGE_CODE
        else:
            super().process_request(request)
