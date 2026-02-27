
from django.urls import path, include
from ensayos import views

urlpatterns = [
    #Generar PDF
    path('ensayos/generarPdf', views.generadorPdf, name= "generadorPdf"),

    #Lista Ensayos
    path('ensayos/lista-ensayos', views.listaEnsayos, name="listaEnsayos"),
    path('ensayos/lista-ensayos/<str:ensayo>', views.ensayosRealizados, name="ensayosRealizados"),
    
    
    #Ensayos
    path('ensayos/humedad/<str:muestra_id>/', views.humedad, name="humedad"),
    path('ensayos/granulometria/<str:muestra_id>/', views.granulometria, name="granulometria"),
    path('ensayos/tmic/<str:muestra_id>/', views.tmic, name="tmic"),
    path('ensayos/tmin/<str:muestra_id>/', views.tmin, name="tmin"),
    path('ensayos/lie/<str:muestra_id>/', views.lie, name="lie"),
    path('ensayos/emi/<str:muestra_id>/', views.emi, name="emi"),
	path('ensayos/emiSinIn/<str:muestra_id>/', views.emiSinInductancia, name="emisin"),
    path('ensayos/pmax/<str:muestra_id>/', views.pmax, name="pmax"),
    path('ensayos/clo/<str:muestra_id>/', views.clo, name="clo"),
    path('ensayos/rec/<str:muestra_id>/', views.rec, name="rec"),
    path('ensayos/n1/<str:muestra_id>/', views.n1, name="n1"),
    path('ensayos/n2/<str:muestra_id>/', views.n2, name="n2"),
    path('ensayos/n4/<str:muestra_id>/', views.n4, name="n4"),
    path('ensayos/o1/<str:muestra_id>/', views.o1, name="o1"),
    path('ensayos/tratamiento/<str:muestra_id>/', views.tratamiento, name="tratamiento"),
    path('ensayos/exploNoExplo/<str:muestra_id>/', views.exploNoExplo, name="explonoexplo"),


	#Gestor de archivos para valores de ensayos
	path('ensayos/gestorArchivos/pmax/', views.gestorArchivoPmax, name="gestorArchivosPmax"),
	path('ensayos/gestorArchivos/lie/', views.gestorArchivoLie, name="gestorArchivosLie"),
	path('ensayos/gestorArchivos/emi/', views.gestorArchivoEmi, name="gestorArchivosEmi"),


	#Cambio lista tamices
	path('ensayos/listaTamices/', views.listaTamices, name="listaTamices"),

    
]