from django.shortcuts import render
from muestras.models import *
from ensayos.models import *
from expedientes.models import *
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, F, ExpressionWrapper, FloatField
from django.db.models.functions import ExtractMonth
from django.http import JsonResponse
import json



# Create your views here.
@login_required
def inicio(request):
    
    user= request.user

    #Fecha actual
    año_actual = timezone.now().year
    
    #Resumen expedientes
    nExpedientesEnsayando= Expedientes.objects.filter(estado="3").count()
    nExpedientesPendientes= Expedientes.objects.filter(estado="4").count()
    nExpedientesAbiertos=nExpedientesEnsayando + nExpedientesPendientes
    
    nExpedientesTerminados= Expedientes.objects.filter(fecha__year=año_actual).filter(estado="5").count()
    nMuestrasTotales= Muestras.objects.filter(expediente__fecha__year= año_actual).count()
    
    #Evolución ensayos
    evolucionExpedientes= Expedientes.objects.filter(estado__in=["3", "4"])
    
    #Número de muestras realizadas por mes
    # Agrupar por mes y contar
    muestras_por_mes_qs = (
        Muestras.objects
        .filter(expediente__fecha__year=año_actual)
        .annotate(mes=ExtractMonth('expediente__fecha'))
        .values('mes')
        .annotate(total=Count('id'))
        .order_by('mes')
    )

    muestras_por_mes_dict= {mes:0 for mes in range(1,13)}

    for item in muestras_por_mes_qs:
        muestras_por_mes_dict[item['mes']]= item['total']
   
    muestrasPorMes = [muestras_por_mes_dict[mes] for mes in range(1, 13)]

    # Convertimos a json
    muestrasPorMes_json= json.dumps(muestrasPorMes)

    #Expedientes por empresas
    top_empresas = Empresa.objects.filter(
            muestras__fecha__year=año_actual
        ).annotate(
            total_muestras=Count('muestras')
        ).order_by('-total_muestras')[:5]
    
    empresasTop= []
    colores= ["primary", "success", "info", "secondary", "warning"]
    bucle= 0
    for empresa in top_empresas:
        empresasTop.append({'empresa': empresa.empresa, 'nMuestras': empresa.total_muestras, 'color': colores[bucle]})
        bucle = bucle + 1
    
    print(empresasTop)
    top_empresas_json= json.dumps(empresasTop)


    #Expedientes por mes 
    expedientes_por_año = (Expedientes.objects
                       .filter(fecha__year__gte=año_actual - 5, fecha__year__lte=año_actual)  # Filtrar los últimos 5 años
                       .values('fecha__year')  # Agrupar por año
                       .annotate(nExpedientes=Count('id'))  # Contar los expedientes
                       .order_by('fecha__year')) 
    # Convertimos a json
    expedientes_por_año = [{'año': item['fecha__year'], 'nExpedientes': item['nExpedientes']} for item in expedientes_por_año]    
    print(f"el expediente es {expedientes_por_año}")
    expediente_por_año_json= json.dumps(expedientes_por_año)

    
    return render(request,'pages/inicio.html', { 
        "nExpedientesAbiertos": nExpedientesAbiertos,
        "nExpedientesPendientes": nExpedientesPendientes,
        "nExpedientesTerminados": nExpedientesTerminados,
        "nMuestrasTotales": nMuestrasTotales,
        "evolucionExpedientes": evolucionExpedientes,
        "user": user,
        "año": año_actual,
        "muestrasPorMes": muestrasPorMes_json,
        "top_empresas": empresasTop,
        "top_empresas_json": top_empresas_json,
        "expediente_por_año_json": expediente_por_año_json
        
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
