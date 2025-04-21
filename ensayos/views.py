from django.shortcuts import render, get_list_or_404, get_object_or_404
from .forms import *
from .models import *
from muestras.models import ListaEnsayos, Muestras
from django.db.models import Q
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt  # Necesario si no manejas CSRF (solo en desarrollo)
from PDF.generarPdf import PDFGenerator
import traceback
import os
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from calidad.models import Equipos
from calidad.forms import *

from django.contrib.auth.decorators import login_required

@login_required
def generadorPdf(request):
    if request.method == 'POST':
        try:
            # Lógica para generar el archivo o procesar los datos
            datosJson= request.body.decode('utf-8')
            datosList= json.loads(datosJson)
            print(f"la lista de datos es: {datosList}")

            pdf_gen= PDFGenerator(datosList)
            output = pdf_gen.generateMuestra()

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
                f.write(output)               

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

#Lista Ensayos
@login_required
def listaEnsayos(request):
    listaEnsayos= ListaEnsayos.objects.all()
    
    return render (request, "ensayos/listaEnsayos/listaEnsayos.html",{
        'ensayos': listaEnsayos,
    })
@login_required
def ensayosRealizados(request, ensayo):
    ensayo_id= ListaEnsayos.objects.get(ensayo=ensayo)
    print(ensayo_id.ensayo)
    #filtramos por tipo de ensayo

    if ensayo_id.ensayo == "Humedad":
        resultados= Humedad.objects.all()
    elif ensayo_id.ensayo== "Granulometria":
        resultados= Granulometria.objects.all()
    elif ensayo_id.ensayo== "TMIc":
        resultados= TMIc.objects.all()
    elif ensayo_id.ensayo== "TMIn":
        resultados= TMIn.objects.all()
    elif ensayo_id.ensayo== "LIE":
        resultados= LIE.objects.all()
    elif ensayo_id.ensayo== "EMI":
        resultados= EMI.objects.all()
    elif ensayo_id.ensayo== "Pmax":
        resultados= Pmax.objects.all()
    else:
        resultados= None
    
    print(resultados)
    #resultados= Resultados.objects.filter(ensayo= ensayo_id)
    
    return render(request, "ensayos/listaEnsayos/ensayosRealizados.html",{
        'resultados': resultados,
        'ensayo': ensayo,
    })

#Ensayos
@login_required
def humedad(request, muestra_id): #################################### Hay que cambiar muestras_id por humedad_id para así poder tener varias humedades en una misma muestra
    #Sacamos el ensayo
    ensayo= get_object_or_404(ListaEnsayos, ensayo= "humedad")
    equipos=get_list_or_404(Equipos, ensayos= ensayo) 
    datosGuardados=False 
    usuario= request.user


    #Filtramos las muestras que pueden salir
    muestras_queryset= Muestras.objects.filter(
        Q(humedad__resultado__isnull=True) & Q(listaEnsayos__ensayo__icontains="humedad") & ~Q(estado=1)
    )
    
    if request.method == 'POST':
               
        form = HumedadForm(request.POST)
        equiposEnsayo= EquiposEnsayoForm(request.POST, prefix='equiposEnsayo')
        print(form.errors)

        if form.is_valid() and equiposEnsayo.is_valid():
            muestra= get_object_or_404(Muestras, id= request.POST.get('muestra'))         

            if form.cleaned_data:
                #Agregamos los campos
                fechaInicio= form.cleaned_data['fechaInicio']
                fechaFin= form.cleaned_data['fechaFin']
                temperaturaAmbiente= form.cleaned_data['temperaturaAmbiente']
                humedad= form.cleaned_data['humedad']
                criterio= form.cleaned_data['criterio']
                tiempoEnsayo= form.cleaned_data['tiempoEnsayo']
                tDesecacion= form.cleaned_data['tDesecacion']
                desviacion= form.cleaned_data['desviacion']
                resultado1= form.cleaned_data['resultado1'].replace(",", ".")
                resultado2= form.cleaned_data['resultado2'].replace(",", ".")
                resultado3= form.cleaned_data['resultado3'].replace(",", ".")
                resultado4= form.cleaned_data['resultado4'].replace(",", ".")
                resultado5= form.cleaned_data['resultado5'].replace(",", ".")
                resultado6= form.cleaned_data['resultado6'].replace(",", ".")
                resultado7= form.cleaned_data['resultado7'].replace(",", ".")
                resultado8= form.cleaned_data['resultado8'].replace(",", ".")
                resultado9= form.cleaned_data['resultado9'].replace(",", ".")
                resultado10= form.cleaned_data['resultado10'].replace(",", ".")
                observacion= form.cleaned_data['observacion']
            
            
            #Comprobamos que no exista un ensayo de humedad previo
            humedad_instancia= Humedad.objects.filter(muestra= muestra)
            humedad_instancia.delete()
            
            
            #Si tiempo desecacion no es "" lo añadimos
            if tiempoEnsayo:
                tiempoEnsayo= float(tiempoEnsayo)
                humedad.tiempoEnsayo=tiempoEnsayo
            
            #Sacamos la media del resultado 
            if resultado1 != "N/D":  
                resultado= 0
                listaResultados=[]
                
                if float(desviacion) >= 0.15:
                    listaResultados = [
                        resultado1, resultado2, resultado3,
                        resultado4, resultado5, resultado6,
                        resultado7, resultado8, resultado9,
                        resultado10,
                    ]
                    
                    longitud_lista= len(listaResultados)
                    
                    sumatorio=0
                    for valor in listaResultados:
                        sumatorio += float(valor)
                        resultado= sumatorio/longitud_lista
                else:
                    listaResultados = [
                        resultado1, resultado2, resultado3,
                    ]
                    
                    longitud_lista= len(listaResultados)
                    
                    sumatorio=0
                    for valor in listaResultados:
                        sumatorio += float(valor)
                        resultado= sumatorio/longitud_lista
                
                #Guardamos los valores en la tabla resultados                
                resultado= round(resultado, 2)  

            else:
                resultado = "N/D"
                listaResultados = [resultado1, resultado2, resultado3]

            #Guardamos los datos en el servidor
            humedad= Humedad.objects.create(
                muestra= muestra,
                fechaInicio= fechaInicio, 
                fechaFin= fechaFin, 
                ensayo= ensayo,
                temperaturaAmbiente= temperaturaAmbiente,
                humedad= humedad,
                tDesecacion= tDesecacion,
                criterio= criterio,
                desviacion=desviacion,
                observacion= observacion,
                resultado= resultado,
                usuario= usuario,
            )

            for valor in listaResultados:
                    resultado= ResultadosHumedad.objects.create(
                        ensayo= humedad,
                        resultado= valor,
                    )
                    
            #Añadimos los equipos
            equipos= equiposEnsayo.cleaned_data['equiposEnsayo']
            humedad.equipos.set (equipos)

            datosGuardados= True
            print(f"datos guardados {datosGuardados}")
        else:
            print (form.errors)
            form.add_error(None, f'Error en el formulario, revisa los datos {form.errors}')
    else:
        if muestra_id != "nueva":
            ensayo= Humedad.objects.get(muestra__id= muestra_id)
            resultados= ResultadosHumedad.objects.filter(ensayo=ensayo).order_by('id')
            equipos=ensayo.equipos.all() 
            
            
            muestra= Muestras.objects.get(id=muestra_id) 
            fechaInicio= str(ensayo.fechaInicio)
            fechaFin= str(ensayo.fechaFin)
            temperaturaAmbiente= ensayo.temperaturaAmbiente
            humedad=ensayo.humedad
            criterio= ensayo.criterio
            tiempoEnsayo= ensayo.tiempoEnsayo
            tDesecacion= ensayo.tDesecacion
            desviacion= ensayo.desviacion
            
            resultado1=0
            
            print(resultados)
            if resultados.exists():
                if len(resultados) <= 3:
                    resultado1= resultados[0].resultado
                    resultado2= resultados[1].resultado
                    resultado3= resultados[2].resultado
                    resultado4= ""
                    resultado5= ""
                    resultado6= ""
                    resultado7= ""
                    resultado8= ""
                    resultado9= ""
                    resultado10= ""
                else:
                    resultado1= resultados[0].resultado
                    resultado2= resultados[1].resultado
                    resultado3= resultados[2].resultado
                    resultado4= resultados[0].resultado
                    resultado5= resultados[1].resultado
                    resultado6= resultados[2].resultado
                    resultado7= resultados[0].resultado
                    resultado8= resultados[1].resultado
                    resultado9= resultados[2].resultado
                    resultado10= resultados[2].resultado

                form = HumedadForm(initial={
                    'muestra': muestra,
                    'fechaInicio': fechaInicio,
                    'fechaFin': fechaFin,
                    'temperaturaAmbiente': temperaturaAmbiente,
                    'humedad': humedad,
                    'criterio':criterio,
                    'tiempoEnsayo':tiempoEnsayo,
                    'tDesecacion': tDesecacion,
                    'desviacion': desviacion,
                    'resultado1': resultado1,
                    'resultado2': resultado2,
                    'resultado3': resultado3,
                    'resultado4': resultado4,
                    'resultado5': resultado5,
                    'resultado6': resultado6,
                    'resultado7': resultado7,
                    'resultado8': resultado8,
                    'resultado9': resultado9,
                    'resultado10': resultado10,
                    })
            else:
                form = HumedadForm(initial={
                    'muestra': muestra,
                    })
                
            form.fields['muestra'].queryset = Muestras.objects.filter(id=muestra_id)
            equiposEnsayo = EquiposEnsayoForm(prefix='equiposEnsayo',initial={'equiposEnsayo': equipos})
            
        else:
            form = HumedadForm()
            form.fields['muestra'].queryset = muestras_queryset

            equiposEnsayo = EquiposEnsayoForm(prefix='equiposEnsayo',initial={'equiposEnsayo': equipos})
            

    return render(request, 'ensayos/nuevosEnsayos/humedad.html', {
        'form': form, 
        'ensayo': ensayo,
        'equiposEnsayo': equiposEnsayo,
        'datosGuardados': datosGuardados,
        })

@login_required
def granulometria(request, muestra_id):
    #Sacamos el ensayo
    ensayo= get_object_or_404(ListaEnsayos, ensayo= "granulometria")
    equipos= get_object_or_404(Equipos, ensayos= ensayo)
    id_ensayo= muestra_id
    datosGuardados= False  
    nombreArchivo= None
    usuario= request.user

    #Filtramos las muestras que pueden salir
    muestras_queryset= Muestras.objects.filter(
        Q(granulometria__resultado__isnull=True) & Q(listaEnsayos__ensayo__icontains="granulometria") & ~Q(estado=1)
    )

    if request.method == 'POST':
        form= GranulometriaForm(request.POST, request.FILES)
        equiposEnsayo = EquiposEnsayoForm(request.POST, prefix='equipos')

        if form.is_valid() and equiposEnsayo.is_valid():
            #Recogemos los datos para guardarlos
            muestra= get_object_or_404(Muestras, id= request.POST.get('muestra'))
                      

            #Agregamos los campos
            fechaInicio= request.POST.get('fechaInicio')
            fechaFin= request.POST.get('fechaFin')
            temperaturaAmbiente= float(request.POST.get('temperaturaAmbiente'))
            humedad= float(request.POST.get('humedad'))
            via= float(request.POST.get('via'))
            d10= float(request.POST.get('d10'))
            d50= float(request.POST.get('d50'))
            d90= float(request.POST.get('d90'))
            archivo=request.FILES.get("archivo")

            #Comprobamos que no exista un ensayo de humedad previo
            granulometria_instancia= Granulometria.objects.filter(muestra= muestra)
            granulometria_instancia.delete()

            granulometria= Granulometria.objects.create(
                muestra=muestra,
                ensayo=ensayo,
                temperaturaAmbiente= temperaturaAmbiente,
                humedad= humedad,
                fechaInicio= fechaInicio,
                fechaFin= fechaFin,
                via= via,
                d10=d10,
                d50= d50,
                d90= d90,
                resultado= d50,
                archivo= archivo,
                usuario= usuario,

            )        

            equipos= equiposEnsayo.cleaned_data['equiposEnsayo']
            granulometria.equipos.set (equipos)

            datosGuardados= True
            nombreArchivo= archivo
        else:
            form.add_error(None, f'Error en el formulario, revisa los datos {form.errors}')
    
    else:
        if muestra_id != 'nueva':
            ensayo= Granulometria.objects.get(muestra__id= muestra_id)            
            
            muestra= Muestras.objects.get(id=muestra_id) 
            fechaInicio= str(ensayo.fechaInicio)
            fechaFin= str(ensayo.fechaFin)
            temperaturaAmbiente= ensayo.temperaturaAmbiente
            humedad=ensayo.humedad
            via= ensayo.via
            d10= ensayo.d10
            d50= ensayo.d50
            d90= ensayo.d90
            archivo= ensayo.archivo
            print(archivo)
            
            
            form = GranulometriaForm(initial={
                'muestra': muestra,
                'fechaInicio': fechaInicio,
                'fechaFin': fechaFin,
                'temperaturaAmbiente': temperaturaAmbiente,
                'humedad': humedad,
                'via':via,
                'd10': d10,
                'd50': d50,
                'd90': d90,
                'archivo': archivo,
                })
            
            form.fields['muestra'].queryset = Muestras.objects.filter(id=muestra_id)
            equiposEnsayo = EquiposEnsayoForm(prefix='equipos',initial={'equiposEnsayo': equipos})

        else:
            form= GranulometriaForm()
            form.fields['muestra'].queryset = muestras_queryset

            equiposEnsayo = EquiposEnsayoForm(prefix='equipos',initial={'equiposEnsayo': equipos})


    return render(request, 'ensayos/nuevosEnsayos/granulometria.html', {
        'ensayo': ensayo,
        'form': form,
        'equiposEnsayo': equiposEnsayo,
        'datosGuardados': datosGuardados,
        'nombreArchivo': nombreArchivo,
    })

@login_required
def tmic(request, muestra_id):
    #Sacamos el ensayo
    ensayo= get_object_or_404(ListaEnsayos, ensayo= "TMIc")   
    equipos=get_list_or_404(Equipos, ensayos= ensayo) 
    datosGuardados=False  
    usuario= request.user 
  
    #Filtramos las muestras que pueden salir
    muestras_queryset= Muestras.objects.filter(
        Q(tmic__resultado__isnull=True) & Q(listaEnsayos__ensayo__icontains="tmic") & ~Q(estado=1)
    )

    if request.method == 'POST':
        #Recibimos los formularios diferenciándolos con el prefijo
        formTmic= TmicForm(request.POST, prefix='tmic')
        formTmicResultados= tmicResultadosFormSet(request.POST, prefix='tmicResultados') 
        equiposEnsayo= EquiposEnsayoForm(request.POST, prefix='equipos')

        
        if formTmic.is_valid() and formTmicResultados.is_valid() and equiposEnsayo.is_valid():
            muestra= get_object_or_404(Muestras, id= request.POST.get('tmic-muestra'))
            
            
            #Comprobamos que no exista un ensayo de humedad previo
            tmic_instancia= TMIc.objects.filter(muestra= muestra)
            tmic_instancia.delete()

            
            #Guardamos el formulario de la capa a falta del resultado final
            fechaInicio= formTmic.cleaned_data['fechaInicio']
            fechaFin= formTmic.cleaned_data['fechaFin']
            temperaturaAmbiente= formTmic.cleaned_data['temperaturaAmbiente']
            humedad= formTmic.cleaned_data['humedad']
            tiempoMaxEnsayo= formTmic.cleaned_data['tiempoMaxEnsayo']
            observacion=formTmic.cleaned_data['observacion']

            tmic= TMIc.objects.create(
                muestra=muestra,
                ensayo=ensayo,
                temperaturaAmbiente= temperaturaAmbiente,
                humedad= humedad,
                fechaInicio= fechaInicio,
                fechaFin= fechaFin,
                tiempoMaxEnsayo=tiempoMaxEnsayo,
                observacion= observacion,
                usuario= usuario,
            )
            equipos= equiposEnsayo.cleaned_data['equiposEnsayo']
            tmic.equipos.set (equipos)

            #Eliminamos los resultados
            resultadosAnteriores= ResultadosTMIc.objects.filter(ensayo= tmic)
            if resultadosAnteriores:
                for resultado in resultadosAnteriores:
                    resultado.delete()

            
            #Guardamos los resultados en la tabla de resultados TMIc 
            listaResultados= []  

            for form in formTmicResultados:
                if form.cleaned_data:  # Para evitar formularios vacíos
                    tPlato = form.cleaned_data['tPlato']
                    tMax = form.cleaned_data['tMax']
                    resultadoPrueba= form.cleaned_data['resultadoPrueba']
                    tipoIgnicion= form.cleaned_data['tipoIgnicion']
                    tiempoPrueba= form.cleaned_data['tiempoPrueba']
                    tiempoMax= form.cleaned_data['tiempoMax']



                    resultadosTmic=ResultadosTMIc.objects.create(
                        ensayo=tmic,
                        tPlato=tPlato,
                        tMaxima=tMax,
                        resultado=resultadoPrueba,
                        tipoIgnicion= tipoIgnicion,
                        tiempoPrueba=tiempoPrueba,
                        tiempoTmax=tiempoMax,
                    )

                    if resultadoPrueba == "1" or resultadoPrueba== "3":
                        listaResultados.append(tPlato)
                    
                    if resultadoPrueba == "3":
                        tmic.funde= "1"

            #Guardamos en el modelo TMIc el resultado del ensayo
            if listaResultados:
                resultado= min(listaResultados)
                tmic.resultado= resultado
                tmic.save()
            else:
                resultado= ">400"
                tmic.resultado= resultado
                tmic.save()

            datosGuardados= True            
        else:
            print (formTmic.errors)
            formTmic.add_error(None, 'Error en el formulario, revisa los datos')
            formTmicResultados.add_error(None, 'Error en el formulario, revisa los datos')

            return render(request, 'ensayos/nuevosEnsayos/tmic.html', {
                'ensayo': ensayo,
                'formTmic': formTmic,
                'equiposEnsayo': equiposEnsayo,
        'datosGuardados': datosGuardados,
                'formTmicResultados': formTmicResultados,
            })
    else:
        if muestra_id != 'nueva':
            ensayo_TMIc= TMIc.objects.get(muestra__id= muestra_id)            
            equipos=ensayo_TMIc.equipos.all() 

            muestra= Muestras.objects.get(id=muestra_id) 
            fechaInicio= str(ensayo_TMIc.fechaInicio)
            fechaFin= str(ensayo_TMIc.fechaFin)
            temperaturaAmbiente= ensayo_TMIc.temperaturaAmbiente
            humedad=ensayo_TMIc.humedad
            tiempoMaxEnsayo= ensayo_TMIc.tiempoMaxEnsayo
            observacion= ensayo_TMIc.observacion
            
            

            formTmic = TmicForm(prefix='tmic', initial={
                'muestra': muestra,
                'fechaInicio': fechaInicio,
                'fechaFin': fechaFin,
                'temperaturaAmbiente': temperaturaAmbiente,
                'humedad': humedad,
                'tiempoMaxEnsayo': tiempoMaxEnsayo,
                'observacion': observacion,
                })
            
            formTmic.fields['muestra'].queryset = Muestras.objects.filter(id=muestra_id)

            resultados= ResultadosTMIc.objects.filter(ensayo=ensayo_TMIc).order_by("id")

            initial_data = []
            for resultado in resultados:
                initial_data.append({
                    'tPlato': resultado.tPlato,
                    'tMax': resultado.tMaxima,
                    'resultadoPrueba': resultado.resultado,
                    'tipoIgnicion': resultado.tipoIgnicion,
                    'tiempoPrueba': resultado.tiempoPrueba,
                    'tiempoMax': resultado.tiempoTmax,
                })
            
            # Crear el formset con los datos iniciales
            TmicResultadosFormSet = formset_factory(TmicResultadosForm, extra=0)
            formTmicResultados = TmicResultadosFormSet(prefix='tmicResultados',initial=initial_data)

            equiposEnsayo = EquiposEnsayoForm(prefix='equipos',initial={'equiposEnsayo': equipos})

        
        else:
            formTmic= TmicForm(prefix='tmic')
            formTmic.fields['muestra'].queryset = muestras_queryset

            formTmicResultados=tmicResultadosFormSet(prefix='tmicResultados')            

            equiposEnsayo = EquiposEnsayoForm(prefix='equipos',initial={'equiposEnsayo': equipos})

    return render(request, 'ensayos/nuevosEnsayos/tmic.html', {
        'ensayo': ensayo,
        'formTmic': formTmic,
        'equiposEnsayo': equiposEnsayo,
        'datosGuardados': datosGuardados,
        'formTmicResultados': formTmicResultados,
        
    })

@login_required
def tmin (request, muestra_id):
     #Sacamos el ensayo
    ensayo= get_object_or_404(ListaEnsayos, ensayo= "TMIn")
    equipos=get_list_or_404(Equipos, ensayos= ensayo) 
    datosGuardados=False  
    usuario= request.user
  
    #Filtramos las muestras que pueden salir
    muestras_queryset= Muestras.objects.filter(
        Q(tmin__resultado__isnull=True) & Q(listaEnsayos__ensayo__icontains="tmin") & ~Q(estado=1)
    )

    if request.method == 'POST':
        #Recibimos los formularios diferenciándolos con el prefijo
        formTmin= TminForm(request.POST, prefix='tmin')
        formTminResultados= tminResultadosFormSet(request.POST, prefix='tminResultados') 
        equiposEnsayo= EquiposEnsayoForm(request.POST, prefix='equipos')
 
        
        if formTmin.is_valid() and formTminResultados.is_valid() and equiposEnsayo.is_valid():

            muestra= get_object_or_404(Muestras, id= request.POST.get('tmin-muestra'))
            
            #Comprobamos que no exista un ensayo  previo
            tmin_instancia= TMIn.objects.filter(muestra= muestra)
            tmin_instancia.delete()

            
            #Guardamos el formulario  a falta del resultado final
            fechaInicio= formTmin.cleaned_data['fechaInicio']
            fechaFin= formTmin.cleaned_data['fechaFin']
            temperaturaAmbiente= formTmin.cleaned_data['temperaturaAmbiente']
            humedad= formTmin.cleaned_data['humedad']
            observacion=formTmin.cleaned_data['observacion']

            tmin= TMIn.objects.create(
                muestra=muestra,
                ensayo=ensayo,
                temperaturaAmbiente= temperaturaAmbiente,
                humedad= humedad,
                fechaInicio= fechaInicio,
                fechaFin= fechaFin,
                observacion= observacion,
                usuario= usuario,
            )
            equipos= equiposEnsayo.cleaned_data['equiposEnsayo']
            tmin.equipos.set (equipos)

            #Eliminamos los resultados
            resultadosAnteriores= ResultadosTMIn.objects.filter(ensayo= tmin)
            if resultadosAnteriores:
                for resultado in resultadosAnteriores:
                    resultado.delete()

            
            #Guardamos los resultados en la tabla de resultados TMIn 
            listaResultados= []  

            for form in formTminResultados:
                if form.cleaned_data:  # Para evitar formularios vacíos
                    tHorno = form.cleaned_data['tHorno']
                    peso = form.cleaned_data['peso']
                    presion= form.cleaned_data['presion']
                    resultadoPrueba= form.cleaned_data['resultadoPrueba']

                    resultadosTmin=ResultadosTMIn.objects.create(
                        ensayo= tmin,
                        tHorno=tHorno,
                        peso= peso,
                        presion=presion,
                        resultado=resultadoPrueba,
                    )

                    if resultadoPrueba == "1":
                        listaResultados.append(tHorno)
                    

            #Guardamos en el modelo TMIn el resultado del ensayo
            if listaResultados:
                resultado= min(listaResultados)
                tmin.resultado= resultado - 20
                tmin.save()
            else:
                resultado= ">800"
                tmin.resultado= resultado
                tmin.save()

            datosGuardados= True
                        
        else:
            print (formTmin.errors)
            print(formTminResultados.errors)
            print(equiposEnsayo.errors)
            formTmin.add_error(None, 'Error en el formulario, revisa los datos')
            return render(request, 'ensayos/nuevosEnsayos/tmin.html', {
                'ensayo': ensayo,
                'formTmin': formTmin,
                'formTminResultados': formTminResultados,
                'equiposEnsayo': equiposEnsayo,
        'datosGuardados': datosGuardados,
            })
    else:
        if muestra_id != 'nueva':
            ensayo_TMIn= TMIn.objects.get(muestra__id= muestra_id)  
            equipos=ensayo_TMIn.equipos.all() 
          
            
            muestra= Muestras.objects.get(id=muestra_id) 
            fechaInicio= str(ensayo_TMIn.fechaInicio)
            fechaFin= str(ensayo_TMIn.fechaFin)
            temperaturaAmbiente= ensayo_TMIn.temperaturaAmbiente
            humedad=ensayo_TMIn.humedad
            observacion= ensayo_TMIn.observacion
            
            
            formTmin = TminForm(prefix='tmin', initial={
                'muestra': muestra,
                'fechaInicio': fechaInicio,
                'fechaFin': fechaFin,
                'temperaturaAmbiente': temperaturaAmbiente,
                'humedad': humedad,
                'observacion': observacion,
                })
            
            formTmin.fields['muestra'].queryset = Muestras.objects.filter(id=muestra_id)

            resultados= ResultadosTMIn.objects.filter(ensayo=ensayo_TMIn).order_by("id")

            initial_data = []
            for resultado in resultados:
                initial_data.append({
                    'tHorno': resultado.tHorno,
                    'peso': resultado.peso,
                    'presion': resultado.presion,
                    'resultadoPrueba': resultado.resultado,
                })
            
            # Crear el formset con los datos iniciales
            TminResultadosFormSet = formset_factory(TminResultadosForm, extra=0)
            formTminResultados = TminResultadosFormSet(prefix='tminResultados',initial=initial_data)

            equiposEnsayo = EquiposEnsayoForm(prefix='equipos',initial={'equiposEnsayo': equipos})


        
        else:
            formTmin= TminForm(prefix='tmin')
            formTmin.fields['muestra'].queryset = muestras_queryset

            formTminResultados=tminResultadosFormSet(prefix='tminResultados')  

            equiposEnsayo = EquiposEnsayoForm(prefix='equipos',initial={'equiposEnsayo': equipos})
          


    return render(request, 'ensayos/nuevosEnsayos/tmin.html', {
        'ensayo': ensayo,
        'formTmin': formTmin,
        'formTminResultados': formTminResultados,
        'equiposEnsayo': equiposEnsayo,
        'datosGuardados': datosGuardados,
    })

@login_required
def gestorArchivoLie(request):
    resultados = []  # Se inicializa aquí para evitar problemas si hay errores previos.

    if request.method == 'POST':
        archivo = request.FILES.get('file')

        if archivo:
            try:
                contenido = archivo.read().decode('utf-8')
                filas = contenido.strip().split('\n')
                
                # Quitamos la primera fila y procesamos las demás
                for fila in filas[1:]:
                    filaLimpia = fila.strip(';').split(';')
                    serie = [valor.strip() for valor in filaLimpia if valor.strip()]
                    resultados.append(serie)
                print(resultados)
            except Exception as e:
                return JsonResponse({"error": f"Error al procesar el archivo: {str(e)}"}, status=400)
        
        else:
            return JsonResponse({"error": "Archivo no recibido"}, status=400)
        
    return JsonResponse({"resultados": resultados})
@login_required
def lie (request, muestra_id):
     #Sacamos el ensayo
    ensayo= get_object_or_404(ListaEnsayos, ensayo= "LIE")
    equipos=get_list_or_404(Equipos, ensayos= ensayo) 
    datosGuardados=False  
    usuario= request.user

    #Filtramos las muestras que pueden salir
    muestras_queryset= Muestras.objects.filter(
        Q(lie__resultado__isnull=True) & Q(listaEnsayos__ensayo__icontains="lie") & ~Q(estado=1)
    )

    if request.method == 'POST':
        #Recibimos los formularios diferenciándolos con el prefijo
        formLie= LieForm(request.POST, prefix='lie')
        formLieResultados= lieResultadosFormSet(request.POST, prefix='lieResultados')  
        equiposEnsayo= EquiposEnsayoForm(request.POST, prefix= 'equiposEnsayo')

        
        if formLie.is_valid() and formLieResultados.is_valid() and equiposEnsayo.is_valid():

            muestra= get_object_or_404(Muestras, id= request.POST.get('lie-muestra'))
            
            #Comprobamos que no exista un ensayo  previo
            lie_instancia= LIE.objects.filter(muestra= muestra)
            lie_instancia.delete()

            
            #Guardamos el formulario  a falta del resultado final
            fechaInicio= formLie.cleaned_data['fechaInicio']
            fechaFin= formLie.cleaned_data['fechaFin']
            temperaturaAmbiente= formLie.cleaned_data['temperaturaAmbiente']
            humedad= formLie.cleaned_data['humedad']
            cerillas= formLie.cleaned_data['cerillas']
            boquilla= formLie.cleaned_data['boquilla']
            observacion = formLie.cleaned_data.get('observacion', '') #Corrige el problema de las comillas

            lie= LIE.objects.create(
                muestra=muestra,
                ensayo=ensayo,
                temperaturaAmbiente= temperaturaAmbiente,
                humedad= humedad,
                cerillas= cerillas,
                boquilla= boquilla,
                fechaInicio= fechaInicio,
                fechaFin= fechaFin,
                observacion= observacion,
                usuario= usuario,
            )
            
            equipos= equiposEnsayo.cleaned_data['equiposEnsayo']
            lie.equipos.set (equipos)

            #Eliminamos los resultados
            resultadosAnteriores= ResultadosLIE.objects.filter(ensayo= lie)
            if resultadosAnteriores:
                for resultado in resultadosAnteriores:
                    resultado.delete()

            
            #Guardamos los resultados en la tabla de resultados LIE 
            listaResultados= []  

            for form in formLieResultados:
                if form.cleaned_data:  # Para evitar formularios vacíos
                    concentracion = form.cleaned_data['concentracion']
                    peso = form.cleaned_data['peso']
                    pex= form.cleaned_data['pex']
                    pm= form.cleaned_data['pm']
                    dpdt= form.cleaned_data['dpdt']
                    resultadoPrueba= form.cleaned_data['resultadoPrueba']

                    resultadosLie=ResultadosLIE.objects.create(
                        ensayo= lie,
                        concentracion= concentracion,
                        peso=peso,
                        pex= pex,
                        pm= pm,
                        dpdt=dpdt,
                        resultado=resultadoPrueba,
                    )

                    if resultadoPrueba == "1":
                        listaResultados.append(concentracion)
                    

            #Guardamos en el modelo LIE el resultado del ensayo
            if listaResultados:
                listaConcentraciones = [10, 20, 30, 60, 125, 250, 500, 750, 1000]

                def encontrar_valor_inferior(lista, valor):
                    # Ordenamos la lista para asegurarnos de que esté en orden ascendente
                    lista_ordenada = sorted(lista)
                    
                    # Verificamos si el valor está en la lista y buscamos el valor inferior
                    for i in range(len(lista_ordenada)):
                        if lista_ordenada[i] == valor:
                            if i > 0:  
                                return lista_ordenada[i - 1]
                            else:
                                return None 
                    return None 

                valor_buscado = min(listaResultados)
                resultado = encontrar_valor_inferior(listaConcentraciones, valor_buscado)

                lie.resultado= resultado
                lie.save()
            else:
                print("adios")
                resultado= "N/D"
                lie.resultado= resultado
                lie.save()

            datosGuardados= True            
        else:
            print (formLie.errors)
            formLie.add_error(None, 'Error en el formulario, revisa los datos')
            return render(request, 'ensayos/nuevosEnsayos/lie.html', {
                'ensayo': ensayo,
                'formLie': formLie,
                'formLieResultados': formLieResultados,
                'equiposEnsayo': equiposEnsayo,
        'datosGuardados': datosGuardados,
            })
    else:
        if muestra_id != 'nueva':
            ensayo_LIE= LIE.objects.get(muestra__id= muestra_id)            
            equipos=ensayo_LIE.equipos.all() 
            
            muestra= Muestras.objects.get(id=muestra_id) 
            fechaInicio= str(ensayo_LIE.fechaInicio)
            fechaFin= str(ensayo_LIE.fechaFin)
            temperaturaAmbiente= ensayo_LIE.temperaturaAmbiente
            humedad=ensayo_LIE.humedad
            cerillas=ensayo_LIE.cerillas
            boquilla=ensayo_LIE.boquilla
            observacion= ensayo_LIE.observacion
            
            
            formLie = LieForm(prefix='lie', initial={
                'muestra': muestra,
                'fechaInicio': fechaInicio,
                'fechaFin': fechaFin,
                'temperaturaAmbiente': temperaturaAmbiente,
                'humedad': humedad,
                'cerillas': cerillas,
                'boquilla': boquilla,
                'observacion': observacion,
                })
            
            formLie.fields['muestra'].queryset = Muestras.objects.filter(id=muestra_id)

            resultados= ResultadosLIE.objects.filter(ensayo=ensayo_LIE).order_by("id")

            initial_data = []
            for resultado in resultados:
                initial_data.append({
                    'concentracion': resultado.concentracion,
                    'peso': resultado.peso,
                    'pex': resultado.pex,
                    'pm': resultado.pm,
                    'dpdt': resultado.dpdt,
                    'resultadoPrueba': resultado.resultado,
                })
            
            # Crear el formset con los datos iniciales
            LieResultadosFormSet = formset_factory(LieResultadosForm, extra=0)
            formLieResultados = LieResultadosFormSet(prefix='lieResultados',initial=initial_data)

            equiposEnsayo= EquiposEnsayoForm(prefix= 'equiposEnsayo', initial= {'equiposEnsayo': equipos})           

        
        else:
            formLie= LieForm(prefix='lie')
            formLie.fields['muestra'].queryset = muestras_queryset

            formLieResultados=lieResultadosFormSet(prefix='lieResultados') 

            equiposEnsayo = EquiposEnsayoForm(prefix='equiposEnsayo',initial={'equiposEnsayo': equipos})          


    return render(request, 'ensayos/nuevosEnsayos/lie.html', {
        'ensayo': ensayo,
        'formLie': formLie,
        'formLieResultados': formLieResultados,
        'equiposEnsayo': equiposEnsayo,
        'datosGuardados': datosGuardados,
    })

@login_required
def gestorArchivoEmi(request):
    resultados = []  # Se inicializa aquí para evitar problemas si hay errores previos.

    if request.method == 'POST':
        archivo = request.FILES.get('file')

        if archivo:
            try:
                contenido = archivo.read().decode('utf-8')
                filas = contenido.strip().split('\n')
                
                # Quitamos la primera fila y procesamos las demás
                for fila in filas[1:]:
                    filaLimpia = fila.strip(';').split(';')
                    serie = [valor.strip() for valor in filaLimpia if valor.strip()]
                    resultados.append(serie)
                print(resultados)
            except Exception as e:
                return JsonResponse({"error": f"Error al procesar el archivo: {str(e)}"}, status=400)
        
        else:
            return JsonResponse({"error": "Archivo no recibido"}, status=400)
        
    return JsonResponse({"resultados": resultados})
@login_required
def emi (request, muestra_id):
    #Sacamos el ensayo
    ensayo= get_object_or_404(ListaEnsayos, ensayo= "EMI")
    equipos=get_list_or_404(Equipos, ensayos= ensayo) 
    datosGuardados=False  
    usuario= request.user
  
    #Filtramos las muestras que pueden salir
    muestras_queryset= Muestras.objects.filter(
        Q(emi__resultado__isnull=True) & Q(listaEnsayos__ensayo__icontains="emi") & ~Q(estado=1)
    )

    if request.method == 'POST':
        #Recibimos los formularios diferenciándolos con el prefijo
        formEmi= EmiForm(request.POST, prefix='emi')
        formEmiResultados= emiResultadosFormSet(request.POST, prefix='emiResultados')  
        equiposEnsayo= EquiposEnsayoForm(request.POST, prefix= "equiposEnsayo")
        
        if formEmi.is_valid() and formEmiResultados.is_valid() and equiposEnsayo.is_valid():

            muestra= get_object_or_404(Muestras, id= request.POST.get('emi-muestra'))
            
            #Comprobamos que no exista un ensayo  previo
            emi_instancia= EMI.objects.filter(muestra= muestra)
            emi_instancia.delete()

            
            #Guardamos el formulario  a falta del resultado final
            fechaInicio= formEmi.cleaned_data['fechaInicio']
            fechaFin= formEmi.cleaned_data['fechaFin']
            temperaturaAmbiente= formEmi.cleaned_data['temperaturaAmbiente']
            humedad= formEmi.cleaned_data['humedad']
            inductancia= formEmi.cleaned_data['inductancia']
            observacion=formEmi.cleaned_data['observacion']
            presion= formEmi.cleaned_data['presion']
            resultado= formEmi.cleaned_data['resultado']
            

            emi= EMI.objects.create(
                muestra=muestra,
                ensayo=ensayo,
                temperaturaAmbiente= temperaturaAmbiente,
                humedad= humedad,
                inductancia= inductancia,
                fechaInicio= fechaInicio,
                fechaFin= fechaFin,
                presion= presion,
                observacion= observacion,
                usuario= usuario,
                
            )
            equipos= equiposEnsayo.cleaned_data['equiposEnsayo']
            emi.equipos.set (equipos)

            #Eliminamos los resultados
            resultadosAnteriores= ResultadosEMI.objects.filter(ensayo= emi)
            if resultadosAnteriores:
                for resultado in resultadosAnteriores:
                    resultado.delete()

            
            #Guardamos los resultados en la tabla de resultados EMI 
            listaResultados= []  

            for form in formEmiResultados:
                if form.cleaned_data and form.cleaned_data["concentracion"] != None: 
                    concentracion = form.cleaned_data['concentracion']
                    energia= form.cleaned_data['energia']
                    retardo= form.cleaned_data['retardo']
                    resultadoPrueba= form.cleaned_data['resultadoPrueba']
                    nEnsayo= form.cleaned_data['numeroEnsayo']

                    resultadosEmi=ResultadosEMI.objects.create(
                        ensayo= emi,
                        concentracion= concentracion,
                        energia= energia,
                        retardo= retardo,
                        resultado=resultadoPrueba,
                        numeroEnsayo=nEnsayo,
                    )

                    if resultadoPrueba == "1":
                        listaResultados.append(energia)
                    

            #Guardamos en el modelo EMI el resultado del ensayo
            if listaResultados:
                resultado= resultado
                
                emi.resultado= resultado
                emi.save()
            else:
                resultado= "N/D"
                emi.resultado= resultado
                emi.save()
                
            datosGuardados= True        
        else:
            
            return render(request, 'ensayos/nuevosEnsayos/emi.html', {
                'ensayo': ensayo,
                'formEmi': formEmi,
                'formEmiResultados': formEmiResultados,
                'equiposEnsayo': equiposEnsayo,
        'datosGuardados': datosGuardados,
            })
    else:
        if muestra_id != 'nueva':
            ensayo_EMI= EMI.objects.get(muestra__id= muestra_id)   
            equipos= ensayo_EMI.equipos.all()        
            
            muestra= Muestras.objects.get(id=muestra_id) 
            fechaInicio= str(ensayo_EMI.fechaInicio)
            fechaFin= str(ensayo_EMI.fechaFin)
            temperaturaAmbiente= ensayo_EMI.temperaturaAmbiente
            humedad=ensayo_EMI.humedad
            inductancia= ensayo_EMI.inductancia
            resultado= ensayo_EMI.resultado
            presion= ensayo_EMI.presion
            observacion= ensayo_EMI.observacion
            
            
            formEmi = EmiForm(prefix='emi', initial={
                'muestra': muestra,
                'fechaInicio': fechaInicio,
                'fechaFin': fechaFin,
                'temperaturaAmbiente': temperaturaAmbiente,
                'humedad': humedad,
                'inductancia': inductancia,
                'resultado': resultado,
                'presion': presion,
                'observacion': observacion,
                })
            
            formEmi.fields['muestra'].queryset = Muestras.objects.filter(id=muestra_id)

            resultados= ResultadosEMI.objects.filter(ensayo=ensayo_EMI).order_by("id")

            initial_data = []
            for resultado in resultados:
                initial_data.append({
                    'concentracion': resultado.concentracion,
                    'energia': resultado.energia,
                    'retardo': resultado.retardo,
                    'resultadoPrueba': resultado.resultado,
                    'numeroEnsayo': resultado.numeroEnsayo,
                })
            
            # Crear el formset con los datos iniciales
            EmiResultadosFormSet = formset_factory(EmiResultadosForm, extra=0)
            formEmiResultados = EmiResultadosFormSet(prefix='emiResultados',initial=initial_data)
            
            equiposEnsayo= EquiposEnsayoForm(prefix="equiposEnsayo", initial= {'equiposEnsayo':equipos})
        
        else:
            formEmi= EmiForm(prefix='emi')
            formEmi.fields['muestra'].queryset = muestras_queryset

            formEmiResultados=emiResultadosFormSet(prefix='emiResultados') 
            equiposEnsayo = EquiposEnsayoForm(prefix='equiposEnsayo',initial={'equiposEnsayo': equipos})           


    return render(request, 'ensayos/nuevosEnsayos/emi.html', {
        'ensayo': ensayo,
        'formEmi': formEmi,
        'formEmiResultados': formEmiResultados,
        'equiposEnsayo': equiposEnsayo,
        'datosGuardados': datosGuardados,
    })
@login_required
def emiSinInductancia(request, muestra_id):
    #Sacamos el ensayo
    ensayo= get_object_or_404(ListaEnsayos, ensayo= "EMIsin")
    equipos=get_list_or_404(Equipos, ensayos= ensayo) 
    datosGuardados=False  
    usuario= request.user
  
    #Filtramos las muestras que pueden salir
    muestras_queryset= Muestras.objects.filter(
        Q(emisin__resultado__isnull=True) & Q(listaEnsayos__ensayo__icontains="emisin") & ~Q(estado=1)
    )

    if request.method == 'POST':
        #Recibimos los formularios diferenciándolos con el prefijo
        formEmi= EmiForm(request.POST, prefix='emi')
        formEmiResultados= emiResultadosFormSet(request.POST, prefix='emiResultados') 
        equiposEnsayo= EquiposEnsayoForm(request.POST, prefix= "equiposEnsayo") 

        if formEmi.is_valid() and formEmiResultados.is_valid() and equiposEnsayo.is_valid():
            muestra= get_object_or_404(Muestras, id= request.POST.get('emi-muestra'))
            
            
            #Comprobamos que no exista un ensayo  previo
            emi_instancia= EMIsin.objects.filter(muestra= muestra)
            emi_instancia.delete()

            
            #Guardamos el formulario  a falta del resultado final
            fechaInicio= formEmi.cleaned_data['fechaInicio']
            fechaFin= formEmi.cleaned_data['fechaFin']
            temperaturaAmbiente= formEmi.cleaned_data['temperaturaAmbiente']
            humedad= formEmi.cleaned_data['humedad']
            inductancia= formEmi.cleaned_data['inductancia']
            observacion=formEmi.cleaned_data['observacion']
            presion= formEmi.cleaned_data['presion']
            resultado= formEmi.cleaned_data['resultado']
            

            emi= EMIsin.objects.create(
                muestra=muestra,
                ensayo=ensayo,
                temperaturaAmbiente= temperaturaAmbiente,
                humedad= humedad,
                inductancia= inductancia,
                fechaInicio= fechaInicio,
                fechaFin= fechaFin,
                presion= presion,
                observacion= observacion,
                usuario= usuario,
                
            )
            equipos= equiposEnsayo.cleaned_data['equiposEnsayo']
            emi.equipos.set (equipos)

            #Eliminamos los resultados
            resultadosAnteriores= ResultadosEMIsin.objects.filter(ensayo= emi)
            if resultadosAnteriores:
                for resultado in resultadosAnteriores:
                    resultado.delete()

            
            #Guardamos los resultados en la tabla de resultados EMI 
            listaResultados= []  

            for form in formEmiResultados:
                if form.cleaned_data and form.cleaned_data["concentracion"] != None: 
                    concentracion = form.cleaned_data['concentracion']
                    energia= form.cleaned_data['energia']
                    retardo= form.cleaned_data['retardo']
                    resultadoPrueba= form.cleaned_data['resultadoPrueba']
                    nEnsayo= form.cleaned_data['numeroEnsayo']

                    resultadosEmi=ResultadosEMIsin.objects.create(
                        ensayo= emi,
                        concentracion= concentracion,
                        energia= energia,
                        retardo= retardo,
                        resultado=resultadoPrueba,
                        numeroEnsayo=nEnsayo,
                    )

                    if resultadoPrueba == "1":
                        listaResultados.append(energia)
                    

            #Guardamos en el modelo EMI el resultado del ensayo
            if listaResultados:
                resultado= resultado
                
                emi.resultado= resultado
                emi.save()
            else:
                resultado= "N/D"
                emi.resultado= resultado
                emi.save()
                
            datosGuardados= True
        else:
            print (formEmi.errors)
            print (formEmiResultados.errors)
            formEmi.add_error(None, f'Error en el formulario, revisa los datos {formEmi.errors}')
            return render(request, 'ensayos/nuevosEnsayos/emi.html', {
                'ensayo': ensayo,
                'formEmi': formEmi,
                'formEmiResultados': formEmiResultados,
                'equiposEnsayo': equiposEnsayo,
        'datosGuardados': datosGuardados,
            })
    else:
        if muestra_id != 'nueva':
            ensayo_EMI= EMIsin.objects.get(muestra__id= muestra_id)  
            equipos= ensayo_EMI.equipos.all()          
            
            muestra= Muestras.objects.get(id=muestra_id) 
            fechaInicio= str(ensayo_EMI.fechaInicio)
            fechaFin= str(ensayo_EMI.fechaFin)
            temperaturaAmbiente= ensayo_EMI.temperaturaAmbiente
            humedad=ensayo_EMI.humedad
            inductancia= ensayo_EMI.inductancia
            resultado= ensayo_EMI.resultado
            presion= ensayo_EMI.presion
            observacion= ensayo_EMI.observacion
            
            
            formEmi = EmiForm(prefix='emi', initial={
                'muestra': muestra,
                'fechaInicio': fechaInicio,
                'fechaFin': fechaFin,
                'temperaturaAmbiente': temperaturaAmbiente,
                'humedad': humedad,
                'inductancia': inductancia,
                'resultado': resultado,
                'presion': presion,
                'observacion': observacion,
                })
            
            formEmi.fields['muestra'].queryset = Muestras.objects.filter(id=muestra_id)

            resultados= ResultadosEMIsin.objects.filter(ensayo=ensayo_EMI).order_by("id")

            initial_data = []
            for resultado in resultados:
                initial_data.append({
                    'concentracion': resultado.concentracion,
                    'energia': resultado.energia,
                    'retardo': resultado.retardo,
                    'resultadoPrueba': resultado.resultado,
                    'numeroEnsayo': resultado.numeroEnsayo,
                })
            
            # Crear el formset con los datos iniciales
            EmiResultadosFormSet = formset_factory(EmiResultadosForm, extra=0)
            formEmiResultados = EmiResultadosFormSet(prefix='emiResultados',initial=initial_data)

            equiposEnsayo= EquiposEnsayoForm(prefix="equiposEnsayo", initial= {'equiposEnsayo':equipos})
        
        else:
            formEmi= EmiForm(prefix='emi')
            formEmi.fields['muestra'].queryset = muestras_queryset
            formEmi.fields['inductancia'].initial = "2"

            formEmiResultados=emiResultadosFormSet(prefix='emiResultados') 
            equiposEnsayo = EquiposEnsayoForm(prefix='equiposEnsayo',initial={'equiposEnsayo': equipos})           


    return render(request, 'ensayos/nuevosEnsayos/emi.html', {
        'ensayo': ensayo,
        'formEmi': formEmi,
        'formEmiResultados': formEmiResultados,
        'equiposEnsayo': equiposEnsayo,
        'datosGuardados': datosGuardados,
    })

@login_required
def gestorArchivoPmax(request):
    resultados = []  # Se inicializa aquí para evitar problemas si hay errores previos.

    if request.method == 'POST':
        archivo = request.FILES.get('file')

        if archivo:
            try:
                contenido = archivo.read().decode('utf-8')
                filas = contenido.strip().split('\n')
                
                # Quitamos la primera fila y procesamos las demás
                for fila in filas[1:]:
                    filaLimpia = fila.strip(';').split(';')
                    serie = [valor.strip() for valor in filaLimpia if valor.strip()]
                    resultados.append(serie)
                print(resultados)
            except Exception as e:
                return JsonResponse({"error": f"Error al procesar el archivo: {str(e)}"}, status=400)
        
        else:
            return JsonResponse({"error": "Archivo no recibido"}, status=400)
        
    return JsonResponse({"resultados": resultados})
@login_required
def pmax (request, muestra_id):
     #Sacamos el ensayo
    ensayo= get_object_or_404(ListaEnsayos, ensayo= "Pmax")
    equipos=get_list_or_404(Equipos, ensayos= ensayo) 
    datosGuardados=False  
    usuario= request.user
  
    #Filtramos las muestras que pueden salir
    muestras_queryset= Muestras.objects.filter(
        Q(pmax__pmax__isnull=True) & Q(pmax__dpdt__isnull=True) & Q(pmax__kmax__isnull=True) & Q(listaEnsayos__ensayo__icontains="pmax") & ~Q(estado=1)
    )

    if request.method == 'POST':
        
        #Recibimos los formularios diferenciándolos con el prefijo
        formPmax= PmaxForm(request.POST, prefix='pmax')
        formPmaxResultados= pmaxResultadosFormSet(request.POST, prefix='pmaxResultados')
        equiposEnsayo= EquiposEnsayoForm(request.POST, prefix='equiposEnsayo')
          
        if formPmax.is_valid() and formPmaxResultados.is_valid() and equiposEnsayo.is_valid():

            muestra= get_object_or_404(Muestras, id= request.POST.get('pmax-muestra'))
            
            #Comprobamos que no exista un ensayo  previo
            pmax_instancia= Pmax.objects.filter(muestra= muestra)
            pmax_instancia.delete()

            
            #Guardamos el formulario  a falta del resultado final
            fechaInicio= formPmax.cleaned_data['fechaInicio']
            fechaFin= formPmax.cleaned_data['fechaFin']
            temperaturaAmbiente= formPmax.cleaned_data['temperaturaAmbiente']
            humedad= formPmax.cleaned_data['humedad']
            cerillas= formPmax.cleaned_data['cerillas']
            boquilla= formPmax.cleaned_data['boquilla']
            pmax= formPmax.cleaned_data['pm_media']
            dpdt= formPmax.cleaned_data['dpdt_media']
            kmax= formPmax.cleaned_data['kmax']
            observacion=formPmax.cleaned_data['observacion']

            pmax= Pmax.objects.create(
                muestra=muestra,
                ensayo=ensayo,
                temperaturaAmbiente= temperaturaAmbiente,
                humedad= humedad,
                cerillas= cerillas,
                boquilla= boquilla,
                pmax= pmax,
                dpdt= dpdt,
                kmax= kmax,
                fechaInicio= fechaInicio,
                fechaFin= fechaFin,
                observacion= observacion,
                usuario= usuario,
            )
            equipos= equiposEnsayo.cleaned_data['equiposEnsayo']
            pmax.equipos.set (equipos)

            #Eliminamos los resultados
            resultadosAnteriores= ResultadosPmax.objects.filter(ensayo= pmax)
            if resultadosAnteriores:
                for resultado in resultadosAnteriores:
                    resultado.delete()
            
            #Guadramos la lista de resultados

            for form in formPmaxResultados:
                
                if form.cleaned_data:  # Para evitar formularios vacíos
                    concentracion = form.cleaned_data['concentracion']
                    peso = form.cleaned_data['peso']
                    serie= form.cleaned_data['serie']
                    pm= form.cleaned_data['pm_serie']
                    dpdt= form.cleaned_data['dpdt_serie']
                    

                    resultadosPmax=ResultadosPmax.objects.create(
                        ensayo= pmax,
                        concentracion= concentracion,
                        peso=peso,
                        serie= serie,
                        pm= pm,
                        dpdt=dpdt,
                    )
                    
                else:
                    formPmax.add_error(None, 'No hay resultados positivos en el ensayo, revisa la tabla.')
                    print(formPmaxResultados.errors)
                    return render(request, 'ensayos/nuevosEnsayos/pmax.html', {
                        'ensayo': ensayo,
                        'formPmax': formPmax,
                        'formPmaxResultados': formPmaxResultados,
                        'equiposEnsayo': equiposEnsayo,
                        'datosGuardados': datosGuardados,
                    })
            datosGuardados= True            
        else:
            print (formPmax.errors)
            formPmax.add_error(None, f'Error en el formulario, revisa los datos {formPmax.errors}')
            return render(request, 'ensayos/nuevosEnsayos/pmax.html', {
                'ensayo': ensayo,
                'formPmax': formPmax,
                'formPmaxResultados': formPmaxResultados,
                'equiposEnsayo': equiposEnsayo,
        'datosGuardados': datosGuardados,
            })
    else:
        if muestra_id != 'nueva':
            ensayo_Pmax= Pmax.objects.get(muestra__id= muestra_id)   
            equipos= ensayo_Pmax.equipos.all()         
            
            muestra= Muestras.objects.get(id=muestra_id) 
            fechaInicio= str(ensayo_Pmax.fechaInicio)
            fechaFin= str(ensayo_Pmax.fechaFin)
            temperaturaAmbiente= ensayo_Pmax.temperaturaAmbiente
            humedad=ensayo_Pmax.humedad
            cerillas=ensayo_Pmax.cerillas
            boquilla=ensayo_Pmax.boquilla
            pmax= ensayo_Pmax.pmax
            dpdt= ensayo_Pmax.dpdt
            kmax= ensayo_Pmax.kmax
            observacion= ensayo_Pmax.observacion
            
            
            formPmax = PmaxForm(prefix='pmax', initial={
                'muestra': muestra,
                'fechaInicio': fechaInicio,
                'fechaFin': fechaFin,
                'temperaturaAmbiente': temperaturaAmbiente,
                'humedad': humedad,
                'cerillas': cerillas,
                'boquilla': boquilla,
                'pm_media': pmax,
                'dpdt_media': dpdt,
                'kmax': kmax,
                'observacion': observacion,
                })
            
            formPmax.fields['muestra'].queryset = Muestras.objects.filter(id=muestra_id)

            resultados= ResultadosPmax.objects.filter(ensayo=ensayo_Pmax).order_by("id")

            initial_data = []
            for resultado in resultados:
                initial_data.append({
                    'concentracion': resultado.concentracion,
                    'peso': resultado.peso,
                    'serie': resultado.serie,
                    'pm_serie': resultado.pm,
                    'dpdt_serie': resultado.dpdt,
                })
            
            # Crear el formset con los datos iniciales
            PmaxResultadosFormSet = formset_factory(PmaxResultadosForm, extra=0)
            formPmaxResultados = PmaxResultadosFormSet(prefix='pmaxResultados',initial=initial_data)
            equiposEnsayo= EquiposEnsayoForm(prefix="equiposEnsayo", initial= {'equiposEnsayo':equipos})

        
        else:
            formPmax= PmaxForm(prefix='pmax')
            formPmax.fields['muestra'].queryset = muestras_queryset

            formPmaxResultados=pmaxResultadosFormSet(prefix='pmaxResultados')     
            equiposEnsayo = EquiposEnsayoForm(prefix='equiposEnsayo',initial={'equiposEnsayo': equipos}) 
                


    return render(request, 'ensayos/nuevosEnsayos/pmax.html', {
        'ensayo': ensayo,
        'formPmax': formPmax,
        'formPmaxResultados': formPmaxResultados,
        'equiposEnsayo': equiposEnsayo,
        'datosGuardados': datosGuardados,
    })

@login_required
def clo (request, muestra_id):
     #Sacamos el ensayo
    ensayo= get_object_or_404(ListaEnsayos, ensayo= "CLO")
    equipos=get_list_or_404(Equipos, ensayos= ensayo) 
    datosGuardados=False  
    usuario= request.user
  
    #Filtramos las muestras que pueden salir
    muestras_queryset= Muestras.objects.filter(
        Q(clo__resultado__isnull=True) & Q(listaEnsayos__ensayo__icontains="clo") & ~Q(estado=1)
    )

    if request.method == 'POST':
        #Recibimos los formularios diferenciándolos con el prefijo
        formClo= CloForm(request.POST, prefix='clo')
        formCloResultados= cloResultadosFormSet(request.POST, prefix='cloResultados')  
        equiposEnsayo= EquiposEnsayoForm(request.POST, prefix= 'equiposEnsayo')
        
        if formClo.is_valid() and formCloResultados.is_valid() and equiposEnsayo.is_valid():

            muestra= get_object_or_404(Muestras, id= request.POST.get('clo-muestra'))
            
            #Comprobamos que no exista un ensayo  previo
            clo_instancia= CLO.objects.filter(muestra= muestra)
            clo_instancia.delete()

            
            #Guardamos el formulario  a falta del resultado final
            fechaInicio= formClo.cleaned_data['fechaInicio']
            fechaFin= formClo.cleaned_data['fechaFin']
            temperaturaAmbiente= formClo.cleaned_data['temperaturaAmbiente']
            humedad= formClo.cleaned_data['humedad']
            cerillas= formClo.cleaned_data['cerillas']
            boquilla= formClo.cleaned_data['boquilla']
            observacion = formClo.cleaned_data.get('observacion', '')
            print(f"observacion es {observacion}")

            clo= CLO.objects.create(
                muestra=muestra,
                ensayo=ensayo,
                temperaturaAmbiente= temperaturaAmbiente,
                humedad= humedad,
                cerillas= cerillas,
                boquilla= boquilla,
                fechaInicio= fechaInicio,
                fechaFin= fechaFin,
                observacion= observacion,
                usuario= usuario,
            )

            equipos= equiposEnsayo.cleaned_data['equiposEnsayo']
            clo.equipos.set (equipos)

            #Eliminamos los resultados
            resultadosAnteriores= ResultadosCLO.objects.filter(ensayo= clo)
            if resultadosAnteriores:
                for resultado in resultadosAnteriores:
                    resultado.delete()

            
            #Guardamos los resultados en la tabla de resultados CLO 
            listaResultados= []  

            for form in formCloResultados:
                if form.cleaned_data:  # Para evitar formularios vacíos
                    concentracion = form.cleaned_data['concentracion']
                    peso = form.cleaned_data['peso']
                    pex= form.cleaned_data['pex']
                    pm= form.cleaned_data['pm']
                    dpdt= form.cleaned_data['dpdt']
                    oxigeno= form.cleaned_data['oxigeno']
                    resultadoPrueba= form.cleaned_data['resultadoPrueba']

                    resultadosClo=ResultadosCLO.objects.create(
                        ensayo= clo,
                        concentracion= concentracion,
                        peso=peso,
                        pex= pex,
                        pm= pm,
                        dpdt=dpdt,
                        oxigeno= oxigeno,
                        resultado=resultadoPrueba,
                    )

                    if resultadoPrueba == "2":
                        listaResultados.append(oxigeno)
                    

            #Guardamos en el modelo CLO el resultado del ensayo
            if listaResultados:
                valor_buscado = max(listaResultados)

                clo.resultado= valor_buscado
                clo.save()
            else:
                resultado= "N/D"
                clo.resultado= resultado
                clo.save()

            datosGuardados= True            
        else:
            print (formClo.errors)
            formClo.add_error(None, 'Error en el formulario, revisa los datos')
            return render(request, 'ensayos/nuevosEnsayos/clo.html', {
                'ensayo': ensayo,
                'formClo': formClo,
                'formCloResultados': formCloResultados,
                'equiposEnsayo': equiposEnsayo,
        'datosGuardados': datosGuardados,
            })
    else:
        if muestra_id != 'nueva':
            ensayo_CLO= CLO.objects.get(muestra__id= muestra_id) 
            equipos= ensayo_CLO.equipos.all()           
            
            muestra= Muestras.objects.get(id=muestra_id) 
            fechaInicio= str(ensayo_CLO.fechaInicio)
            fechaFin= str(ensayo_CLO.fechaFin)
            temperaturaAmbiente= ensayo_CLO.temperaturaAmbiente
            humedad=ensayo_CLO.humedad
            cerillas=ensayo_CLO.cerillas
            boquilla=ensayo_CLO.boquilla
            observacion= ensayo_CLO.observacion
            
            
            formClo = CloForm(prefix='clo', initial={
                'muestra': muestra,
                'fechaInicio': fechaInicio,
                'fechaFin': fechaFin,
                'temperaturaAmbiente': temperaturaAmbiente,
                'humedad': humedad,
                'cerillas': cerillas,
                'boquilla': boquilla,
                'observacion': observacion,
                })
            
            formClo.fields['muestra'].queryset = Muestras.objects.filter(id=muestra_id)

            resultados= ResultadosCLO.objects.filter(ensayo=ensayo_CLO).order_by("id")

            initial_data = []
            for resultado in resultados:
                initial_data.append({
                    'concentracion': resultado.concentracion,
                    'peso': resultado.peso,
                    'pex': resultado.pex,
                    'pm': resultado.pm,
                    'dpdt': resultado.dpdt,
                    'oxigeno': resultado.oxigeno,
                    'resultadoPrueba': resultado.resultado,
                })
            
            # Crear el formset con los datos iniciales
            CloResultadosFormSet = formset_factory(CloResultadosForm, extra=0)
            formCloResultados = CloResultadosFormSet(prefix='cloResultados',initial=initial_data)

            equiposEnsayo= EquiposEnsayoForm(prefix= 'equiposEnsayo', initial= {'equiposEnsayo': equipos})
        
        else:
            formClo= CloForm(prefix='clo')
            formClo.fields['muestra'].queryset = muestras_queryset

            formCloResultados=cloResultadosFormSet(prefix='cloResultados')   
            equiposEnsayo = EquiposEnsayoForm(prefix='equiposEnsayo',initial={'equiposEnsayo': equipos})



    return render(request, 'ensayos/nuevosEnsayos/clo.html', {
        'ensayo': ensayo,
        'formClo': formClo,
        'formCloResultados': formCloResultados,
        'equiposEnsayo': equiposEnsayo,
        'datosGuardados': datosGuardados,
    })

@login_required
def rec (request, muestra_id):
     #Sacamos el ensayo
    ensayo= get_object_or_404(ListaEnsayos, ensayo= "REC")
    equipos=get_list_or_404(Equipos, ensayos= ensayo) 
    datosGuardados=False  
    usuario= request.user
  
    #Filtramos las muestras que pueden salir
    muestras_queryset= Muestras.objects.filter(
        Q(rec__resultado__isnull=True) & Q(listaEnsayos__ensayo__icontains="rec") & ~Q(estado=1)
    )

    if request.method == 'POST':
        print(request.POST)
        #Recibimos los formularios diferenciándolos con el prefijo
        formRec= RecForm(request.POST, prefix='rec')
        formRecResultadosSerie1= recResultadosSerie1FormSet(request.POST, prefix='recResultadosSerie1') 
        formRecResultadosSerie2= recResultadosSerie2FormSet(request.POST, prefix='recResultadosSerie2') 
        equiposEnsayo= EquiposEnsayoForm(request.POST, prefix= 'equiposEnsayo') 
        
        if formRec.is_valid() and formRecResultadosSerie1.is_valid() and formRecResultadosSerie2.is_valid() and equiposEnsayo.is_valid():

            muestra= get_object_or_404(Muestras, id= request.POST.get('rec-muestra'))
            
            
            #Comprobamos que no exista un ensayo  previo
            rec_instancia= REC.objects.filter(muestra= muestra)
            rec_instancia.delete()

            
            #Guardamos el formulario  a falta del resultado final
            fechaInicio= formRec.cleaned_data['fechaInicio']
            fechaFin= formRec.cleaned_data['fechaFin']
            temperaturaAmbiente= formRec.cleaned_data['temperaturaAmbiente']
            humedad= formRec.cleaned_data['humedad']
            observacion=formRec.cleaned_data['observacion']

            rec= REC.objects.create(
                muestra=muestra,
                ensayo=ensayo,
                temperaturaAmbiente= temperaturaAmbiente,
                humedad= humedad,
                fechaInicio= fechaInicio,
                fechaFin= fechaFin,
                observacion= observacion,
                usuario= usuario,
            )
            equipos= equiposEnsayo.cleaned_data['equiposEnsayo']
            rec.equipos.set (equipos)

            #Eliminamos los resultados
            resultadosAnteriores= ResultadosREC.objects.filter(ensayo= rec)
            if resultadosAnteriores:
                for resultado in resultadosAnteriores:
                    resultado.delete()

            
            #Guardamos los resultados en la tabla de resultados REC 
            listaResultados1= []  
            listaResultados2= [] 

            for form in formRecResultadosSerie1:
                if form.cleaned_data:  # Para evitar formularios vacíos
                    nPrueba= form.cleaned_data['nPrueba']
                    tension= form.cleaned_data['tension']
                    tiempo= form.cleaned_data['tiempo']
                    resultadoPrueba= form.cleaned_data['resultadoPrueba']

                    resultadosRec=ResultadosREC.objects.create(
                        nPrueba= nPrueba,
                        ensayo= rec,
                        tension= tension,
                        tiempo= tiempo,
                        resultado=resultadoPrueba,
                    )

                    listaResultados1.append(resultadoPrueba)
                    
            for form in formRecResultadosSerie2:
                if form.cleaned_data:  # Para evitar formularios vacíos
                    nPrueba= form.cleaned_data['nPrueba']
                    tension= form.cleaned_data['tension']
                    tiempo= form.cleaned_data['tiempo']
                    resultadoPrueba= form.cleaned_data['resultadoPrueba']

                    resultadosRec=ResultadosREC.objects.create(
                        nPrueba= nPrueba,
                        ensayo= rec,
                        tension= tension,
                        tiempo= tiempo,
                        resultado=resultadoPrueba,
                    )

                    listaResultados2.append(resultadoPrueba)

            #Guardamos en el modelo REC el resultado del ensayo
            if listaResultados1 and listaResultados2:
                
                
                rs1 = min(listaResultados1)
                rs2= min(listaResultados2)

                rs= (rs1+rs2)/2
                hwl= 100
                resultadoEnsayo= (0.001*float(rs)*hwl)*(10**6)
                print(float(rs))
                print(resultadoEnsayo)

                rec.resultado= resultadoEnsayo
                rec.save()
            else:
                resultado= "N/D"
                rec.resultado= resultado
                rec.save()

            datosGuardados= True        
        else:
            print (formRec.errors)
            formRec.add_error(None, 'Error en el formulario, revisa los datos')
            return render(request, 'ensayos/nuevosEnsayos/rec.html', {
                'ensayo': ensayo,
                'formRec': formRec,
                'formRecResultadosSerie1': formRecResultadosSerie1,
                'formRecResultadosSerie2': formRecResultadosSerie2,
                'equiposEnsayo': equiposEnsayo,
        'datosGuardados': datosGuardados,
            })
    else:
        if muestra_id != 'nueva':
            ensayo_REC= REC.objects.get(muestra__id= muestra_id)
            equipos= ensayo_REC.equipos.all()            
            
            muestra= Muestras.objects.get(id=muestra_id) 
            fechaInicio= str(ensayo_REC.fechaInicio)
            fechaFin= str(ensayo_REC.fechaFin)
            temperaturaAmbiente= ensayo_REC.temperaturaAmbiente
            humedad=ensayo_REC.humedad
            observacion= ensayo_REC.observacion
            
            
            formRec = RecForm(prefix='rec', initial={
                'muestra': muestra,
                'fechaInicio': fechaInicio,
                'fechaFin': fechaFin,
                'temperaturaAmbiente': temperaturaAmbiente,
                'humedad': humedad,
                'observacion': observacion,
                })
            
            formRec.fields['muestra'].queryset = Muestras.objects.filter(id=muestra_id)

            resultados= ResultadosREC.objects.filter(ensayo=ensayo_REC).order_by("id")
            print(resultados)

            initial_data1 = []
            initial_data2 = []
            for resultado in resultados:
                print("hola")
                print(resultado.nPrueba)
                if resultado.nPrueba == "1":
                    initial_data1.append({
                        'nPrueba': resultado.nPrueba,
                        'tension': resultado.tension,
                        'tiempo': resultado.tiempo,
                        'resultadoPrueba': resultado.resultado,
                    })
                if resultado.nPrueba == "2":
                    initial_data2.append({
                        'nPrueba': resultado.nPrueba,
                        'tension': resultado.tension,
                        'tiempo': resultado.tiempo,
                        'resultadoPrueba': resultado.resultado,
                    })
            print(initial_data1)
            # Crear el formset con los datos iniciales
            RecResultadosFormSet = formset_factory(RecResultadosForm, extra=0)

            formRecResultadosSerie1=recResultadosSerie1FormSet(prefix='recResultadosSerie1', initial= initial_data1)   
            formRecResultadosSerie2=recResultadosSerie2FormSet(prefix='recResultadosSerie2', initial= initial_data2)

            equiposEnsayo= EquiposEnsayoForm(prefix= 'equiposEnsayo', initial= {'equiposEnsayo': equipos})
        
        else:
            formRec= RecForm(prefix='rec')
            formRec.fields['muestra'].queryset = muestras_queryset
            
            default_data1 = [
                {'nPrueba': '1', 'tension': 100, 'tiempo': 60, },
                {'nPrueba': '1', 'tension': 500, 'tiempo': 60, },
                {'nPrueba': '1',  'tension': 1000, 'tiempo': 60,},
            ]

            default_data2 = [
                {'nPrueba': '2', 'tension': 100, 'tiempo': 60,},
                {'nPrueba': '2', 'tension': 500, 'tiempo': 60,},
                {'nPrueba': '2',  'tension': 1000, 'tiempo': 60,},
            ]

            formRecResultadosSerie1=recResultadosSerie1FormSet(prefix='recResultadosSerie1', initial= default_data1)   
            formRecResultadosSerie2=recResultadosSerie2FormSet(prefix='recResultadosSerie2', initial= default_data2)  


            equiposEnsayo = EquiposEnsayoForm(prefix='equiposEnsayo',initial={'equiposEnsayo': equipos})       


    return render(request, 'ensayos/nuevosEnsayos/rec.html', {
        'ensayo': ensayo,
        'formRec': formRec,
        'formRecResultadosSerie1': formRecResultadosSerie1,
        'formRecResultadosSerie2': formRecResultadosSerie2,
        'equiposEnsayo': equiposEnsayo,
        'datosGuardados': datosGuardados,
    })

@login_required
def n1 (request, muestra_id):
     #Sacamos el ensayo
    ensayo= get_object_or_404(ListaEnsayos, ensayo= "N1")
    equipos=get_list_or_404(Equipos, ensayos= ensayo) 
    datosGuardados=False  
    usuario= request.user
  
    #Filtramos las muestras que pueden salir
    muestras_queryset= Muestras.objects.filter(
        Q(n1__resultado__isnull=True) & Q(listaEnsayos__ensayo__icontains="n1") & ~Q(estado=1)
    )

    if request.method == 'POST':
        print(request.POST)
        #N1ibimos los formularios diferenciándolos con el prefijo
        formN1= N1Form(request.POST, prefix='n1')
        formN1Resultados= n1ResultadosFormSet(request.POST, prefix='n1Resultados')  
        equiposEnsayo= EquiposEnsayoForm(request.POST, prefix='equiposEnsayo')
        
        if formN1.is_valid() and formN1Resultados.is_valid() and equiposEnsayo.is_valid():

            muestra= get_object_or_404(Muestras, id= request.POST.get('n1-muestra'))
              
            
            #Comprobamos que no exista un ensayo  previo
            n1_instancia= N1.objects.filter(muestra= muestra)
            n1_instancia.delete()

            
            #Guardamos el formulario  a falta del resultado final
            fechaInicio= formN1.cleaned_data['fechaInicio']
            fechaFin= formN1.cleaned_data['fechaFin']
            temperaturaAmbiente= formN1.cleaned_data['temperaturaAmbiente']
            humedad= formN1.cleaned_data['humedad']
            tipoPolvo= formN1.cleaned_data['tipoPolvo']
            pruebaPreseleccion= formN1.cleaned_data['pruebaPreseleccion']
            observacion=formN1.cleaned_data['observacion']

            n1= N1.objects.create(
                muestra=muestra,
                ensayo=ensayo,
                temperaturaAmbiente= temperaturaAmbiente,
                humedad= humedad,
                tipoPolvo= tipoPolvo,
                pruebaPreseleccion= pruebaPreseleccion,
                fechaInicio= fechaInicio,
                fechaFin= fechaFin,
                observacion= observacion,
                usuario= usuario,
            )
            equipos= equiposEnsayo.cleaned_data['equiposEnsayo']
            n1.equipos.set (equipos)

            #Eliminamos los resultados
            resultadosAnteriores= ResultadosN1.objects.filter(ensayo= n1)
            if resultadosAnteriores:
                for resultado in resultadosAnteriores:
                    resultado.delete()

            
            #Guardamos los resultados en la tabla de resultados N1 
            listaResultados= []  
            listaRebasaHumedad= []

            for form in formN1Resultados:
                if form.cleaned_data :  # Para evitar formularios vacíos
                    tiempo= form.cleaned_data['tiempo']
                    zonaHumeda= form.cleaned_data['zonaHumeda']
                    print(f'El tiempo es {tiempo}')
        

                    print(tiempo)
                    print(zonaHumeda)
                    resultadosN1=ResultadosN1.objects.create(
                        ensayo= n1,
                        tiempo= tiempo,
                        zonaHumeda=zonaHumeda,
                    )

                    listaResultados.append(tiempo)
                    listaRebasaHumedad.append(zonaHumeda)
                    
            print(f"la lista resultados es: {listaResultados}")
            #Guardamos en el modelo N1 el resultado del ensayo
            if listaResultados and all(element is not None for element in listaResultados):
                if len(listaResultados) == len(listaRebasaHumedad):
                    #Polvos no metálicos
                    if tipoPolvo == "1":
                        for i in range(len(listaResultados)):
                            if listaResultados[i] < 45:
                                if listaRebasaHumedad[i] == "1":
                                    resultado="2"
                                    break
                                else:
                                    resultado= "3"
                            else:
                                resultado= "1"
                                break
                    
                    #Polvos metálicos
                    else:
                        valor_buscado = min(listaResultados)
                        if valor_buscado < 600:
                            if valor_buscado <= 300:
                                resultado="2"
                            else:
                                resultado="3"
                        else:
                            resultado= "1"

                n1.resultado= resultado
                n1.save()
            else:
                resultado= "1"
                n1.resultado= resultado
                n1.save()

            datosGuardados= True            
        else:
            print (formN1.errors)
            formN1.add_error(None, 'Error en el formulario, revisa los datos')
            return render(request, 'ensayos/nuevosEnsayos/n1.html', {
                'ensayo': ensayo,
                'formN1': formN1,
                'formN1Resultados': formN1Resultados,
                'equiposEnsayo': equiposEnsayo,
                'datosGuardados': datosGuardados,
            })
    else:
        if muestra_id != 'nueva':
            ensayo_N1= N1.objects.get(muestra__id= muestra_id)
            equipos= ensayo_N1.equipos.all()            
            
            muestra= Muestras.objects.get(id=muestra_id) 
            fechaInicio= str(ensayo_N1.fechaInicio)
            fechaFin= str(ensayo_N1.fechaFin)
            temperaturaAmbiente= ensayo_N1.temperaturaAmbiente
            humedad=ensayo_N1.humedad
            tipoPolvo= ensayo_N1.tipoPolvo
            pruebaPreseleccion= ensayo_N1.pruebaPreseleccion
            observacion= ensayo_N1.observacion
            

                        
            
            formN1 = N1Form(prefix='n1', initial={
                'muestra': muestra,
                'fechaInicio': fechaInicio,
                'fechaFin': fechaFin,
                'temperaturaAmbiente': temperaturaAmbiente,
                'humedad': humedad,
                'tipoPolvo': tipoPolvo,
                'pruebaPreseleccion': pruebaPreseleccion,
                'observacion': observacion,
                })
            
            formN1.fields['muestra'].queryset = Muestras.objects.filter(id=muestra_id)

            resultados= ResultadosN1.objects.filter(ensayo=ensayo_N1).order_by("id")
            print(resultados)

            initial_data = []
            for resultado in resultados:
                initial_data.append({
                    'tiempo': resultado.tiempo,
                    'zonaHumeda': resultado.zonaHumeda,
                })
            
            # Crear el formset con los datos iniciales
            N1ResultadosFormSet = formset_factory(N1ResultadosForm, extra=0)
            formN1Resultados = N1ResultadosFormSet(prefix='n1Resultados',initial=initial_data)
            equiposEnsayo= EquiposEnsayoForm(prefix= 'equiposEnsayo', initial= {'equiposEnsayo': equipos})
        
        else:
            formN1= N1Form(prefix='n1')
            formN1.fields['muestra'].queryset = muestras_queryset

            formN1Resultados=n1ResultadosFormSet(prefix='n1Resultados')  
            equiposEnsayo = EquiposEnsayoForm(prefix='equiposEnsayo',initial={'equiposEnsayo': equipos})         


    return render(request, 'ensayos/nuevosEnsayos/n1.html', {
        'ensayo': ensayo,
        'formN1': formN1,
        'formN1Resultados': formN1Resultados,
        'equiposEnsayo': equiposEnsayo,
        'datosGuardados': datosGuardados,
    })

@login_required
def n2 (request, muestra_id):
     #Sacamos el ensayo
    ensayo= get_object_or_404(ListaEnsayos, ensayo= "N2")
    equipos= get_list_or_404(Equipos, ensayos=ensayo)
    datosGuardados= False
    usuario= request.user

  
    #Filtramos las muestras que pueden salir
    muestras_queryset= Muestras.objects.filter(
        Q(n2__resultado__isnull=True) & Q(listaEnsayos__ensayo__icontains="n2") & ~Q(estado=1)
    )

    if request.method == 'POST':
        #N2ibimos los formularios diferenciándolos con el prefijo
        formN2= N2Form(request.POST, prefix='n2')
        formN2Resultados= n2ResultadosFormSet(request.POST, prefix='n2Resultados')  
        equiposEnsayo= EquiposEnsayoForm(request.POST, prefix= 'equiposEnsayo')
        
        if formN2.is_valid() and formN2Resultados.is_valid() and equiposEnsayo.is_valid():

            muestra= get_object_or_404(Muestras, id= request.POST.get('n2-muestra')) 
            
            #Comprobamos que no exista un ensayo  previo
            n2_instancia= N2.objects.filter(muestra= muestra)
            n2_instancia.delete()

            
            #Guardamos el formulario  a falta del resultado final
            fechaInicio= formN2.cleaned_data['fechaInicio']
            fechaFin= formN2.cleaned_data['fechaFin']
            temperaturaAmbiente= formN2.cleaned_data['temperaturaAmbiente']
            humedad= formN2.cleaned_data['humedad']
            observacion=formN2.cleaned_data['observacion']

            n2= N2.objects.create(
                muestra=muestra,
                ensayo=ensayo,
                temperaturaAmbiente= temperaturaAmbiente,
                humedad= humedad,
                fechaInicio= fechaInicio,
                fechaFin= fechaFin,
                observacion= observacion,
                usuario= usuario,
            )
            equipos= equiposEnsayo.cleaned_data['equiposEnsayo']
            n2.equipos.set (equipos)

            #Eliminamos los resultados
            resultadosAnteriores= ResultadosN2.objects.filter(ensayo= n2)
            if resultadosAnteriores:
                for resultado in resultadosAnteriores:
                    resultado.delete()

            
            #Guardamos los resultados en la tabla de resultados N2 
            listaResultados= []  

            for form in formN2Resultados:
                if form.cleaned_data:  # Para evitar formularios vacíos
                    resultado= form.cleaned_data['resultado']

                    resultadosN2=ResultadosN2.objects.create(
                        ensayo= n2,
                        resultado= resultado
                    )
                    if resultado == "1":
                        listaResultados.append(resultado)
                    

            #Guardamos en el modelo N2 el resultado del ensayo
            if listaResultados:
                resultado= "2"
                n2.resultado= resultado
                n2.save()
            else:
                resultado= "1"
                n2.resultado= resultado
                n2.save()

            datosGuardados= True            
        else:
            print (formN2.errors)
            formN2.add_error(None, 'Error en el formulario, revisa los datos')
            return render(request, 'ensayos/nuevosEnsayos/n2.html', {
                'ensayo': ensayo,
                'formN2': formN2,
                'formN2Resultados': formN2Resultados,
                'equiposEnsayo': equiposEnsayo,
                'datosGuardados': datosGuardados,
            })
    else:
        if muestra_id != 'nueva':
            ensayo_N2= N2.objects.get(muestra__id= muestra_id) 
            equipos= ensayo_N2.equipos.all()           
            
            muestra= Muestras.objects.get(id=muestra_id) 
            fechaInicio= str(ensayo_N2.fechaInicio)
            fechaFin= str(ensayo_N2.fechaFin)
            temperaturaAmbiente= ensayo_N2.temperaturaAmbiente
            humedad=ensayo_N2.humedad
            observacion= ensayo_N2.observacion
            
            
            formN2 = N2Form(prefix='n2', initial={
                'muestra': muestra,
                'fechaInicio': fechaInicio,
                'fechaFin': fechaFin,
                'temperaturaAmbiente': temperaturaAmbiente,
                'humedad': humedad,
                'observacion': observacion,
                })
            
            formN2.fields['muestra'].queryset = Muestras.objects.filter(id=muestra_id)

            resultados= ResultadosN2.objects.filter(ensayo=ensayo_N2).order_by("id")

            initial_data = []
            for resultado in resultados:
                initial_data.append({
                    'resultado': resultado.resultado,
                })
            
            # Crear el formset con los datos iniciales
            N2ResultadosFormSet = formset_factory(N2ResultadosForm, extra=0)
            formN2Resultados = N2ResultadosFormSet(prefix='n2Resultados',initial=initial_data)
            equiposEnsayo= EquiposEnsayoForm(prefix= 'equiposEnsayo', initial= {'equiposEnsayo': equipos})
        
        else:
            formN2= N2Form(prefix='n2')
            formN2.fields['muestra'].queryset = muestras_queryset

            formN2Resultados=n2ResultadosFormSet(prefix='n2Resultados') 
            equiposEnsayo= EquiposEnsayoForm(prefix= 'equiposEnsayo', initial= {'equiposEnsayo': equipos})           


    return render(request, 'ensayos/nuevosEnsayos/n2.html', {
        'ensayo': ensayo,
        'formN2': formN2,
        'formN2Resultados': formN2Resultados,
        'equiposEnsayo': equiposEnsayo,
        'datosGuardados': datosGuardados,
    })

@login_required
def n4 (request, muestra_id):
     #Sacamos el ensayo
    ensayo= get_object_or_404(ListaEnsayos, ensayo= "N4")
    equipos= get_list_or_404(Equipos, ensayos=ensayo)
    datosGuardados= False
    usuario= request.user
  
    #Filtramos las muestras que pueden salir
    muestras_queryset= Muestras.objects.filter(
        Q(n4__resultado__isnull=True) & Q(listaEnsayos__ensayo__icontains="n4") & ~Q(estado=1)
    )

    if request.method == 'POST':
        #N4ibimos los formularios diferenciándolos con el prefijo
        formN4= N4Form(request.POST, prefix='n4')
        formN4Resultados= n4ResultadosFormSet(request.POST, prefix='n4Resultados') 
        equiposEnsayo= EquiposEnsayoForm(request.POST, prefix= 'equiposEnsayo')
        
        if formN4.is_valid() and formN4Resultados.is_valid() and equiposEnsayo.is_valid():

            idMuestra= request.POST.get('n4-muestra')
            muestra= get_object_or_404(Muestras, id= idMuestra) 
            
            #Comprobamos que no exista un ensayo  previo
            n4_instancia= N4.objects.filter(muestra= muestra)
            n4_instancia.delete()

            
            #Guardamos el formulario  a falta del resultado final
            fechaInicio= formN4.cleaned_data['fechaInicio']
            fechaFin= formN4.cleaned_data['fechaFin']
            temperaturaAmbiente= formN4.cleaned_data['temperaturaAmbiente']
            humedad= formN4.cleaned_data['humedad']
            observacion=formN4.cleaned_data['observacion']

            n4= N4.objects.create(
                muestra=muestra,
                ensayo=ensayo,
                temperaturaAmbiente= temperaturaAmbiente,
                humedad= humedad,
                fechaInicio= fechaInicio,
                fechaFin= fechaFin,
                observacion= observacion,
                usuario= usuario,
            )
            equipos= equiposEnsayo.cleaned_data['equiposEnsayo']
            n4.equipos.set (equipos)

            #Eliminamos los resultados
            resultadosAnteriores= ResultadosN4.objects.filter(ensayo= n4)
            if resultadosAnteriores:
                for resultado in resultadosAnteriores:
                    resultado.delete()

            
            #Guardamos los resultados en la tabla de resultados N4 
            listaResultados= []  

            for form in formN4Resultados:
                if form.cleaned_data:  # Para evitar formularios vacíos
                    celda= form.cleaned_data['celda']
                    tConsigna= form.cleaned_data['tConsigna']
                    tMax= form.cleaned_data['tMax']
                    tiempo= form.cleaned_data['tiempo']
                    resultado= form.cleaned_data['resultado']

                    resultadosN4=ResultadosN4.objects.create(
                        ensayo= n4,
                        celda= celda,
                        tConsigna= tConsigna,
                        tMax= tMax,
                        tiempo= tiempo,
                        resultado= resultado
                    )
                    
                    listaResultados.append(resultado)
            print(listaResultados)

            #Guardamos en el modelo N4 el resultado del ensayo
            if len(listaResultados) == 1:
                print("a")
                if listaResultados[0]== "2":
                    resultado= "1"                    

            if len(listaResultados) == 2:
                print("b")
                if listaResultados[1]== "1":
                    resultado= "2"

            if len(listaResultados) == 3:
                print("c")
                if listaResultados[2]== "2":
                    resultado= "3"
            
            if len(listaResultados) == 4:
                print("d")
                if listaResultados[3]== "1":
                    resultado= "4"
                else:
                    resultado= "5"
            print(len(listaResultados))

            n4.resultado= resultado
            n4.save()

            datosGuardados= True
            #return redirect(reverse('n4', args=[idMuestra]))

                        
        else:
            print ("error")
            formN4.add_error(None, f'Error en el formulario, revisa los datos {formN4.errors}')
            
            return render(request, 'ensayos/nuevosEnsayos/n4.html', {
                'ensayo': ensayo,
                'formN4': formN4,
                'formN4Resultados': formN4Resultados,
                'equiposEnsayo': equiposEnsayo,
                'datosGuardados': datosGuardados,
            })
    else:
        if muestra_id != 'nueva':
            ensayo_N4= N4.objects.get(muestra__id= muestra_id) 
            equipos= ensayo_N4.equipos.all()        
            
            muestra= Muestras.objects.get(id=muestra_id) 
            fechaInicio= str(ensayo_N4.fechaInicio)
            fechaFin= str(ensayo_N4.fechaFin)
            temperaturaAmbiente= ensayo_N4.temperaturaAmbiente
            humedad=ensayo_N4.humedad
            observacion= ensayo_N4.observacion
            
            
            formN4 = N4Form(prefix='n4', initial={
                'muestra': muestra,
                'fechaInicio': fechaInicio,
                'fechaFin': fechaFin,
                'temperaturaAmbiente': temperaturaAmbiente,
                'humedad': humedad,
                'observacion': observacion,
                })
            
            formN4.fields['muestra'].queryset = Muestras.objects.filter(id=muestra_id)

            resultados= ResultadosN4.objects.filter(ensayo=ensayo_N4).order_by("id")

            initial_data = []
            for resultado in resultados:
                initial_data.append({
                    'celda': resultado.celda,
                    'tConsigna': resultado.tConsigna,
                    'tMax': resultado.tMax,
                    'tiempo': resultado.tiempo,
                    'resultado': resultado.resultado,
                    
                })
            
            while len(initial_data) != 4:
                initial_data.append({
                    'celda': "",
                    'tConsigna': "",
                    'tMax': "",
                    'tiempo': "",
                    'resultado': "",
                    
                })
                
            
            # Crear el formset con los datos iniciales
            N4ResultadosFormSet = formset_factory(N4ResultadosForm, extra=0)
            formN4Resultados = N4ResultadosFormSet(prefix='n4Resultados',initial=initial_data)

            equiposEnsayo= EquiposEnsayoForm(prefix= 'equiposEnsayo', initial= {'equiposEnsayo': equipos})
        
        else:
            formN4= N4Form(prefix='n4')
            formN4.fields['muestra'].queryset = muestras_queryset

            formN4Resultados=n4ResultadosFormSet(prefix='n4Resultados') 
            equiposEnsayo= EquiposEnsayoForm(prefix= 'equiposEnsayo', initial= {'equiposEnsayo': equipos})           


    return render(request, 'ensayos/nuevosEnsayos/n4.html', {
        'ensayo': ensayo,
        'formN4': formN4,
        'formN4Resultados': formN4Resultados,
        'equiposEnsayo': equiposEnsayo,
        'datosGuardados': datosGuardados,
    })

@login_required
def o1 (request, muestra_id):
     #Sacamos el ensayo
    ensayo= get_object_or_404(ListaEnsayos, ensayo= "O1")
    equipos= get_list_or_404(Equipos, ensayos=ensayo)
    datosGuardados= False
    usuario= request.user
  
    #Filtramos las muestras que pueden salir
    muestras_queryset= Muestras.objects.filter(
        Q(o1__resultado__isnull=True) & Q(listaEnsayos__ensayo__icontains="o1") & ~Q(estado=1)
    )

    if request.method == 'POST':
        #O1ibimos los formularios diferenciándolos con el prefijo
        formO1= O1Form(request.POST, prefix='o1')
        formO1Resultados= o1ResultadosFormSet(request.POST, prefix='o1Resultados') 

        equiposEnsayo= EquiposEnsayoForm(request.POST, prefix= 'equiposEnsayo') 
        
        if formO1.is_valid() and formO1Resultados.is_valid() and equiposEnsayo.is_valid():

            muestra= get_object_or_404(Muestras, id= request.POST.get('o1-muestra')) 
            
            #Comprobamos que no exista un ensayo  previo
            o1_instancia= O1.objects.filter(muestra= muestra)
            o1_instancia.delete()

            
            #Guardamos el formulario  a falta del resultado final
            fechaInicio= formO1.cleaned_data['fechaInicio']
            fechaFin= formO1.cleaned_data['fechaFin']
            temperaturaAmbiente= formO1.cleaned_data['temperaturaAmbiente']
            humedad= formO1.cleaned_data['humedad']
            observacion=formO1.cleaned_data['observacion']

            o1= O1.objects.create(
                muestra=muestra,
                ensayo=ensayo,
                temperaturaAmbiente= temperaturaAmbiente,
                humedad= humedad,
                fechaInicio= fechaInicio,
                fechaFin= fechaFin,
                observacion= observacion,
                usuario= usuario,
            )
            equipos= equiposEnsayo.cleaned_data['equiposEnsayo']
            o1.equipos.set (equipos)

            #Eliminamos los resultados
            resultadosAnteriores= ResultadosO1.objects.filter(ensayo= o1)
            if resultadosAnteriores:
                for resultado in resultadosAnteriores:
                    resultado.delete()

            
            #Guardamos los resultados en la tabla de resultados O1 
            listaResultados= [] 
            listaResultadosReferencia=[] 
            listaRebasaHumedad= []
            nEnsayo= 1

            for form in formO1Resultados:
                if form.cleaned_data:  # Para evitar formularios vacíos
                    
                    proporcion= form.cleaned_data['proporcion']
                    tiempo1= form.cleaned_data['tiempo1']
                    tiempo2= form.cleaned_data['tiempo2']
                    tiempo3= form.cleaned_data['tiempo3']
                    tiempo4= form.cleaned_data['tiempo4']
                    tiempo5= form.cleaned_data['tiempo5']
                    resultado= form.cleaned_data['resultado']

                    #Los tres primeros son ensayos de referencia, los otros dos son los ensayos normales
                    if nEnsayo <= 3:
                        nEnsayo= nEnsayo + 1
                        ensayoReferencia= True
                        listaResultadosReferencia.append({"proporcion": proporcion, "resultado": resultado}) 
                    else:
                        ensayoReferencia= False
                        listaResultados.append(resultado)

                    resultadosO1=ResultadosO1.objects.create(
                        ensayo= o1,
                        ensayoReferencia= ensayoReferencia,
                        proporcion= proporcion,
                        tiempo1= tiempo1,
                        tiempo2= tiempo2,
                        tiempo3= tiempo3,
                        tiempo4= tiempo4,
                        tiempo5= tiempo5,
                        resultado= resultado,
                    )
              

            #Resultado ensayo
            print(listaResultados) 
            print(listaResultadosReferencia) 
            
            #Sacamos valor de referencia con el que comparar los resultados
            valorReferencia= min(listaResultados)
            tiempo37= [d["resultado"] for d in listaResultadosReferencia if d["proporcion"] == "1"]
            tiempo64= [d["resultado"] for d in listaResultadosReferencia if d["proporcion"] == "2"]
            tiempo46= [d["resultado"] for d in listaResultadosReferencia if d["proporcion"] == "3"]

            print(tiempo37)
            resultadoEnsayo= "1"

            if valorReferencia <= tiempo37[0]:
                resultadoEnsayo= "2"
            if valorReferencia <= tiempo64[0]:
                resultadoEnsayo= "3"
            if valorReferencia <= tiempo46[0]:
                resultadoEnsayo= "4"

            #Guardamos en el modelo O1 el resultado del ensayo
            o1.resultado= resultadoEnsayo
            o1.save()

            datosGuardados= True

        else:
            print (formO1Resultados.errors)
            formO1.add_error(None, 'Error en el formulario, revisa los datos')
            return render(request, 'ensayos/nuevosEnsayos/o1.html', {
                'ensayo': ensayo,
                'formO1': formO1,
                'formO1Resultados': formO1Resultados,
                'equiposEnsayo': equiposEnsayo,
                'datosGuardados': datosGuardados,
            })
    else:
        if muestra_id != 'nueva':
            ensayo_O1= O1.objects.get(muestra__id= muestra_id)    
            equipos= ensayo_O1.equipos.all()        
            
            muestra= Muestras.objects.get(id=muestra_id) 
            fechaInicio= str(ensayo_O1.fechaInicio)
            fechaFin= str(ensayo_O1.fechaFin)
            temperaturaAmbiente= ensayo_O1.temperaturaAmbiente
            humedad=ensayo_O1.humedad
            observacion= ensayo_O1.observacion
            
            
            formO1 = O1Form(prefix='o1', initial={
                'muestra': muestra,
                'fechaInicio': fechaInicio,
                'fechaFin': fechaFin,
                'temperaturaAmbiente': temperaturaAmbiente,
                'humedad': humedad,
                'observacion': observacion,
                })
            
            formO1.fields['muestra'].queryset = Muestras.objects.filter(id=muestra_id)

            resultados= ResultadosO1.objects.filter(ensayo=ensayo_O1).order_by("id")


            initial_data = []
            for resultado in resultados:
                initial_data.append({
                    'proporcion': resultado.proporcion,
                    'tiempo1': resultado.tiempo1,
                    'tiempo2': resultado.tiempo2,
                    'tiempo3': resultado.tiempo3,
                    'tiempo4': resultado.tiempo4,
                    'tiempo5': resultado.tiempo5,
                    "resultado": resultado.resultado
                })
            
            # Crear el formset con los datos iniciales
            O1ResultadosFormSet = formset_factory(O1ResultadosForm, extra=0)
            if initial_data:
                formO1Resultados = O1ResultadosFormSet(prefix='o1Resultados',initial=initial_data)
            else:
                formO1Resultados= o1ResultadosFormSet(prefix='o1Resultados')

            equiposEnsayo= EquiposEnsayoForm(prefix= 'equiposEnsayo', initial= {'equiposEnsayo': equipos})

        
        else:
            formO1= O1Form(prefix='o1')
            formO1.fields['muestra'].queryset = muestras_queryset

            formO1Resultados=o1ResultadosFormSet(prefix='o1Resultados')   

            equiposEnsayo= EquiposEnsayoForm(prefix= 'equiposEnsayo', initial= {'equiposEnsayo': equipos})         


    return render(request, 'ensayos/nuevosEnsayos/o1.html', {
        'ensayo': ensayo,
        'formO1': formO1,
        'formO1Resultados': formO1Resultados,
        'equiposEnsayo': equiposEnsayo,
        'datosGuardados': datosGuardados,
    })

@login_required
def tratamiento (request, muestra_id):
     #Sacamos el ensayo
    ensayo= get_object_or_404(ListaEnsayos, ensayo= "Tratamiento")
    datosGuardados= False
    usuario= request.user
  
    #Filtramos las muestras que pueden salir
    muestras_queryset= Muestras.objects.filter(
        Q(tratamiento__secado__isnull=True) & Q(tratamiento__molido__isnull=True) & Q(tratamiento__tamizado__isnull=True) & Q(listaEnsayos__ensayo__icontains="tratamiento") & ~Q(estado=1)
    )

    if request.method == 'POST':
        #Creamos los formularios diferenciándolos con el prefijo
        formTratamiento= TratamientoForm(request.POST, prefix='tratamiento') 
        
        if formTratamiento.is_valid():
            muestra= get_object_or_404(Muestras, id= request.POST.get('tratamiento-muestra'))  
            
            #Comprobamos que no exista un ensayo  previo
            tratamiento_instancia= Tratamiento.objects.filter(muestra= muestra)
            tratamiento_instancia.delete()

            #Guardamos el formulario 
            if formTratamiento.cleaned_data:
                secado= formTratamiento.cleaned_data["secado"]
                equipoSecado= formTratamiento.cleaned_data["equipoSecado"]
                fechaSecadoInicio= formTratamiento.cleaned_data["fechaSecadoInicio"]
                fechaSecadoFin=formTratamiento.cleaned_data["fechaSecadoFin"]
                temperatura= formTratamiento.cleaned_data["temperatura"]
                tiempo= formTratamiento.cleaned_data["tiempo"]

                molido= formTratamiento.cleaned_data["molido"]
                equipoMolido= formTratamiento.cleaned_data["equipoMolido"]
                fechaMolidoInicio= formTratamiento.cleaned_data["fechaMolidoInicio"]
                fechaMolidoFin= formTratamiento.cleaned_data["fechaMolidoFin"]

                tamizado= formTratamiento.cleaned_data["tamizado"]
                equipoTamizado= formTratamiento.cleaned_data["equipoTamizado"]
                fechaTamizadoInicio= formTratamiento.cleaned_data["fechaTamizadoInicio"]
                fechaTamizadoFin=formTratamiento.cleaned_data["fechaTamizadoFin"]

            tratamiento= Tratamiento.objects.create(
                muestra=muestra,
                ensayo=ensayo,
                secado=secado,
                fechaSecadoInicio= fechaSecadoInicio,
                fechaSecadoFin= fechaSecadoFin,
                temperatura= temperatura,
                tiempo= tiempo,

                molido=molido,
                fechaMolidoInicio= fechaMolidoInicio,
                fechaMolidoFin= fechaMolidoFin,

                tamizado= tamizado,
                fechaTamizadoInicio= fechaTamizadoInicio,
                fechaTamizadoFin=fechaTamizadoFin,
                
                usuario= usuario,
                
            )
            if equipoSecado:
                if isinstance(equipoSecado, (list, tuple, set)):  # Si es iterable
                    tratamiento.equipoSecado.set(equipoSecado)
                else:  # Si no es iterable, lo pasamos como una lista
                    tratamiento.equipoSecado.set([equipoSecado])

            if equipoMolido:
                if isinstance(equipoMolido, (list, tuple, set)):  # Si es iterable
                    tratamiento.equipoMolido.set(equipoMolido)
                else:  # Si no es iterable, lo pasamos como una lista
                    tratamiento.equipoMolido.set([equipoMolido])

            if equipoTamizado:
                if isinstance(equipoTamizado, (list, tuple, set)):  # Si es iterable
                    tratamiento.equipoTamizado.set(equipoTamizado)
                else:  # Si no es iterable, lo pasamos como una lista
                    tratamiento.equipoTamizado.set([equipoTamizado])
            
            datosGuardados= True
        else:
            print("No valido")
            print (formTratamiento.errors)
            formTratamiento.add_error(None, 'Error en el formulario, revisa los datos')
            return render(request, 'ensayos/nuevosEnsayos/tratamiento.html', {
                'ensayo': ensayo,
                'formTratamiento': formTratamiento,
                'datosGuardados': datosGuardados,
            })
    else:
        if muestra_id != 'nueva':
            ensayo_tratamiento= Tratamiento.objects.get(muestra__id= muestra_id)            
            
            muestra= Muestras.objects.get(id=muestra_id) 

            secado= ensayo_tratamiento.secado
            equipoSecado= list(ensayo_tratamiento.equipoSecado.values_list('id', flat=True))
            fechaSecadoInicio= str(ensayo_tratamiento.fechaSecadoInicio)
            fechaSecadoFin= str(ensayo_tratamiento.fechaSecadoFin)
            temperatura= ensayo_tratamiento.temperatura
            tiempo=ensayo_tratamiento.tiempo

            molido= ensayo_tratamiento.molido
            equipoMolido= list(ensayo_tratamiento.equipoMolido.values_list('id', flat=True))
            fechaMolidoInicio= str(ensayo_tratamiento.fechaMolidoInicio)
            fechaMolidoFin= str(ensayo_tratamiento.fechaMolidoFin)

            tamizado= ensayo_tratamiento.tamizado
            equipoTamizado= list(ensayo_tratamiento.equipoTamizado.values_list('id', flat=True))
            fechaTamizadoInicio= str(ensayo_tratamiento.fechaTamizadoInicio)
            fechaTamizadoFin=str(ensayo_tratamiento.fechaTamizadoFin)
            
            formTratamiento = TratamientoForm(prefix='tratamiento', initial={
                "muestra": muestra,
                "secado":secado,
                "fechaSecadoInicio": fechaSecadoInicio,
                "fechaSecadoFin": fechaSecadoFin,
                "tiempo":tiempo,
                "temperatura": temperatura,
                "molido":molido,
                "fechaMolidoInicio": fechaMolidoInicio,
                "fechaMolidoFin": fechaMolidoFin,
                "tamizado": tamizado,
                "fechaTamizadoInicio": fechaTamizadoInicio,
                "fechaTamizadoFin":fechaTamizadoFin,
                "equipoSecado": equipoSecado,
                "equipoMolido": equipoMolido,
                "equipoTamizado": equipoTamizado,
            })
            print (formTratamiento)
             # type: ignore
            formTratamiento.fields['muestra'].queryset = Muestras.objects.filter(id=muestra_id)
        
        else:
            formTratamiento= TratamientoForm(prefix='tratamiento')
            formTratamiento.fields['muestra'].queryset = muestras_queryset  


    return render(request, 'ensayos/nuevosEnsayos/tratamiento.html', {
        'ensayo': ensayo,
        'formTratamiento': formTratamiento,
        'datosGuardados': datosGuardados,
    })