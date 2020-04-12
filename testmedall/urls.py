from django.urls import path
from testmedall import views

app_name = 'testmedall'
urlpatterns = [
    path('', views.index, name='docs')
]
