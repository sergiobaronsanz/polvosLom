
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from muestras.forms import DescripcionMuestraForm, MuestrasForm
from .models import Muestras, DescripcionMuestra
from ensayos.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
import json

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
        resultados.extend(resultado)
    if listaEnsayos.filter(ensayo= "tmin").exists():
        resultado= TMIn.objects.filter(muestra= muestra)
        resultados.extend(resultado)
    if listaEnsayos.filter(ensayo= "LIE").exists():
        resultado= LIE.objects.filter(muestra= muestra)
        print(resultado)
        resultados.extend(resultado)     
    if listaEnsayos.filter(ensayo= "EMI").exists():
        resultado= EMI.objects.filter(muestra= muestra)
        print(resultado)
        resultados.extend(resultado)   
    if listaEnsayos.filter(ensayo= "Pmax").exists():
        resultado= Pmax.objects.filter(muestra= muestra)
        print(resultado)
        resultados.extend(resultado) 
    if listaEnsayos.filter(ensayo= "CLO").exists():
        resultado= CLO.objects.filter(muestra= muestra)
        print("CLO")
        resultados.extend(resultado)  
    if listaEnsayos.filter(ensayo= "REC").exists():
        resultado= REC.objects.filter(muestra= muestra)
        print("REC")
        resultados.extend(resultado) 
    if listaEnsayos.filter(ensayo= "N1").exists():
        resultado= N1.objects.filter(muestra= muestra)
        print("N1")
        resultados.extend(resultado) 
    if listaEnsayos.filter(ensayo= "N2").exists():
        resultado= N2.objects.filter(muestra= muestra)
        print("N2")
        resultados.extend(resultado) 
    if listaEnsayos.filter(ensayo= "N4").exists():
        resultado= N4.objects.filter(muestra= muestra)
        print("N4")
        resultados.extend(resultado)
    if listaEnsayos.filter(ensayo= "O1").exists():
        resultado= O1.objects.filter(muestra= muestra)
        print("O1")
        resultados.extend(resultado)
    
        
    #print (resultados)
    #pasamos los datos a json para poder mandarlos al script de js
    ensayos_json=[]
    for resultado in resultados:
        if resultado.ensayo.ensayo != "Pmax":
            ensayo= resultado.ensayo
            muestra_id= muestra.id
            muestra_nombre= muestra.empresa.abreviatura + "-" + str(muestra.id_muestra)

            resultado_valor= resultado.resultado
            if resultado_valor:
                ensayo_dict= {"ensayo":ensayo.ensayo, "muestra_id": muestra_id, "muestra_nombre": muestra_nombre} 
                ensayos_json.append(ensayo_dict)
        else:
            if resultado.pmax:
                ensayo= resultado.ensayo
                muestra_id= muestra.id
                muestra_nombre= muestra.empresa.abreviatura + "-" + str(muestra.id_muestra)
                ensayo_dict= {"ensayo":ensayo.ensayo, "muestra_id": muestra_id, "muestra_nombre": muestra_nombre} 
                ensayos_json.append(ensayo_dict)

    #Sacamos los datos para js
    ensayos_json_str = json.dumps(ensayos_json)
    muestra_json_str= json.dumps(muestra_id)

    #Sacamos las url
    url_ensayosMuestras= reverse('ensayosMuestrasSimple', kwargs={'muestra': muestra_id})

    
    
    return render(request, 'verMuestra.html', {
        "muestra": muestra,
        "muestra_json": muestra_json_str,
        "descripcion": descripcion,
        "resultados": resultados,
        "ensayos_json":ensayos_json_str,
        "url_ensayosMuestras": url_ensayosMuestras,
    })