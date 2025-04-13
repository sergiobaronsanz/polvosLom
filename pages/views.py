from django.shortcuts import render
from muestras.models import *
from ensayos.models import *
from expedientes.models import *
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def inicio(request):
    
    user= request.user

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
        "expedientes": expedientes,
        "user": user,
        
    })



def login_view(request):

    if request.method == "POST":
        usuario=request.POST.get("usuario")
        contraseña=request.POST.get("contraseña")

        user = authenticate(request, username=usuario, password=contraseña)
        print(user)

        if user is not None:
            login(request, user)
            return redirect('inicio')  # redirige a la página principal (ajusta la ruta según tu app)
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")

    
    return render(request, 'pages/login.html')


def logout_view(request):
    # Cerrar la sesión del usuario
    logout(request)
    
    # Redirigir al usuario a la página de login o la página principal
    return redirect('login')  # O a la URL de tu preferencia