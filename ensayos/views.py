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
            resultado1= request.POST.get('resultado1')
            resultado2= request.POST.get('resultado2')
            resultado3= request.POST.get('resultado3')
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

                for valor in listaResultados:
                    resultado= ResultadosHumedad.objects.create(
                        ensayo= humedad,
                        resultado= valor,
                    )

            else:
                resultado = "N/D"
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
                resultado= ">400"
                tmic.resultado= resultado
                tmic.save()
                        
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
            
            #Comprobamos que no exista un ensayo  previo
            tmin_instancia= TMIn.objects.filter(muestra= muestra)
            tmin_instancia.delete()

            
            #Guardamos el formulario  a falta del resultado final
            fecha= formTmin.cleaned_data['fecha']
            temperaturaAmbiente= formTmin.cleaned_data['temperaturaAmbiente']
            humedad= formTmin.cleaned_data['humedad']
            observacion=formTmin.cleaned_data['observacion']

            tmin= TMIn.objects.create(
                muestra=muestra,
                ensayo=ensayo,
                temperaturaAmbiente= temperaturaAmbiente,
                humedad= humedad,
                fecha= fecha,
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
            observacion= ensayo_TMIn.observacion
            
            
            formTmin = TminForm(prefix='tmin', initial={
                'muestra': muestra,
                'fecha': fecha,
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

        
        else:
            formTmin= TminForm(prefix='tmin')
            formTmin.fields['muestra'].queryset = muestras_queryset

            formTminResultados=tminResultadosFormSet(prefix='tminResultados')            


    return render(request, 'ensayos/nuevosEnsayos/tmin.html', {
        'ensayo': ensayo,
        'formTmin': formTmin,
        'formTminResultados': formTminResultados,
    })


def lie (request, muestra_id):
     #Sacamos el ensayo
    ensayo= get_object_or_404(ListaEnsayos, ensayo= "LIE")
  
    #Filtramos las muestras que pueden salir
    muestras_queryset= Muestras.objects.filter(
        Q(lie__resultado__isnull=True) & Q(listaEnsayos__ensayo__icontains="lie") & ~Q(estado=1)
    )

    if request.method == 'POST':
        #Recibimos los formularios diferenciándolos con el prefijo
        formLie= LieForm(request.POST, prefix='lie')
        formLieResultados= lieResultadosFormSet(request.POST, prefix='lieResultados')  
        
        if formLie.is_valid() and formLieResultados.is_valid():

            muestra= get_object_or_404(Muestras, id= request.POST.get('lie-muestra'))
            equipos= get_list_or_404(Equipos, ensayos=ensayo)  
            
            #Comprobamos que no exista un ensayo  previo
            lie_instancia= LIE.objects.filter(muestra= muestra)
            lie_instancia.delete()

            
            #Guardamos el formulario  a falta del resultado final
            fecha= formLie.cleaned_data['fecha']
            temperaturaAmbiente= formLie.cleaned_data['temperaturaAmbiente']
            humedad= formLie.cleaned_data['humedad']
            cerillas= formLie.cleaned_data['cerillas']
            boquilla= formLie.cleaned_data['boquilla']
            observacion=formLie.cleaned_data['observacion']

            lie= LIE.objects.create(
                muestra=muestra,
                ensayo=ensayo,
                temperaturaAmbiente= temperaturaAmbiente,
                humedad= humedad,
                cerillas= cerillas,
                boquilla= boquilla,
                fecha= fecha,
                observacion= observacion,
            )
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
                        
        else:
            print (formLie.errors)
            formLie.add_error(None, 'Error en el formulario, revisa los datos')
            return render(request, 'ensayos/nuevosEnsayos/lie.html', {
                'ensayo': ensayo,
                'formLie': formLie,
                'formLieResultados': formLieResultados,
            })
    else:
        if muestra_id != 'nueva':
            ensayo_LIE= LIE.objects.get(muestra__id= muestra_id)            
            
            muestra= Muestras.objects.get(id=muestra_id) 
            fecha= str(ensayo_LIE.fecha)
            temperaturaAmbiente= ensayo_LIE.temperaturaAmbiente
            humedad=ensayo_LIE.humedad
            cerillas=ensayo_LIE.cerillas,
            boquilla=ensayo_LIE.boquilla,
            observacion= ensayo_LIE.observacion,
            
            
            formLie = LieForm(prefix='lie', initial={
                'muestra': muestra,
                'fecha': fecha,
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
        
        else:
            formLie= LieForm(prefix='lie')
            formLie.fields['muestra'].queryset = muestras_queryset

            formLieResultados=lieResultadosFormSet(prefix='lieResultados')            


    return render(request, 'ensayos/nuevosEnsayos/lie.html', {
        'ensayo': ensayo,
        'formLie': formLie,
        'formLieResultados': formLieResultados,
    })


def emi (request, muestra_id):
     #Sacamos el ensayo
    ensayo= get_object_or_404(ListaEnsayos, ensayo= "EMI")
  
    #Filtramos las muestras que pueden salir
    muestras_queryset= Muestras.objects.filter(
        Q(emi__resultado__isnull=True) & Q(listaEnsayos__ensayo__icontains="emi") & ~Q(estado=1)
    )

    if request.method == 'POST':
        #Recibimos los formularios diferenciándolos con el prefijo
        formEmi= EmiForm(request.POST, prefix='emi')
        formEmiResultados= emiResultadosFormSet(request.POST, prefix='emiResultados')  
        
        if formEmi.is_valid() and formEmiResultados.is_valid():

            muestra= get_object_or_404(Muestras, id= request.POST.get('emi-muestra'))
            equipos= get_list_or_404(Equipos, ensayos=ensayo)  
            
            #Comprobamos que no exista un ensayo  previo
            emi_instancia= EMI.objects.filter(muestra= muestra)
            emi_instancia.delete()

            
            #Guardamos el formulario  a falta del resultado final
            fecha= formEmi.cleaned_data['fecha']
            temperaturaAmbiente= formEmi.cleaned_data['temperaturaAmbiente']
            humedad= formEmi.cleaned_data['humedad']
            inductancia= formEmi.cleaned_data['inductancia']
            observacion=formEmi.cleaned_data['observacion']

            emi= EMI.objects.create(
                muestra=muestra,
                ensayo=ensayo,
                temperaturaAmbiente= temperaturaAmbiente,
                humedad= humedad,
                inductancia= inductancia,
                fecha= fecha,
                observacion= observacion,
            )
            emi.equipos.set (equipos)

            #Eliminamos los resultados
            resultadosAnteriores= ResultadosEMI.objects.filter(ensayo= emi)
            if resultadosAnteriores:
                for resultado in resultadosAnteriores:
                    resultado.delete()

            
            #Guardamos los resultados en la tabla de resultados EMI 
            listaResultados= []  

            for form in formEmiResultados:
                if form.cleaned_data:  # Para evitar formularios vacíos
                    concentracion = form.cleaned_data['concentracion']
                    energia= form.cleaned_data['energia']
                    retardo= form.cleaned_data['retardo']
                    resultadoPrueba= form.cleaned_data['resultadoPrueba']

                    resultadosEmi=ResultadosEMI.objects.create(
                        ensayo= emi,
                        concentracion= concentracion,
                        energia= energia,
                        retardo= retardo,
                        resultado=resultadoPrueba,
                    )

                    if resultadoPrueba == "1":
                        listaResultados.append(concentracion)
                    

            #Guardamos en el modelo EMI el resultado del ensayo
            if listaResultados:
                resultado= min(listaResultados)
                
                emi.resultado= resultado
                emi.save()
            else:
                resultado= ">1000"
                emi.resultado= resultado
                emi.save()
                
                        
        else:
            print (formEmi.errors)
            formEmi.add_error(None, 'Error en el formulario, revisa los datos')
            return render(request, 'ensayos/nuevosEnsayos/emi.html', {
                'ensayo': ensayo,
                'formEmi': formEmi,
                'formEmiResultados': formEmiResultados,
            })
    else:
        if muestra_id != 'nueva':
            ensayo_EMI= EMI.objects.get(muestra__id= muestra_id)            
            
            muestra= Muestras.objects.get(id=muestra_id) 
            fecha= str(ensayo_EMI.fecha)
            temperaturaAmbiente= ensayo_EMI.temperaturaAmbiente
            humedad=ensayo_EMI.humedad
            inductancia= ensayo_EMI.inductancia
            observacion= ensayo_EMI.observacion,
            
            
            formEmi = EmiForm(prefix='emi', initial={
                'muestra': muestra,
                'fecha': fecha,
                'temperaturaAmbiente': temperaturaAmbiente,
                'humedad': humedad,
                'inductancia': inductancia,
                'observacion': observacion,
                })
            
            formEmi.fields['muestra'].queryset = Muestras.objects.filter(id=muestra_id)

            resultados= ResultadosEMI.objects.filter(ensayo=ensayo_EMI).order_by("id")

            initial_data = []
            for resultado in resultados:
                initial_data.append({
                    'concentracion': resultado.concentracion,
                    'energia': resultado.energia,
                    'retardo': resultado.resultado,
                    'resultadoPrueba': resultado.resultado,
                })
            
            # Crear el formset con los datos iniciales
            EmiResultadosFormSet = formset_factory(EmiResultadosForm, extra=0)
            formEmiResultados = EmiResultadosFormSet(prefix='emiResultados',initial=initial_data)
        
        else:
            formEmi= EmiForm(prefix='emi')
            formEmi.fields['muestra'].queryset = muestras_queryset

            formEmiResultados=emiResultadosFormSet(prefix='emiResultados')            


    return render(request, 'ensayos/nuevosEnsayos/emi.html', {
        'ensayo': ensayo,
        'formEmi': formEmi,
        'formEmiResultados': formEmiResultados,
    })


def pmax (request, muestra_id):
     #Sacamos el ensayo
    ensayo= get_object_or_404(ListaEnsayos, ensayo= "Pmax")
  
    #Filtramos las muestras que pueden salir
    muestras_queryset= Muestras.objects.filter(
        Q(pmax__pmax__isnull=True) & Q(pmax__dpdt__isnull=True) & Q(pmax__kmax__isnull=True) & Q(listaEnsayos__ensayo__icontains="pmax") & ~Q(estado=1)
    )

    if request.method == 'POST':
        #Recibimos los formularios diferenciándolos con el prefijo
        formPmax= PmaxForm(request.POST, prefix='pmax')
        formPmaxResultados= pmaxResultadosFormSet(request.POST, prefix='pmaxResultados')  
        
        if formPmax.is_valid() and formPmaxResultados.is_valid():

            muestra= get_object_or_404(Muestras, id= request.POST.get('pmax-muestra'))
            equipos= get_list_or_404(Equipos, ensayos=ensayo)  
            
            #Comprobamos que no exista un ensayo  previo
            pmax_instancia= Pmax.objects.filter(muestra= muestra)
            pmax_instancia.delete()

            
            #Guardamos el formulario  a falta del resultado final
            fecha= formPmax.cleaned_data['fecha']
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
                fecha= fecha,
                observacion= observacion,
            )

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

                    print(form.cleaned_data)

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
                    return render(request, 'ensayos/nuevosEnsayos/pmax.html', {
                        'ensayo': ensayo,
                        'formPmax': formPmax,
                        'formPmaxResultados': formPmaxResultados,
                    })
                        
        else:
            print (formPmax.errors)
            formPmax.add_error(None, f'Error en el formulario, revisa los datos {formPmax.errors}')
            return render(request, 'ensayos/nuevosEnsayos/pmax.html', {
                'ensayo': ensayo,
                'formPmax': formPmax,
                'formPmaxResultados': formPmaxResultados,
            })
    else:
        if muestra_id != 'nueva':
            ensayo_Pmax= Pmax.objects.get(muestra__id= muestra_id)            
            
            muestra= Muestras.objects.get(id=muestra_id) 
            fecha= str(ensayo_Pmax.fecha)
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
                'fecha': fecha,
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
        
        else:
            formPmax= PmaxForm(prefix='pmax')
            formPmax.fields['muestra'].queryset = muestras_queryset

            formPmaxResultados=pmaxResultadosFormSet(prefix='pmaxResultados')            


    return render(request, 'ensayos/nuevosEnsayos/pmax.html', {
        'ensayo': ensayo,
        'formPmax': formPmax,
        'formPmaxResultados': formPmaxResultados,
    })


def clo (request, muestra_id):
     #Sacamos el ensayo
    ensayo= get_object_or_404(ListaEnsayos, ensayo= "CLO")
  
    #Filtramos las muestras que pueden salir
    muestras_queryset= Muestras.objects.filter(
        Q(clo__resultado__isnull=True) & Q(listaEnsayos__ensayo__icontains="clo") & ~Q(estado=1)
    )

    if request.method == 'POST':
        #Recibimos los formularios diferenciándolos con el prefijo
        formClo= CloForm(request.POST, prefix='clo')
        formCloResultados= cloResultadosFormSet(request.POST, prefix='cloResultados')  
        
        if formClo.is_valid() and formCloResultados.is_valid():

            muestra= get_object_or_404(Muestras, id= request.POST.get('clo-muestra'))
            equipos= get_list_or_404(Equipos, ensayos=ensayo)  
            
            #Comprobamos que no exista un ensayo  previo
            clo_instancia= CLO.objects.filter(muestra= muestra)
            clo_instancia.delete()

            
            #Guardamos el formulario  a falta del resultado final
            fecha= formClo.cleaned_data['fecha']
            temperaturaAmbiente= formClo.cleaned_data['temperaturaAmbiente']
            humedad= formClo.cleaned_data['humedad']
            cerillas= formClo.cleaned_data['cerillas']
            boquilla= formClo.cleaned_data['boquilla']
            observacion=formClo.cleaned_data['observacion']

            clo= CLO.objects.create(
                muestra=muestra,
                ensayo=ensayo,
                temperaturaAmbiente= temperaturaAmbiente,
                humedad= humedad,
                cerillas= cerillas,
                boquilla= boquilla,
                fecha= fecha,
                observacion= observacion,
            )
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

                    if resultadoPrueba == "1":
                        listaResultados.append(concentracion)
                    

            #Guardamos en el modelo CLO el resultado del ensayo
            if listaResultados:
                valor_buscado = min(listaResultados)

                clo.resultado= valor_buscado
                clo.save()
            else:
                resultado= "N/D"
                clo.resultado= resultado
                clo.save()

                        
        else:
            print (formClo.errors)
            formClo.add_error(None, 'Error en el formulario, revisa los datos')
            return render(request, 'ensayos/nuevosEnsayos/clo.html', {
                'ensayo': ensayo,
                'formClo': formClo,
                'formCloResultados': formCloResultados,
            })
    else:
        if muestra_id != 'nueva':
            ensayo_CLO= CLO.objects.get(muestra__id= muestra_id)            
            
            muestra= Muestras.objects.get(id=muestra_id) 
            fecha= str(ensayo_CLO.fecha)
            temperaturaAmbiente= ensayo_CLO.temperaturaAmbiente
            humedad=ensayo_CLO.humedad
            cerillas=ensayo_CLO.cerillas,
            boquilla=ensayo_CLO.boquilla,
            observacion= ensayo_CLO.observacion,
            
            
            formClo = CloForm(prefix='clo', initial={
                'muestra': muestra,
                'fecha': fecha,
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
        
        else:
            formClo= CloForm(prefix='clo')
            formClo.fields['muestra'].queryset = muestras_queryset

            formCloResultados=cloResultadosFormSet(prefix='cloResultados')            


    return render(request, 'ensayos/nuevosEnsayos/clo.html', {
        'ensayo': ensayo,
        'formClo': formClo,
        'formCloResultados': formCloResultados,
    })


def rec (request, muestra_id):
     #Sacamos el ensayo
    ensayo= get_object_or_404(ListaEnsayos, ensayo= "REC")
  
    #Filtramos las muestras que pueden salir
    muestras_queryset= Muestras.objects.filter(
        Q(rec__resultado__isnull=True) & Q(listaEnsayos__ensayo__icontains="rec") & ~Q(estado=1)
    )

    if request.method == 'POST':
        #Recibimos los formularios diferenciándolos con el prefijo
        formRec= RecForm(request.POST, prefix='rec')
        formRecResultados= recResultadosFormSet(request.POST, prefix='recResultados')  
        
        if formRec.is_valid() and formRecResultados.is_valid():

            muestra= get_object_or_404(Muestras, id= request.POST.get('rec-muestra'))
            equipos= get_list_or_404(Equipos, ensayos=ensayo)  
            
            #Comprobamos que no exista un ensayo  previo
            rec_instancia= REC.objects.filter(muestra= muestra)
            rec_instancia.delete()

            
            #Guardamos el formulario  a falta del resultado final
            fecha= formRec.cleaned_data['fecha']
            temperaturaAmbiente= formRec.cleaned_data['temperaturaAmbiente']
            humedad= formRec.cleaned_data['humedad']
            observacion=formRec.cleaned_data['observacion']

            rec= REC.objects.create(
                muestra=muestra,
                ensayo=ensayo,
                temperaturaAmbiente= temperaturaAmbiente,
                humedad= humedad,
                fecha= fecha,
                observacion= observacion,
            )
            rec.equipos.set (equipos)

            #Eliminamos los resultados
            resultadosAnteriores= ResultadosREC.objects.filter(ensayo= rec)
            if resultadosAnteriores:
                for resultado in resultadosAnteriores:
                    resultado.delete()

            
            #Guardamos los resultados en la tabla de resultados REC 
            listaResultados= []  

            for form in formRecResultados:
                if form.cleaned_data:  # Para evitar formularios vacíos
                    tension= form.cleaned_data['tension']
                    tiempo= form.cleaned_data['tiempo']
                    resultadoPrueba= form.cleaned_data['resultadoPrueba']

                    resultadosRec=ResultadosREC.objects.create(
                        ensayo= rec,
                        tension= tension,
                        tiempo= tiempo,
                        resultado=resultadoPrueba,
                    )

                    if resultadoPrueba == "1":
                        listaResultados.append(concentracion)
                    

            #Guardamos en el modelo REC el resultado del ensayo
            if listaResultados:
                valor_buscado = min(listaResultados)

                rec.resultado= valor_buscado
                rec.save()
            else:
                resultado= "N/D"
                rec.resultado= resultado
                rec.save()

                        
        else:
            print (formRec.errors)
            formRec.add_error(None, 'Error en el formulario, revisa los datos')
            return render(request, 'ensayos/nuevosEnsayos/rec.html', {
                'ensayo': ensayo,
                'formRec': formRec,
                'formRecResultados': formRecResultados,
            })
    else:
        if muestra_id != 'nueva':
            ensayo_REC= REC.objects.get(muestra__id= muestra_id)            
            
            muestra= Muestras.objects.get(id=muestra_id) 
            fecha= str(ensayo_REC.fecha)
            temperaturaAmbiente= ensayo_REC.temperaturaAmbiente
            humedad=ensayo_REC.humedad
            cerillas=ensayo_REC.cerillas,
            boquilla=ensayo_REC.boquilla,
            observacion= ensayo_REC.observacion,
            
            
            formRec = RecForm(prefix='rec', initial={
                'muestra': muestra,
                'fecha': fecha,
                'temperaturaAmbiente': temperaturaAmbiente,
                'humedad': humedad,
                'cerillas': cerillas,
                'boquilla': boquilla,
                'observacion': observacion,
                })
            
            formRec.fields['muestra'].queryset = Muestras.objects.filter(id=muestra_id)

            resultados= ResultadosREC.objects.filter(ensayo=ensayo_REC).order_by("id")

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
            RecResultadosFormSet = formset_factory(RecResultadosForm, extra=0)
            formRecResultados = RecResultadosFormSet(prefix='recResultados',initial=initial_data)
        
        else:
            formRec= RecForm(prefix='rec')
            formRec.fields['muestra'].queryset = muestras_queryset

            formRecResultados=recResultadosFormSet(prefix='recResultados')            


    return render(request, 'ensayos/nuevosEnsayos/rec.html', {
        'ensayo': ensayo,
        'formRec': formRec,
        'formRecResultados': formRecResultados,
    })