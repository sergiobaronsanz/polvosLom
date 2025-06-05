
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from muestras.forms import DescripcionMuestraForm, MuestrasForm
from .models import Muestras, DescripcionMuestra
from ensayos.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
import json
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import traceback
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Exists, OuterRef

# Create your views here.
@login_required
def muestras(request):
      #Sacamos las muestras
    try:
        muestras= Muestras.objects.all().order_by('-fecha').annotate(
            tiene_descripcion= Exists(DescripcionMuestra.objects.filter(muestra= OuterRef('pk')))
        )
    except ObjectDoesNotExist:
        print("no hay muestras")
    
    if request.POST:
        filtro= request.POST["filtro"]
        muestras= Muestras.objects.filter(empresa__abreviatura__icontains=filtro).order_by('-fecha')
    
    return render(request, 'muestras.html', {
        'muestras': muestras
    })
@login_required
def recepcionMuestra(request, muestra="nueva"):
    if request.method == 'POST':
        if muestra != "nueva":
            muestra_obj = Muestras.objects.get(id=muestra)
            descripcion_existente = DescripcionMuestra.objects.get(muestra=muestra_obj)
            form = DescripcionMuestraForm(request.POST, request.FILES, instance=descripcion_existente)
        else:
            form = DescripcionMuestraForm(request.POST, request.FILES)

        if form.is_valid():
            descripcion = form.save(commit=False)

            # Si no se subieron nuevas imágenes, conservar las anteriores
            if muestra != "nueva":
                if not request.FILES.get('imagenMuestra'):
                    descripcion.imagenMuestra = descripcion_existente.imagenMuestra
                if not request.FILES.get('imagenEnvoltorio'):
                    descripcion.imagenEnvoltorio = descripcion_existente.imagenEnvoltorio

            descripcion.save()

            if muestra == "nueva":
                # Actualizar estado de la muestra
                muestra_obj = descripcion.muestra
                muestra_obj.estado = "3"
                muestra_obj.save()

                # Cambiar estado del expediente si todas las muestras están en estado "3"
                expediente = muestra_obj.expediente
                muestras = Muestras.objects.filter(expediente=expediente)
                if all(m.estado == "3" for m in muestras):
                    expediente.estado = "3"
                    expediente.save()

            return redirect('verMuestra', str(muestra_obj.id))

    else:
        if muestra != "nueva":
            muestraEnsayo = Muestras.objects.get(id=muestra)
            descripcion = DescripcionMuestra.objects.get(muestra=muestraEnsayo)
            form = DescripcionMuestraForm(instance=descripcion)
            form.fields['muestra'].queryset = Muestras.objects.filter(id=muestraEnsayo.id)
        else:
            form = DescripcionMuestraForm()
            form.fields['muestra'].queryset = Muestras.objects.filter(descripcionmuestra__isnull=True)

    return render(request, 'recepcionMuestra.html', {'form': form})

#Devuelve una lista con los ensayos que están 
def listaEnsayosMuestra(muestra):
    #Para que aparezca el ensayo deberemos crear el ensayo (instanciandolo) en signals.py en Expedientes
    listaEnsayos= muestra.listaEnsayos.all()
    resultados= []

    if listaEnsayos.filter(ensayo__iexact= "humedad").exists():
        resultado= Humedad.objects.filter(muestra= muestra)
        resultados.extend(resultado)
    if listaEnsayos.filter(ensayo__iexact= "granulometria").exists():
        resultado= Granulometria.objects.filter(muestra= muestra)
        resultados.extend(resultado)
    if listaEnsayos.filter(ensayo__iexact= "tmic").exists():
        resultado= TMIc.objects.filter(muestra= muestra)
        resultados.extend(resultado)
    if listaEnsayos.filter(ensayo__iexact= "tmin").exists():
        resultado= TMIn.objects.filter(muestra= muestra)
        resultados.extend(resultado)
    if listaEnsayos.filter(ensayo__iexact= "LIE").exists():
        resultado= LIE.objects.filter(muestra= muestra)
        print(resultado)
        resultados.extend(resultado)     
    if listaEnsayos.filter(ensayo__iexact= "EMI").exists():
        resultado= EMI.objects.filter(muestra= muestra)
        print(resultado)
        resultados.extend(resultado)
    if listaEnsayos.filter(ensayo__iexact= "EMIsin").exists():
        resultado= EMIsin.objects.filter(muestra= muestra)
        print(resultado)
        resultados.extend(resultado)   
    if listaEnsayos.filter(ensayo__iexact= "Pmax").exists():
        resultado= Pmax.objects.filter(muestra= muestra)
        print(resultado)
        resultados.extend(resultado) 
    if listaEnsayos.filter(ensayo__iexact= "CLO").exists():
        resultado= CLO.objects.filter(muestra= muestra)
        print("CLO")
        resultados.extend(resultado)  
    if listaEnsayos.filter(ensayo__iexact= "REC").exists():
        resultado= REC.objects.filter(muestra= muestra)
        print("REC")
        resultados.extend(resultado) 
    if listaEnsayos.filter(ensayo__iexact= "N1").exists():
        resultado= N1.objects.filter(muestra= muestra)
        print("N1")
        resultados.extend(resultado) 
    if listaEnsayos.filter(ensayo__iexact= "N2").exists():
        resultado= N2.objects.filter(muestra= muestra)
        print("N2")
        resultados.extend(resultado) 
    if listaEnsayos.filter(ensayo__iexact= "N4").exists():
        resultado= N4.objects.filter(muestra= muestra)
        print("N4")
        resultados.extend(resultado)
    if listaEnsayos.filter(ensayo__iexact= "O1").exists():
        resultado= O1.objects.filter(muestra= muestra)
        print("O1")
        resultados.extend(resultado)
    if listaEnsayos.filter(ensayo__iexact= "tratamiento").exists():
        resultado= Tratamiento.objects.filter(muestra= muestra)
        print("tratamiento")
        resultados.extend(resultado)

    return resultados

def listaEnsayosTerminados(resultados, muestra):
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
                if resultado_valor is not None:
                    ensayo_dict= {"ensayo":ensayo.ensayo, "muestra_id": muestra_id, "muestra_nombre": muestra_nombre} 
                    ensayos.append(ensayo_dict)
        else:
            if resultado.pmax is not None:
                ensayo= resultado.ensayo
                muestra_id= muestra.id
                muestra_nombre= muestra.empresa.abreviatura + "-" + str(muestra.id_muestra)
                ensayo_dict= {"ensayo":ensayo.ensayo, "muestra_id": muestra_id, "muestra_nombre": muestra_nombre} 
                ensayos.append(ensayo_dict)

    return ensayos
    
@login_required       
def verMuestra(request, muestra_id):
    
    muestra= get_object_or_404(Muestras, id= muestra_id)
    expediente= muestra.expediente

    usuarios= get_list_or_404(User)
    
    #Sacamos la descripción de la muestra
    descripcion= get_object_or_404(DescripcionMuestra, muestra=muestra)   
    
    #Sacamos la lista de los ensayos de las muestras
    resultados= listaEnsayosMuestra (muestra)
    
    #Sacamos la lista de los ensayos terminados
    ensayos= listaEnsayosTerminados(resultados, muestra)

    #Sacamos los datos para js
    ensayos_json_str = json.dumps(ensayos)
    muestra_json_str= json.dumps(muestra_id)

    #Sacamos las url
    url_ensayosMuestras= reverse('ensayosMuestrasSimple', kwargs={'muestra': muestra_id})
    url_descripcionMuestra= reverse('recepcionMuestra', kwargs={'muestra': muestra_id})
    
    
    
    return render(request, 'verMuestra.html', {
        "muestra": muestra,
        "muestra_json": muestra_json_str,
        "descripcion": descripcion,
        "resultados": resultados,
        "ensayos_json":ensayos_json_str,
        "ensayos": ensayos,
        "url_ensayosMuestras": url_ensayosMuestras,
        "url_descripcionMuestra": url_descripcionMuestra,
        "usuarios": usuarios,
        "expediente": expediente,
    })

@login_required
def envioMail(request):
    if request.method == 'POST':
        try:
            #Recibimos los datos
            datosJson= request.body.decode('utf-8')
            datosList= json.loads(datosJson)
            id_muestra= datosList[0]['muestra']
            muestra= Muestras.objects.get(id= id_muestra)
            print(muestra)
            abreviatura= muestra.empresa.abreviatura
            numeroMuestra= muestra.id_muestra
            expediente=muestra.expediente
            empresa=muestra.empresa.empresa

            asunto= f"Resultados de {abreviatura}-{numeroMuestra} de la empresa {empresa} para el expediente {expediente}" 
            mensaje= f"Hola,\n\nYa tienes los resultados de {abreviatura}-{numeroMuestra}.\n\nUn saludo."
            remitente = settings.EMAIL_HOST_USER
            destinatarios = ['s.baronsanz@gmail.com']
            print(mensaje)
    
            send_mail(asunto, mensaje, remitente, destinatarios, fail_silently=False)

            return JsonResponse({'mensaje': 'Email enviado'})

        except Exception as e:
            # Captura y devuelve la traza completa del error
            traza_error = traceback.format_exc()
            print(traza_error)  # Muestra la traza en la consola del servidor

            return JsonResponse({
                'error': 'Error interno del servidor',
                'detalle': str(e),
                'traza': traza_error  # Incluye la traza en la respuesta
            }, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)


#Función para marcar los ensayos como revisados
def revisionMuestra(request):
    if request.method == "POST":
        try:
            #Recibimos los datos
            datosJson= request.body.decode('utf-8')
            idMuestra= datosJson
            print(idMuestra)
            muestra= get_object_or_404(Muestras, id= idMuestra)

            #Guardamos el nuevo estado de la muestra: Finalizada
            muestra.estado= "5"
            muestra.save()
            print("Muestra revisada")

            #Comprobamos si todas las muestras del estado de expedientes están terminadas
            expediente= muestra.expediente
            muestras= get_list_or_404(Muestras, expediente= expediente)
            print(muestras)

            listadoEstadoMuestras= []
            for muestra in muestras:
                if muestra.estado=="5":
                    listadoEstadoMuestras.append(True)
                else:
                    listadoEstadoMuestras.append(False)

            
            print(listadoEstadoMuestras)
            
            if all(listadoEstadoMuestras):
                expediente.estado="5"
                expediente.save()

            
            return JsonResponse({'mensaje': 'revisiónRealizada'})

        except Exception as e:
            # Captura y devuelve la traza completa del error
            traza_error = traceback.format_exc()
            print(traza_error)  # Muestra la traza en la consola del servidor

            return JsonResponse({
                'error': 'Error interno del servidor',
                'detalle': str(e),
                'traza': traza_error  # Incluye la traza en la respuesta
            }, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
@login_required
def cambiarIdMuestra(request, id_muestra):
    print("borrar")
    muestra= get_object_or_404(Muestras, id= id_muestra)
    
    if request.method == "POST":
        nuevoId= request.POST["nuevoId"]

        muestra.id_muestra= nuevoId
        muestra.save()
        
        return redirect ('verMuestra', muestra.id)
    
    return render(request, 'cambio.html', {
        'muestra': muestra,
    })
    

@login_required
def eliminarMuestra (request, muestra):
    muestra= get_object_or_404(Muestras, id= muestra)
    expediente= muestra.expediente
    muestra.delete()

    nMuestras= Muestras.objects.filter(expediente= expediente)

    if nMuestras:
        return redirect('revisarExpediente', expediente.id)
    
    else:
        expediente.delete()
        return redirect('inicio')

    