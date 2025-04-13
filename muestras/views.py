
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from muestras.forms import DescripcionMuestraForm, MuestrasForm
from .models import Muestras, DescripcionMuestra
from ensayos.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
import json
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
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
@login_required
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
@login_required       
def verMuestra(request, muestra_id):
    
    muestra= get_object_or_404(Muestras, id= muestra_id)

    usuarios= get_list_or_404(User)

    print(usuarios)
    
    #Sacamos la descripción de la muestra
    descripcion= get_object_or_404(DescripcionMuestra, muestra=muestra)   
    
    #Sacamos los resultados 
    listaEnsayos= muestra.listaEnsayos.all()
    resultados= []

    #Para que aparezca el ensayo deberemos crear el ensayo (instanciandolo) en signals.py en Expedientes
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
    if listaEnsayos.filter(ensayo= "EMIsin").exists():
        resultado= EMIsin.objects.filter(muestra= muestra)
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
    if listaEnsayos.filter(ensayo= "tratamiento").exists():
        resultado= Tratamiento.objects.filter(muestra= muestra)
        print("tratamiento")
        resultados.extend(resultado)
    
    print(resultados)
        
    #print (resultados)
    #pasamos los datos a json para poder mandarlos al script de js
    ensayos=[]
    for resultado in resultados:
        if resultado.ensayo.ensayo != "Pmax":
            ensayo= resultado.ensayo
            muestra_id= muestra.id
            muestra_nombre= muestra.empresa.abreviatura + "-" + str(muestra.id_muestra)
            if resultado.ensayo.ensayo == "Tratamiento":
                if resultado.secado == "2" or resultado.molido=="2" or resultado.tamizado== "2": #Si hay algun tratamiento agregamos hoja tratamiento
                    ensayo_dict= {"ensayo":ensayo.ensayo, "muestra_id": muestra_id, "muestra_nombre": muestra_nombre} 
                    ensayos.append(ensayo_dict)
            #Si hay resultado agregamos las hojas 
            else:
                resultado_valor= resultado.resultado
                if resultado_valor:
                    ensayo_dict= {"ensayo":ensayo.ensayo, "muestra_id": muestra_id, "muestra_nombre": muestra_nombre} 
                    ensayos.append(ensayo_dict)
        else:
            if resultado.pmax:
                ensayo= resultado.ensayo
                muestra_id= muestra.id
                muestra_nombre= muestra.empresa.abreviatura + "-" + str(muestra.id_muestra)
                ensayo_dict= {"ensayo":ensayo.ensayo, "muestra_id": muestra_id, "muestra_nombre": muestra_nombre} 
                ensayos.append(ensayo_dict)

    #Sacamos los datos para js
    ensayos_json_str = json.dumps(ensayos)
    muestra_json_str= json.dumps(muestra_id)

    #Sacamos las url
    url_ensayosMuestras= reverse('ensayosMuestrasSimple', kwargs={'muestra': muestra_id})
    

    
    
    return render(request, 'verMuestra.html', {
        "muestra": muestra,
        "muestra_json": muestra_json_str,
        "descripcion": descripcion,
        "resultados": resultados,
        "ensayos_json":ensayos_json_str,
        "ensayos": ensayos,
        "url_ensayosMuestras": url_ensayosMuestras,
        "usuarios": usuarios,
    })