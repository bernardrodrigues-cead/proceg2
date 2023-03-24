from django.urls import path
from FichaUab import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pessoa/create/', views.PessoaCreateView.as_view(), name='create_pessoa'),
    path('create/', views.PessoaFichaUabCreateView.as_view(), name='create_pessoa_ficha_uab'),
    path('update/<int:pk>/', views.PessoaFichaUabUpdateView.as_view(), name='update_pessoa_ficha_uab'),
]
