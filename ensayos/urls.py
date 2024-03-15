
from django.urls import path, include
from ensayos import views

urlpatterns = [
    #Lista Ensayos
    path('ensayos/lista-ensayos', views.listaEnsayos, name="listaEnsayos"),
    path('ensayos/lista-ensayos/<str:ensayo>', views.ensayosRealizados, name="ensayosRealizados"),
    
    #Equipos
    path('equipos', views.equipos, name="equipos"),
    path('equipos/nuevo-equipo', views.nuevoEquipo, name="nuevoEquipo"),
    
    #Ensayos
    path('ensayos/humedad/<str:muestra_id>/', views.humedad, name="humedad"),
    
    
]