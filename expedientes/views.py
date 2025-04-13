from django.shortcuts import render, redirect, get_object_or_404
from expedientes.forms import ExpedientesForm, EmpresaForm, EnsayosMuestras
from django.http import JsonResponse
from .models import Empresa, Expedientes
from ensayos.models import *
from muestras.models import Muestras
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.contrib.auth.decorators import login_required


#Seleccion Expediente
@login_required
def nuevoExpediente(request): 
    if request.method == 'POST':
        form = ExpedientesForm(request.POST)
        if form.is_valid():
            expedienteForm= request.POST["expediente"]
            empresaForm= request.POST["empresa"]
            nMuestrasForm= request.POST["nMuestras"]
            abreviaturaForm= request.POST["abreviatura"]
            
            try:
                empresa = Empresa.objects.get(empresa__icontains=empresaForm)
            except ObjectDoesNotExist:
                print("No se encontró ninguna empresa que coincida con la búsqueda.")
                empresa= Empresa(empresa=empresaForm, abreviatura=abreviaturaForm)
                empresa.save()
            
            try:
                expediente=Expedientes.objects.get(expediente=expedienteForm)
                expediente.nMuestras += int(nMuestrasForm)
            except ObjectDoesNotExist:
                expediente= Expedientes(expediente= expedienteForm, empresa= empresa, estado=1,nMuestras=nMuestrasForm)
                expediente.save()   
            
            abreviatura= empresa.abreviatura 
            
            return redirect('ensayosMuestras', nMuestras=nMuestrasForm, empresa= empresa, expediente=expediente)        
    else:
        form = ExpedientesForm()

    return render(request, 'nuevoExpediente.html', {'form': form})
@login_required
def empresaSugerencias(request):
    data= []
    empresas= Empresa.objects.filter(empresa__icontains=request.POST['term'])
    print(f"las empresas son {empresas}")
    for empresa in empresas:
        data.append(empresa.empresa)
    return JsonResponse(data, safe=False)
@login_required
def empresaExistente(request):
    empresas= Empresa.objects.filter(empresa__iexact=request.POST['term'])
    data=False
    if empresas:
        data=True
    else:
        data=False
    return JsonResponse(data, safe=False)
@login_required
def abreviaturaExistente(request):
    abreviatura= Empresa.objects.filter(abreviatura__iexact=request.POST["term"])
    data=False
    if abreviatura:
        data=True
    else:
        data=False
    print (abreviatura, data)
    return JsonResponse(data, safe=False)

#Seleccion de los ensayos para cada muestra
@login_required
def ensayosMuestras(request,expediente, empresa, nMuestras):

    #Extraemos los objetos de expediente y empresa
    try:
        expediente= Expedientes.objects.get(expediente=expediente)
    except ObjectDoesNotExist:
        print("No existe el expediente")
        
    try:
        empresa= Empresa.objects.get(empresa=empresa)
    except ObjectDoesNotExist:
        print("No existe la empresa") 
        
    
    #Numero de muestras y su identificación
    muestra= Muestras.objects.filter(empresa__empresa=empresa).order_by('-id_muestra')
    
    #Sacamos el id
    if muestra.exists():
        ultimo_id = muestra.first().id_muestra
        id_muestra= ultimo_id + 1

    else:
        id_muestra=1
    
    #Asignamos nombre
    abreviaturaCompleta=empresa.abreviatura + "-" +str(id_muestra)
    
    #mandamos el formulario
    form= EnsayosMuestras()

    
    if form.is_valid:
        if request.POST:
            listaEnsayos = request.POST.getlist('listaEnsayos')
            observaciones= request.POST.get('observaciones')
            
            nuevaMuestra= Muestras(
                id_muestra= id_muestra, 
                empresa= empresa, 
                expediente= expediente, 
                observaciones= observaciones)
            nuevaMuestra.save()

             #Al ser una mny to many no se puede ingresar directamentec como las otras
            nuevaMuestra.listaEnsayos.set(listaEnsayos)
            
            if nMuestras>1:
                return redirect('ensayosMuestras', nMuestras=nMuestras-1, empresa= empresa, expediente=expediente) 
            else:
                return redirect('verExpedientes')    
    
    return render(request, 'ensayosMuestras.html',{
        'abreviaturaCompleta': abreviaturaCompleta,
        'form': form
    })
@login_required
def ensayosMuestrasSimple(request, muestra):
    muestra= Muestras.objects.get(id= muestra)
    expediente= muestra.expediente
    abreviatura= expediente.empresa.abreviatura
    numero_id= muestra.id_muestra
    abreviaturaCompleta= abreviatura + "-" + str(numero_id)
    
    if request.method == "POST":
        form= EnsayosMuestras(request.POST)
        if form.is_valid():
            listaEnsayos = request.POST.getlist('listaEnsayos')
            observaciones= request.POST.get('observaciones')
            
            muestra.observaciones= observaciones
            muestra.listaEnsayos.set(listaEnsayos)


    else:
        form= EnsayosMuestras(initial={
            'listaEnsayos': muestra.listaEnsayos.all(),
            'observaciones': muestra.observaciones
        })



    return render(request, 'ensayosMuestras.html',{
        'abreviaturaCompleta': abreviaturaCompleta,
        'form': form
    })

#Ver expedientes
@login_required
def verExpedientes(request):

    #Sacamos los expedientes
    try:
        expedientes= Expedientes.objects.all().order_by('-fecha')
    except ObjectDoesNotExist:
        print("no hay expedientes")
    
    if request.POST:
        filtro= request.POST["filtro"]
        expedientes= Expedientes.objects.filter(expediente__icontains=filtro).order_by('-fecha')

    
    return render(request, "verExpedientes.html",{
        'expedientes': expedientes
    } )

@login_required
def expediente (request, nExpediente):

    #Sacamos el expediente
    expediente= get_object_or_404(Expedientes, expediente=nExpediente)
    #Sacamos las muestras asignadas a ese expediente
    muestras= Muestras.objects.filter(expediente= expediente)

        
    return render (request, "revisarExpediente.html", {
        "expediente": expediente,
        'muestras': muestras, 
    })


@login_required
def eliminarExpediente (request, expediente):
    if request.POST:
        expediente= get_object_or_404(Expedientes, expediente=expediente)
        expediente.delete()
    return redirect("verExpedientes")