from django.shortcuts import render, redirect
from expedientes.forms import ExpedientesForm, EmpresaForm, EnsayosMuestras
from django.http import JsonResponse
from .models import Empresa, Expedientes
from muestras.models import Muestras
from django.core.exceptions import ObjectDoesNotExist


#Seleccion Expediente
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

def empresaSugerencias(request):
    data= []
    empresas= Empresa.objects.filter(empresa__icontains=request.POST['term'])
    print(f"las empresas son {empresas}")
    for empresa in empresas:
        data.append(empresa.empresa)
    return JsonResponse(data, safe=False)

def empresaExistente(request):
    empresas= Empresa.objects.filter(empresa__iexact=request.POST['term'])
    data=False
    if empresas:
        data=True
    else:
        data=False
    return JsonResponse(data, safe=False)

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
    abreviatura=empresa.abreviatura + "-" +str(id_muestra)
    print(abreviatura)
    
    #mandamos el formulario
    form= EnsayosMuestras()
    
    if request.POST:
        listaEnsayos = request.POST.getlist('listaEnsayos')
        observaciones= request.POST.get('observaciones')
        
        nuevaMuestra= Muestras(
            id_muestra= id_muestra, 
            empresa= empresa, 
            expediente= expediente, 
            observaciones= observaciones)
        nuevaMuestra.save()
        
        nuevaMuestra.listaEnsayos.set(listaEnsayos) #Al ser una mny to many no se puede ingresar directamentec como las otras
        
        
        if nMuestras>1:
            return redirect('ensayosMuestras', nMuestras=nMuestras-1, empresa= empresa, expediente=expediente) 
        else:
            return redirect('inicio')
    
    
    return render(request, 'ensayosMuestras.html',{
        'abreviatura': abreviatura,
        'form': form
    })


#Ver expedientes
def verExpedientes(request):

    #Sacamos los expedientes
    try:
        expedientes= Expedientes.objects.all().order_by()
    except ObjectDoesNotExist:
        print("no hay expedientes")

    



    return render(request, "verExpedientes.html",{
        'expedientes': expedientes
    } )


def expediente (request, nExpediente):

    #Sacamos el expediente
    try:
        expediente= Expedientes.objects.get(expediente=nExpediente)
    except ObjectDoesNotExist:
        print("No existe expediente")
    
    #Sacamos las muestras asignadas a ese expediente


    return render (request, "revisarExpediente.html", {
        "expediente": expediente
    })