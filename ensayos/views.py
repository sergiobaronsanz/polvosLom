from django.shortcuts import render, get_list_or_404, get_object_or_404
from .forms import HumedadForm, EquiposForm
from .models import *
from ensayos.models import ListaEnsayos
from muestras.models import Muestras

# Create your views here.
def equipos (request):
    equipos= Equipos.objects.all().order_by()
    
    return render (request, "ensayos/equipos.html",{
        'equipos': equipos
        
    })
    
def nuevoEquipo (request):
    if request.method == "POST":
        form= EquiposForm(request.POST)
        
        if form.is_valid():
            form.save()
               
    else:
        form= EquiposForm()
    
    return render (request, "ensayos/nuevoEquipo.html",{
        'equipos': equipos,
        'form': EquiposForm,
        
    })

def humedad(request):
    if request.method == 'POST':
        form = HumedadForm(request.POST)
        print("hola")

        if form.is_valid():
            print(request.POST)
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
            if tiempoEnsayo != "":
                tiempoEnsayo= float(tiempoEnsayo)
                humedad.tiempoEnsayo=tiempoEnsayo
            
            #Sacamos la media del resultado
            resultado= 0
            
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
                
            resultado= round(resultado, 2)              
            #Guardamos los valores en la tabla resultados
            resultados= Resultados.objects.create(
                muestra= muestra,
                ensayo= ensayo,
                resultado= resultado,
                unidades= "%",
            )
            
            ############################################################################################
            #POSIBILIDAD DE ELIMINAR LOS ENSAYOS QUE HAYA DE HUM PARA DICHA MUESTRA ANTES DE GUADAR OTRO,
            #SI NO, SE VAN A REPETIR LOS ENSAYOS
            ############################################################################################

    else:
        form = HumedadForm()

    return render(request, 'ensayos/humedad.html', {'form': form})