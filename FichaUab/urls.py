from django.urls import path
from FichaUab import views

urlpatterns = [
    path('', views.index, name='index')
]
