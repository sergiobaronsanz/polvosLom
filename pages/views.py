from django.shortcuts import render
from muestras.models import *
from ensayos.models import *
from expedientes.models import *
from django.db.models import Q
from django.utils import timezone

# Create your views here.

def inicio(request):
    
    #Fecha actual
    año_actual = timezone.now().year
    
    #Resumen expedientes
    nExpedientesEnsayando= Expedientes.objects.filter(fecha__year=año_actual).filter(estado="3").count()
    nExpedientesPendientes= Expedientes.objects.filter(fecha__year=año_actual).filter(estado="4").count()
    nExpedientesAbiertos=nExpedientesEnsayando + nExpedientesPendientes
    
    nExpedientesTerminados= Expedientes.objects.filter(fecha__year=año_actual).filter(estado="4").count()
    nMuestrasTotales= Muestras.objects.filter(expediente__fecha__year= año_actual).count()
    
    #Evolución ensayos
    expedientes= Expedientes.objects.filter(fecha__year=año_actual, estado__in=["3", "4"])
    print(expedientes)
    
    #muestrasExpedientes= Muestras.objects.filter(expediente= expedientes)
    
    return render(request,'pages/inicio.html', { 
        "nExpedientesAbiertos": nExpedientesAbiertos,
        "nExpedientesPendientes": nExpedientesPendientes,
        "nExpedientesTerminados": nExpedientesTerminados,
        "nMuestrasTotales": nMuestrasTotales,
        "expedientes": expedientes
        
    })