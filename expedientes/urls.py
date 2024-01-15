from django.urls import path, include
from expedientes import views

urlpatterns = [
    #path('expedientes/', views.descripcionMuestra, name="expedientes"),
    path('expedientes/nuevo-expediente', views.nuevoExpediente, name="nuevoExpediente"),   
    path('expedientes/empresas-sugeridas', views.empresaSugerencias, name="empresasSugeridas"), 
    path('expedientes/empresas-existentes', views.empresaExistente, name="empresasExistente"), 
    path('expedientes/abreviaturas-existentes', views.abreviaturaExistente, name="abreviaturaExistente"),
    path('expedientes/nuevo-expediente/muestras/<str:expediente>/<str:empresa>/<int:nMuestras>/', views.ensayosMuestras, name="ensayosMuestras"),  
    path('expedientes/ver-expedientes', views.verExpedientes, name="verExpedientes"), 
    path('expedientes/ver-expedientes/revisar-expediente/<str:nExpediente>', views.expediente, name="revisarExpediente"),
    path('expedientes/ver-expedientes/revisar-expediente/eliminar-expediente/<str:expediente>', views.eliminarExpediente, name="eliminarExpediente"),  
    
]