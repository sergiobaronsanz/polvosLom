from django.shortcuts import render, get_list_or_404, get_object_or_404
from .forms import HumedadForm, EquiposForm
from .models import *
from ensayos.models import ListaEnsayos
from muestras.models import Muestras
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
               
    else:
        form= EquiposForm()
    
    return render (request, "ensayos/equipos/nuevoEquipo.html",{
        'equipos': equipos,
        'form': EquiposForm,
        
    })

#Ensayos
def humedad(request, muestra_id):
    
    #Filtramos las muestras que pueden salir
    muestras_queryset= Muestras.objects.filter(
        Q(humedad__isnull=True) & Q(listaEnsayos__ensayo__icontains="humedad")
    )
    
    if request.method == 'POST':
               
        form = HumedadForm(request.POST)
        print(form.errors)

        if form.is_valid():
            muestra= get_object_or_404(Muestras, id= request.POST.get('muestra'))
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
            
            ensayo= get_object_or_404(ListaEnsayos, ensayo= "humedad")
            equipos= get_list_or_404(Equipos, ensayos=ensayo)
            print(desviacion)
            
            #Comprobamos si hay un ensayo creado
            humedad_existente= Humedad.objects.filter (muestra=muestra)
            
            if humedad_existente.exists():
                mensaje_error = "Ya existe una humedad para esta muestra"
                humedad_existente.delete()
                return render(request, 'ensayos/nuevosEnsayos/humedad.html', {'form': form, 'mensaje_error': mensaje_error})
            
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
            
            print(listaResultados)
                            
            resultado= round(resultado, 2)             
            #Guardamos los valores en la tabla resultados
            resultados= Resultados.objects.create(
                muestra= muestra,
                ensayo= ensayo,
                resultado= resultado,
                unidades= "%",
            )
            
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

