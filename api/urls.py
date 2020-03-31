from django.urls import path

from api import views

app_name = 'api'
urlpatterns = [
    path('', views.documentations, name='docs'),
    path('list/symptoms/', views.list_symptoms, name='list-symptoms'),
    path('list/diseases/', views.list_diseases, name='list-diseases'),
    path('info/symptom/<str:concept_id>/', views.info_on_symptom, name='info-on-symptom'),
    path('info/disease/<str:concept_id>/', views.info_on_disease, name='info-on-disease'),
    path('predict/', views.predict, name='predict')
]
