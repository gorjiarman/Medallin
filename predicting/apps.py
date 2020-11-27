from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PredictingConfig(AppConfig):
    name = 'predicting'
    verbose_name = _('Predicting')

