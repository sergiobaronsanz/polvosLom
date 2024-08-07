from django.shortcuts import render, get_list_or_404, get_object_or_404
from .forms import *
from .models import *
from muestras.models import ListaEnsayos, Muestras
from django.db.models import Q

# Create your views here.

#Lista Ensayos

def listaEnsayos(request):
    listaEnsayos= ListaEnsayos.objects.all()
    
    return render (request, "ensayos/listaEnsayos/listaEnsayos.html",{
        'ensayos': listaEnsayos,
    })

def ensayosRealizados(request, ensayo):
    ensayo_id= ListaEnsayos.objects.get(ensayo=ensayo)
    print(ensayo_id.ensayo)

    #filtramos por tipo de ensayo

    if ensayo_id.ensayo == "Humedad":
        resultados= Humedad.objects.all()
    if ensayo_id.ensayo== "Granulometria":
        resultados= Granulometria.objects.all()
    if ensayo_id.ensayo== "TMIc":
        resultados= TMIc.objects.all()
    else:
        resultados= None
    
    #resultados= Resultados.objects.filter(ensayo= ensayo_id)
    
    return render(request, "ensayos/listaEnsayos/ensayosRealizados.html",{
        'resultados': resultados,
        'ensayo': ensayo,
    })

#Equipos
def equipos (request):
    equipos= Equipos.objects.all().order_by()
    
    return render (request, "ensayos/equipos/equipos.html",{
        'equipos': equipos
        
    })
    
def nuevoEquipo (request):
    if request.method == "POST":
        form= EquiposForm(request.POST)
        
        if form.is_valid():
            form.save()

            return redirect ("equipos")
               
    else:
        form= EquiposForm()
    
    return render (request, "ensayos/equipos/nuevoEquipo.html",{
        'equipos': equipos,
        'form': EquiposForm,
        
    })

#Ensayos
def humedad(request, muestra_id): #################################### Hay que cambiar muestras_id por humedad_id para así poder tener varias humedades en una misma muestra
    #Sacamos el ensayo
    ensayo= get_object_or_404(ListaEnsayos, ensayo= "humedad")

    #Filtramos las muestras que pueden salir
    muestras_queryset= Muestras.objects.filter(
        Q(humedad__resultado__isnull=True) & Q(listaEnsayos__ensayo__icontains="humedad") & ~Q(estado=1)
    )
    
    if request.method == 'POST':
               
        form = HumedadForm(request.POST)
        print(form.errors)

        if form.is_valid():
            muestra= get_object_or_404(Muestras, id= request.POST.get('muestra'))
            equipos= get_list_or_404(Equipos, ensayos=ensayo)            

            #Agregamos los campos
            fecha= request.POST.get('fecha')
            temperaturaAmbiente= float(request.POST.get('temperaturaAmbiente'))
            humedad= float(request.POST.get('humedad'))
            criterio= float(request.POST.get('criterio'))
            tiempoEnsayo= request.POST.get('tiempoEnsayo')
            tDesecacion= float(request.POST.get('tDesecacion'))
            desviacion= float(request.POST.get('desviacion'))
            resultado1= float(request.POST.get('resultado1'))
            resultado2= float(request.POST.get('resultado2'))
            resultado3= float(request.POST.get('resultado3'))
            resultado4= request.POST.get('resultado4')
            resultado5= request.POST.get('resultado5')
            resultado6= request.POST.get('resultado6')
            resultado7= request.POST.get('resultado7')
            resultado8= request.POST.get('resultado8')
            resultado9= request.POST.get('resultado9')
            resultado10= request.POST.get('resultado10')
            observacion= request.POST.get("observacion")
            
            
            #Comprobamos que no exista un ensayo de humedad previo
            humedad_instancia= Humedad.objects.filter(muestra= muestra)
            humedad_instancia.delete()
            
            
            #Si tiempo desecacion no es "" lo añadimos
            if tiempoEnsayo:
                tiempoEnsayo= float(tiempoEnsayo)
                humedad.tiempoEnsayo=tiempoEnsayo
            
            #Sacamos la media del resultado     
            resultado= 0
            listaResultados=[]
            
            if float(desviacion) >= 0.15:
                listaResultados = [
                    resultado1, resultado2, resultado3,
                    float(resultado4), float(resultado5), float(resultado6),
                    float(resultado7), float(resultado8), float(resultado9),
                    float(resultado10),
                ]
                
                longitud_lista= len(listaResultados)
                
                sumatorio=0
                for valor in listaResultados:
                    sumatorio += valor
                    resultado= sumatorio/longitud_lista
            else:
                listaResultados = [
                    resultado1, resultado2, resultado3,
                ]
                
                longitud_lista= len(listaResultados)
                
                sumatorio=0
                for valor in listaResultados:
                    sumatorio += valor
                    resultado= sumatorio/longitud_lista
            
            #Guardamos los valores en la tabla resultados                
            resultado= round(resultado, 2)  

            #Guardamos los datos en el servidor
            
            humedad= Humedad.objects.create(
                    muestra= muestra,
                    fecha= fecha, 
                    ensayo= ensayo,
                    temperaturaAmbiente= temperaturaAmbiente,
                    humedad= humedad,
                    tDesecacion= tDesecacion,
                    criterio= criterio,
                    desviacion=desviacion,
                    observacion= observacion,
                    resultado= resultado
            )
            
            #Añadimos los equipos
            humedad.equipos.set(equipos)           
            
            #Guardamos los resultados en la base de datos      
            for valor in listaResultados:
                resultado= ResultadosHumedad.objects.create(
                    ensayo= humedad,
                    resultado= valor,
                )
            
            

            
            ############################################################################################
            #POSIBILIDAD DE ELIMINAR LOS ENSAYOS QUE HAYA DE HUM PARA DICHA MUESTRA ANTES DE GUADAR OTRO,
            #SI NO, SE VAN A REPETIR LOS ENSAYOS
            ############################################################################################
            return redirect ("inicio")
        else:
            print("no valido")
    else:
        if muestra_id != "nueva":
            ensayo= Humedad.objects.get(muestra__id= muestra_id)
            resultados= ResultadosHumedad.objects.filter(ensayo=ensayo).order_by('id')
            
            
            muestra= Muestras.objects.get(id=muestra_id) 
            fecha= str(ensayo.fecha)
            temperaturaAmbiente= ensayo.temperaturaAmbiente
            humedad=ensayo.humedad
            criterio= ensayo.criterio
            tiempoEnsayo= ensayo.tiempoEnsayo
            tDesecacion= ensayo.tDesecacion
            desviacion= ensayo.desviacion
            
            resultado1=0
            
            print(resultados)
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
                'fecha': fecha,
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
            
            form.fields['muestra'].queryset = Muestras.objects.filter(id=muestra_id)
            
        else:
            form = HumedadForm()
            form.fields['muestra'].queryset = muestras_queryset

    return render(request, 'ensayos/nuevosEnsayos/humedad.html', {
        'form': form, 
        'ensayo': ensayo,
        })


def granulometria(request, muestra_id):
    #Sacamos el ensayo
    ensayo= get_object_or_404(ListaEnsayos, ensayo= "granulometria")

    #Filtramos las muestras que pueden salir
    muestras_queryset= Muestras.objects.filter(
        Q(granulometria__resultado__isnull=True) & Q(listaEnsayos__ensayo__icontains="granulometria") & ~Q(estado=1)
    )

    if request.method == 'POST':
        form= GranulometriaForm(request.POST)

        if form.is_valid:
            #Recogemos los datos para guardarlos
            muestra= get_object_or_404(Muestras, id= request.POST.get('muestra'))
            equipos= get_list_or_404(Equipos, ensayos=ensayo)            

            #Agregamos los campos
            fecha= request.POST.get('fecha')
            temperaturaAmbiente= float(request.POST.get('temperaturaAmbiente'))
            humedad= float(request.POST.get('humedad'))
            via= float(request.POST.get('via'))
            d10= float(request.POST.get('d10'))
            d50= float(request.POST.get('d50'))
            d90= float(request.POST.get('d90'))
            observacion= request.POST.get("observacion")

            #Comprobamos que no exista un ensayo de humedad previo
            granulometria_instancia= Granulometria.objects.filter(muestra= muestra)
            granulometria_instancia.delete()

            granulometria= Granulometria.objects.create(
                muestra=muestra,
                ensayo=ensayo,
                temperaturaAmbiente= temperaturaAmbiente,
                humedad= humedad,
                fecha= fecha,
                via= via,
                d10=d10,
                d50= d50,
                d90= d90,
                resultado= d50,
                observacion=observacion
            )        

            granulometria.equipos.set (equipos)

            return redirect ("inicio")
    
    else:
        if muestra_id != 'nueva':
            ensayo= Granulometria.objects.get(muestra__id= muestra_id)            
            
            muestra= Muestras.objects.get(id=muestra_id) 
            fecha= str(ensayo.fecha)
            temperaturaAmbiente= ensayo.temperaturaAmbiente
            humedad=ensayo.humedad
            via= ensayo.via
            d10= ensayo.d10
            d50= ensayo.d50
            d90= ensayo.d90
            
            
            form = GranulometriaForm(initial={
                'muestra': muestra,
                'fecha': fecha,
                'temperaturaAmbiente': temperaturaAmbiente,
                'humedad': humedad,
                'via':via,
                'd10': d10,
                'd50': d50,
                'd90': d90,
                })
            
            form.fields['muestra'].queryset = Muestras.objects.filter(id=muestra_id)

        else:
            form= GranulometriaForm()
            form.fields['muestra'].queryset = muestras_queryset


    return render(request, 'ensayos/nuevosEnsayos/granulometria.html', {
        'ensayo': ensayo,
        'form': form,
    })


def tmic(request, muestra_id):
    #Sacamos el ensayo
    ensayo= get_object_or_404(ListaEnsayos, ensayo= "TMIc")
  
    #Filtramos las muestras que pueden salir
    muestras_queryset= Muestras.objects.filter(
        Q(tmic__resultado__isnull=True) & Q(listaEnsayos__ensayo__icontains="tmic") & ~Q(estado=1)
    )

    if request.method == 'POST':
        #Recibimos los formularios diferenciándolos con el prefijo
        formTmic= TmicForm(request.POST, prefix='tmic')
        formTmicResultados= tmicResultadosFormSet(request.POST, prefix='tmicResultados')  
        
        if formTmic.is_valid() and formTmicResultados.is_valid():

            muestra= get_object_or_404(Muestras, id= request.POST.get('tmic-muestra'))
            equipos= get_list_or_404(Equipos, ensayos=ensayo)  
            
            #Comprobamos que no exista un ensayo de humedad previo
            tmic_instancia= TMIc.objects.filter(muestra= muestra)
            tmic_instancia.delete()

            
            #Guardamos el formulario de la capa a falta del resultado final
            fecha= formTmic.cleaned_data['fecha']
            temperaturaAmbiente= formTmic.cleaned_data['temperaturaAmbiente']
            humedad= formTmic.cleaned_data['humedad']
            tiempoMaxEnsayo= formTmic.cleaned_data['tiempoMaxEnsayo']
            observacion=formTmic.cleaned_data['observacion']

            tmic= TMIc.objects.create(
                muestra=muestra,
                ensayo=ensayo,
                temperaturaAmbiente= temperaturaAmbiente,
                humedad= humedad,
                fecha= fecha,
                tiempoMaxEnsayo=tiempoMaxEnsayo,
                observacion= observacion,
            )
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
                formTmic.add_error(None, 'No hay resultados positivos en el ensayo, revisa la tabla.')
                return render(request, 'ensayos/nuevosEnsayos/tmic.html', {
                    'ensayo': ensayo,
                    'formTmic': formTmic,
                    'formTmicResultados': formTmicResultados,
                })
                        
        else:
            print (formTmic.errors)
            formTmic.add_error(None, 'Error en el formulario, revisa los datos')
            return render(request, 'ensayos/nuevosEnsayos/tmic.html', {
                'ensayo': ensayo,
                'formTmic': formTmic,
                'formTmicResultados': formTmicResultados,
            })
    else:
        if muestra_id != 'nueva':
            ensayo_TMIc= TMIc.objects.get(muestra__id= muestra_id)            
            
            muestra= Muestras.objects.get(id=muestra_id) 
            fecha= str(ensayo_TMIc.fecha)
            temperaturaAmbiente= ensayo_TMIc.temperaturaAmbiente
            humedad=ensayo_TMIc.humedad
            tiempoMaxEnsayo= ensayo_TMIc.tiempoMaxEnsayo
            observacion= ensayo_TMIc.observacion
            
            
            formTmic = TmicForm(prefix='tmic', initial={
                'muestra': muestra,
                'fecha': fecha,
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

        
        else:
            formTmic= TmicForm(prefix='tmic')
            formTmic.fields['muestra'].queryset = muestras_queryset

            formTmicResultados=tmicResultadosFormSet(prefix='tmicResultados')            


    return render(request, 'ensayos/nuevosEnsayos/tmic.html', {
        'ensayo': ensayo,
        'formTmic': formTmic,
        'formTmicResultados': formTmicResultados,
    })


def tmin (request, muestra_id):
     #Sacamos el ensayo
    ensayo= get_object_or_404(ListaEnsayos, ensayo= "TMIn")
  
    #Filtramos las muestras que pueden salir
    muestras_queryset= Muestras.objects.filter(
        Q(tmin__resultado__isnull=True) & Q(listaEnsayos__ensayo__icontains="tmin") & ~Q(estado=1)
    )

    if request.method == 'POST':
        #Recibimos los formularios diferenciándolos con el prefijo
        formTmin= TminForm(request.POST, prefix='tmin')
        formTminResultados= tminResultadosFormSet(request.POST, prefix='tminResultados')  
        
        if formTmin.is_valid() and formTminResultados.is_valid():

            muestra= get_object_or_404(Muestras, id= request.POST.get('tmin-muestra'))
            equipos= get_list_or_404(Equipos, ensayos=ensayo)  
            
            #Comprobamos que no exista un ensayo de humedad previo
            tmin_instancia= TMIn.objects.filter(muestra= muestra)
            tmin_instancia.delete()

            
            #Guardamos el formulario de la capa a falta del resultado final
            fecha= formTmin.cleaned_data['fecha']
            temperaturaAmbiente= formTmin.cleaned_data['temperaturaAmbiente']
            humedad= formTmin.cleaned_data['humedad']
            tiempoMaxEnsayo= formTmin.cleaned_data['tiempoMaxEnsayo']
            observacion=formTmin.cleaned_data['observacion']

            tmin= TMIn.objects.create(
                muestra=muestra,
                ensayo=ensayo,
                temperaturaAmbiente= temperaturaAmbiente,
                humedad= humedad,
                fecha= fecha,
                tiempoMaxEnsayo=tiempoMaxEnsayo,
                observacion= observacion,
            )
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
                    tPlato = form.cleaned_data['tPlato']
                    tMax = form.cleaned_data['tMax']
                    resultadoPrueba= form.cleaned_data['resultadoPrueba']
                    tipoIgnicion= form.cleaned_data['tipoIgnicion']
                    tiempoPrueba= form.cleaned_data['tiempoPrueba']
                    tiempoMax= form.cleaned_data['tiempoMax']



                    resultadosTmin=ResultadosTMIn.objects.create(
                        ensayo=tmin,
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
                        tmin.funde= "1"

            #Guardamos en el modelo TMIn el resultado del ensayo
            if listaResultados:
                resultado= min(listaResultados)
                tmin.resultado= resultado
                tmin.save()
            else:
                formTmin.add_error(None, 'No hay resultados positivos en el ensayo, revisa la tabla.')
                return render(request, 'ensayos/nuevosEnsayos/tmin.html', {
                    'ensayo': ensayo,
                    'formTmin': formTmin,
                    'formTminResultados': formTminResultados,
                })
                        
        else:
            print (formTmin.errors)
            formTmin.add_error(None, 'Error en el formulario, revisa los datos')
            return render(request, 'ensayos/nuevosEnsayos/tmin.html', {
                'ensayo': ensayo,
                'formTmin': formTmin,
                'formTminResultados': formTminResultados,
            })
    else:
        if muestra_id != 'nueva':
            ensayo_TMIn= TMIn.objects.get(muestra__id= muestra_id)            
            
            muestra= Muestras.objects.get(id=muestra_id) 
            fecha= str(ensayo_TMIn.fecha)
            temperaturaAmbiente= ensayo_TMIn.temperaturaAmbiente
            humedad=ensayo_TMIn.humedad
            tiempoMaxEnsayo= ensayo_TMIn.tiempoMaxEnsayo
            observacion= ensayo_TMIn.observacion
            
            
            formTmin = TminForm(prefix='tmin', initial={
                'muestra': muestra,
                'fecha': fecha,
                'temperaturaAmbiente': temperaturaAmbiente,
                'humedad': humedad,
                'tiempoMaxEnsayo': tiempoMaxEnsayo,
                'observacion': observacion,
                })
            
            formTmin.fields['muestra'].queryset = Muestras.objects.filter(id=muestra_id)

            resultados= ResultadosTMIn.objects.filter(ensayo=ensayo_TMIn).order_by("id")

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
            TminResultadosFormSet = formset_factory(TminResultadosForm, extra=0)
            formTminResultados = TminResultadosFormSet(prefix='tminResultados',initial=initial_data)

        
        else:
            formTmin= TminForm(prefix='tmin')
            formTmin.fields['muestra'].queryset = muestras_queryset

            formTminResultados=tminResultadosFormSet(prefix='tminResultados')            


    return render(request, 'ensayos/nuevosEnsayos/tmin.html', {
        'ensayo': ensayo,
        'formTmin': formTmin,
        'formTminResultados': formTminResultados,
    })
