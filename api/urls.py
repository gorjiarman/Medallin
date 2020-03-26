from django.urls import path

from api import views

app_name = 'api'
urlpatterns = [
    path('list/symptoms/', views.list_symptoms, name='list-symptoms'),
    path('list/diseases/', views.list_diseases, name='list-diseases'),
    path('predict/', views.predict, name='predict')
]
