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
def generadorZipConjunto(request):#############################################################
    if request.method == 'POST':
        try:
            # Lógica para generar el archivo o procesar los datos
            datosJson= request.body.decode('utf-8')
            datosList= json.loads(datosJson)

            #creamos una caroeta temporal donde se almacenarán todos los archivos
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

                    # Copiar los archivos descomprimidos a la carpeta final
                    for filename in os.listdir(temp_unzip_dir):
                        filepath = os.path.join(temp_unzip_dir, filename)
                        if os.path.isfile(filepath):
                            shutil.copy(filepath, os.path.join(final_folder, filename))

            # Crear el zip final con todos los archivos combinados
            desktop = os.path.join(os.path.expanduser('~'), 'Desktop')  # o 'Desktop'
            final_zip_path = os.path.join(desktop, 'resultado_final.zip')
            with zipfile.ZipFile(final_zip_path, 'w') as zipf:
                for filename in os.listdir(final_folder):
                    filepath = os.path.join(final_folder, filename)
                    zipf.write(filepath, arcname=filename)

            # Limpieza opcional
            shutil.rmtree(final_folder)

            print(f"ZIP final creado en: {final_zip_path}")
            """for 
                output = pdf_gen.generate()

            # Guardar el resultado según la cantidad de archivos
            # Obtener la ruta al escritorio
            ruta_escritorio = os.path.join(os.path.expanduser("~"), "Desktop")

            # Verificar si la ruta del escritorio existe (por seguridad)
            if not os.path.exists(ruta_escritorio):
                raise FileNotFoundError("No se pudo encontrar el escritorio del usuario.")

            # Determinar el nombre del archivo según la condición

            id_archivo= datosList[0]['muestra_nombre']
            id_ensayo= datosList[0]['ensayo']
            print(len(datosList))

            nombre_archivo = f'{id_archivo}.zip' if len(datosList) > 1 else f"{id_archivo}-{id_ensayo}.pdf"

            print(nombre_archivo)
            # Construir la ruta completa del archivo
            ruta_archivo = os.path.join(ruta_escritorio, nombre_archivo)

            

            # Guardar el archivo en la ruta especificada
            with open(ruta_archivo, 'wb') as f:
                f.write(output) """              

            return JsonResponse({'mensaje': 'Archivo generado correctamente'})
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
def expediente (request, nExpediente):

    #Sacamos el expediente
    expediente= get_object_or_404(Expedientes, expediente=nExpediente)
    #Sacamos las muestras asignadas a ese expediente
    muestras= Muestras.objects.filter(expediente= expediente)

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
    '''        #Sacamos los datos para js
    ensayos_json_str = json.dumps(ensayos)
    muestra_json_str= json.dumps(muestra_id)###############'''
        
    return render (request, "revisarExpediente.html", {
        'expediente': expediente,
        'muestras': muestras,
        'ensayosMuestras_json': ensayosMuestras_json, 
    })


@login_required
def eliminarExpediente (request, expediente):
    if request.POST:
        expediente= get_object_or_404(Expedientes, expediente=expediente)
        expediente.delete()
    return redirect("verExpedientes")