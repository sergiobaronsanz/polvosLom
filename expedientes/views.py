from django.shortcuts import render, redirect, get_object_or_404
from expedientes.forms import ExpedientesForm, EmpresaForm, EnsayosMuestras
from django.http import JsonResponse
from .models import Empresa, Expedientes
from ensayos.models import *
from muestras.models import Muestras
from muestras.views import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.contrib.auth.decorators import login_required
from PDF.generarPdf import PDFGenerator
import os
import zipfile
import tempfile
import shutil
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Exists, OuterRef

import traceback
from django.http import HttpResponse, JsonResponse
from io import BytesIO



#Seleccion Expediente
@login_required
def nuevoExpediente(request): 
    if request.method == 'POST':
        form = ExpedientesForm(request.POST)
        if form.is_valid():
            expedienteForm= form.cleaned_data["expediente"].upper()
            empresaForm= form.cleaned_data["empresa"].upper()
            nMuestrasForm= form.cleaned_data["nMuestras"]
            abreviaturaForm= form.cleaned_data["abreviatura"].upper()
            
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
    expedientes= Expedientes.objects.all().order_by('estado', '-fecha')
        
    query_year= Expedientes.objects.values("fecha__year").distinct().order_by("-fecha__year")
    listaYears = [año['fecha__year'] for año in query_year]
    
    if request.method == "POST":

        filtro = request.POST.get("filtro")
        year = request.POST.get("year")

        expedientes= Expedientes.objects.all()

        if filtro:       
            expedientes= expedientes.filter(expediente__icontains=filtro)
        if year:
            expedientes= expedientes.filter(fecha__year= year)

        expedientes = expedientes.order_by('-fecha')
    
    return render(request, "verExpedientes.html",{
        'expedientes': expedientes,
        'listaYears': listaYears,
    } )


@login_required
def generadorZipConjunto(request):
    if request.method == 'POST':
        try:
            # Lógica para generar el archivo o procesar los datos
            datosJson = request.body.decode('utf-8')
            datosList = json.loads(datosJson)

            # Creamos una carpeta temporal donde se almacenarán todos los archivos
            final_folder = tempfile.mkdtemp()

            for resultadosMuestra in datosList:
                print(f"La lista es {resultadosMuestra}\n")
                pdf_gen = PDFGenerator(resultadosMuestra)

                # output es un archivo ZIP (BytesIO o path)
                output = pdf_gen.generateMuestra()

                # Crear carpeta temporal para descomprimir este ZIP
                with tempfile.TemporaryDirectory() as temp_unzip_dir:
                    # Si output es un archivo en disco
                    if isinstance(output, str):
                        zip_path = output
                    else:
                        # Si output es un BytesIO o similar, guardarlo en un archivo temporal
                        zip_path = os.path.join(temp_unzip_dir, 'temp.zip')
                        with open(zip_path, 'wb') as f:
                            f.write(output)

                    # Descomprimir el zip en el directorio temporal
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        zip_ref.extractall(temp_unzip_dir)

                    os.remove(zip_path)

                    # Copiar los archivos descomprimidos a la carpeta final
                    for filename in os.listdir(temp_unzip_dir):
                        filepath = os.path.join(temp_unzip_dir, filename)
                        if os.path.isfile(filepath):
                            extract_folder = os.path.join(final_folder, f"{resultadosMuestra[0]['muestra_nombre']}")
                            os.makedirs(extract_folder, exist_ok=True)
                            shutil.copy(filepath, os.path.join(extract_folder, filename))

            # Crear el zip final con todos los archivos combinados
            muestra = Muestras.objects.get(id=int(resultadosMuestra[0]['muestra_id']))
            expediente = muestra.expediente.expediente
            final_zip_name = f"{expediente}.zip"

            # Crear un archivo en memoria (en lugar de guardarlo en el disco)
            zip_buffer = BytesIO()

            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(final_folder):
                    for file in files:
                        file_path = os.path.join(root, file)
                        # Guardamos la ruta relativa para mantener la estructura dentro del ZIP
                        arcname = os.path.relpath(file_path, final_folder)
                        zipf.write(file_path, arcname=arcname)

            # Aseguramos que la posición del archivo en memoria esté al principio
            zip_buffer.seek(0)

            # Crear una respuesta HttpResponse con el archivo ZIP en memoria
            response = HttpResponse(zip_buffer, content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename="{final_zip_name}"'

            # Limpiar carpeta temporal final
            shutil.rmtree(final_folder)

            print(f"ZIP final creado en memoria con nombre: {final_zip_name}")

            return response

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
def expediente (request, expediente):

    #Sacamos el expediente
    expediente= get_object_or_404(Expedientes, id=expediente)
    #Sacamos las muestras asignadas a ese expediente
    muestras = Muestras.objects.filter(expediente=expediente).annotate(
        tiene_descripcion=Exists(DescripcionMuestra.objects.filter(muestra=OuterRef('pk')))
    )
    
    usuarios= get_list_or_404(User)


    ensayosMuestras=[]
    for muestra in muestras:
        #Sacamos la lista de los ensayos de las muestras
        resultados= listaEnsayosMuestra (muestra)
        
        #Sacamos la lista de los ensayos terminados
        ensayos= listaEnsayosTerminados(resultados, muestra)

        ensayosMuestras.append(ensayos)
    print(ensayosMuestras)
    
    #pasamos la variable a json para que se pueda leer en js
    ensayosMuestras_json= json.dumps(ensayosMuestras)
    expediente_json= json.dumps(expediente.id)
        
    return render (request, "revisarExpediente.html", {
        'expediente': expediente,
        'muestras': muestras,
        'ensayosMuestras_json': ensayosMuestras_json, 
        'expediente_json': expediente_json,
        "usuarios": usuarios,

    })

@login_required
def envioMail(request):
    if request.method == 'POST':
        try:
            #Recibimos los datos
            datosJson= request.body.decode('utf-8')
            datosList= json.loads(datosJson)
            id_expediente= datosList[0]['expediente']
            expediente= Expedientes.objects.get(id= id_expediente)
            muestras= get_list_or_404(Muestras, expediente= expediente)
            print(expediente)
            asuntosMuestras= []
            for muestra in muestras:
                abreviatura= muestra.empresa.abreviatura
                numeroMuestra= muestra.id_muestra
                asuntosMuestras.append(f"{abreviatura}-{numeroMuestra}")
            nExpediente=expediente.expediente
            empresa=expediente.empresa
            listaDestinatarios = [user.email for user in User.objects.all()]


            asunto= f"Resultados de {' , '.join(asuntosMuestras)} de la empresa {empresa} para el expediente {nExpediente}" 
            mensaje= f"Hola,\n\nYa tienes los resultados de {' , '.join(asuntosMuestras)}.\n\nUn saludo."
            remitente = settings.EMAIL_HOST_USER
            destinatarios = listaDestinatarios
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

@login_required
def eliminarExpediente (request, expediente):
    if request.POST:
        expediente= get_object_or_404(Expedientes, expediente=expediente)
        expediente.delete()
    return redirect("verExpedientes")


