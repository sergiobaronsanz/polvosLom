
from django.urls import path, include
from ensayos import views

urlpatterns = [
    #Generar PDF
    path('ensayos/generarPdf', views.generadorPdf, name= "generadorPdf"),

    #Lista Ensayos
    path('ensayos/lista-ensayos', views.listaEnsayos, name="listaEnsayos"),
    path('ensayos/lista-ensayos/<str:ensayo>', views.ensayosRealizados, name="ensayosRealizados"),
    
    #Equipos
    path('equipos', views.equipos, name="equipos"),
    path('equipos/nuevo-equipo', views.nuevoEquipo, name="nuevoEquipo"),
    
    #Ensayos
    path('ensayos/humedad/<str:muestra_id>/', views.humedad, name="humedad"),
    path('ensayos/granulometria/<str:muestra_id>/', views.granulometria, name="granulometria"),
    path('ensayos/tmic/<str:muestra_id>/', views.tmic, name="tmic"),
    path('ensayos/tmin/<str:muestra_id>/', views.tmin, name="tmin"),
    path('ensayos/lie/<str:muestra_id>/', views.lie, name="lie"),
    path('ensayos/emi/<str:muestra_id>/', views.emi, name="emi"),
    path('ensayos/pmax/<str:muestra_id>/', views.pmax, name="pmax"),
    path('ensayos/clo/<str:muestra_id>/', views.clo, name="clo"),
    path('ensayos/rec/<str:muestra_id>/', views.rec, name="rec"),
    path('ensayos/n1/<str:muestra_id>/', views.n1, name="n1"),
    path('ensayos/n2/<str:muestra_id>/', views.n2, name="n2"),
    path('ensayos/n4/<str:muestra_id>/', views.n4, name="n4"),
    path('ensayos/o1/<str:muestra_id>/', views.o1, name="o1"),


    
]