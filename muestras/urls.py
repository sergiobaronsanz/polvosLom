
from django.urls import path, include
from muestras import views

urlpatterns = [
    #path('muestras/expediente', views.seleccionExpediente, name="seleccionExpediente"),
    path('muestras/recepcion', views.recepcionMuestra, name="recepcionMuestra"),
    path('muestras/ver-muestra/<str:muestra_id>', views.verMuestra, name="verMuestra")
    
]