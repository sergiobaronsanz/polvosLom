
from django.urls import path, include
from muestras import views

urlpatterns = [
    #path('muestras/expediente', views.seleccionExpediente, name="seleccionExpediente"),
    path('muestras', views.muestras, name="muestras"),
    path('muestras/recepcion/<str:muestra>', views.recepcionMuestra, name="recepcionMuestra"),
    path('muestras/ver-muestra/<str:muestra_id>', views.verMuestra, name="verMuestra"),

	#Revisón muestra
	path('muestra/revisionMuestra', views.revisionMuestra, name= "revisionMuestra"),

	#Envio Email
    path('muestra/envioMail', views.envioMail, name="envioMail"),

	#CambioIdMuestra
    path('muestra/cambioId/<str:id_muestra>', views.cambiarIdMuestra, name="cambioId"),
	
	#Eliminar muestra
	path('muestra/borrar-muestra/<str:muestra>', views.eliminarMuestra, name= "eliminarMuestra"),
    
]