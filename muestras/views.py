
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from muestras.forms import DescripcionMuestraForm, MuestrasForm
from .models import Muestras, DescripcionMuestra
from ensayos.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

# Create your views here.

def muestras(request):
      #Sacamos las muestras
    try:
        muestras= Muestras.objects.all().order_by('-fecha')
    except ObjectDoesNotExist:
        print("no hay muestras")
    
    if request.POST:
        filtro= request.POST["filtro"]
        muestras= Muestras.objects.filter(empresa__abreviatura__icontains=filtro).order_by('-fecha')
    
    return render(request, 'muestras.html', {
        'muestras': muestras
    })

def recepcionMuestra(request):
    if request.method == 'POST':
        form = DescripcionMuestraForm(request.POST, request.FILES)
        if form.is_valid():
            # Guardar el formulario si es válido
            form.save()
            
            #Actualizar el estado de la muestra
            id_muestra= request.POST['muestra']
            muestra= Muestras.objects.get(id= id_muestra)
            muestra.estado= "3"
            muestra.save()

            redirect('muestras')
            
            
    else:
        form = DescripcionMuestraForm()

    return render(request, 'recepcionMuestra.html', {'form': form})
    
    
def verMuestra(request, muestra_id):
    
    muestra= get_object_or_404(Muestras, id= muestra_id)
    
    #Sacamos la descripción de la muestra
    descripcion= get_object_or_404(DescripcionMuestra, muestra=muestra)   
    
    #Sacamos los resultados 
    listaEnsayos= muestra.listaEnsayos.all()
    resultados= []

    if listaEnsayos.filter(ensayo= "humedad").exists():
        resultado= Humedad.objects.filter(muestra= muestra)
        resultados.extend(resultado)
    if listaEnsayos.filter(ensayo= "granulometria").exists():
        resultado= Granulometria.objects.filter(muestra= muestra)
        resultados.extend(resultado)
    if listaEnsayos.filter(ensayo= "tmic").exists():
        resultado= TMIc.objects.filter(muestra= muestra)
        print(resultado)
        resultados.extend(resultado)
    if listaEnsayos.filter(ensayo= "tmin").exists():
        resultado= TMIn.objects.filter(muestra= muestra)
        print(resultado)
        resultados.extend(resultado)
    
        

    #Sacamos las url
    url_ensayosMuestras= reverse('ensayosMuestrasSimple', kwargs={'muestra': muestra_id})

    
    
    return render(request, 'verMuestra.html', {
        "muestra": muestra,
        "descripcion": descripcion,
        "resultados": resultados,
        "url_ensayosMuestras": url_ensayosMuestras,
    })