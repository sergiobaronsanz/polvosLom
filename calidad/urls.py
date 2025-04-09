from django.urls import path, include
from calidad import views

urlpatterns = [
	#Equipos
    path('equipos', views.equipos, name="equipos"),
    path('equipos/nuevo-equipo', views.nuevoEquipo, name="nuevoEquipo"),
	path('equipos/editar-equipo/<str:id_equipo>/', views.editarEquipo, name="editarEquipo"),
	path('eqipos/eliminarEquipo/<str:id_equipo>', views.eliminarEquipo, name= "eliminarEquipo"),
]