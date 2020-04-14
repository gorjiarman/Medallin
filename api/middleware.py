from django.utils.deprecation import MiddlewareMixin
from django.utils import translation


class AdminLanguageMiddleware(MiddlewareMixin):

    @staticmethod
    def process_request(request):
        if request.path.startswith('/admin'):
            translation.activate("fa-ir")
            request.LANGUAGE_CODE = translation.get_language()
