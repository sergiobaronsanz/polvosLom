
from django.urls import path, include
from ensayos import views

urlpatterns = [
    #path('muestras/expediente', views.seleccionExpediente, name="seleccionExpediente"),
    path('ensayos/humedad', views.humedad, name="humedad"),
    path('equipos', views.equipos, name="equipos"),
    path('equipos/nuevo-equipo', views.nuevoEquipo, name="nuevoEquipo"),
    
]