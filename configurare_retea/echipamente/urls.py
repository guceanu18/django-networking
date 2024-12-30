from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_echipamente, name='lista_echipamente'),
    path('adauga/', views.adauga_echipament, name='adauga_echipament'),
    path('configureaza_echipament/<int:echipament_id>/', views.configureaza_echipament, name='configureaza_echipament'),
    path('configurare_interfata/<int:router_id>', views.configurare_interfata, name='configurare_interfata'),
    path('router/<int:router_id>/interfata/<int:interfata_id>/sterge/', views.stergere_interfata, name='stergere_interfata'),
    path('router/<int:router_id>/interfata/<int:interfata_id>/editare/', views.editare_interfata, name='editare_interfata'),
    path('vizualizare_interfete/<int:router_id>/interfete/', views.lista_interfete, name='lista_interfete'),
    path('actiune_echipament/', views.actiune_echipament, name='actiune_echipament'),
    path('stergere/<int:echipament_id>/', views.stergere_echipament, name='stergere_echipament'),
]
