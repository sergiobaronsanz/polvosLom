from django.urls import path, include
from calidad import views

urlpatterns = [
	#Equipos
    path('equipos', views.equipos, name="equipos"),
    path('equipos/nuevo-equipo', views.nuevoEquipo, name="nuevoEquipo"),
]