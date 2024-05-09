from django.shortcuts import render, get_list_or_404, get_object_or_404
from .forms import HumedadForm, EquiposForm
from .models import *
from muestras.models import ListaEnsayos, Muestras
from ensayos.models import Resultados
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
    print(ensayo_id)
    resultados= Resultados.objects.filter(ensayo= ensayo_id)
    
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
    
    #Filtramos las muestras que pueden salir
    muestras_queryset= Muestras.objects.filter(
        Q(humedad__isnull=True) & Q(listaEnsayos__ensayo__icontains="humedad") & ~Q(estado=1)
    )
    
    if request.method == 'POST':
               
        form = HumedadForm(request.POST)
        print(form.errors)

        if form.is_valid():
            muestra= get_object_or_404(Muestras, id= request.POST.get('muestra'))
            ensayo= get_object_or_404(ListaEnsayos, ensayo= "humedad")
            equipos= get_list_or_404(Equipos, ensayos=ensayo)

            #Comprobamos que exista un resultado sin valor para poder asignar el valor
            resultadoAsignado= Resultados.objects.get(muestra=muestra, ensayo=ensayo)
            print (resultadoAsignado)
            

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
                    resultado= resultadoAsignado
            )
            
            #Añadimos los equipos
            humedad.equipos.set(equipos)
            
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
            
            resultadoAsignado.resultado= resultado
            resultadoAsignado.save()


            
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

    return render(request, 'ensayos/nuevosEnsayos/humedad.html', {'form': form})

