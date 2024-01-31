from django.shortcuts import render, get_list_or_404, get_object_or_404
from .forms import HumedadForm
from .models import ResultadosHumedad, Humedad
from ensayos.models import ListaEnsayos
from muestras.models import Muestras

# Create your views here.
def humedad(request):
    if request.method == 'POST':
        form = HumedadForm(request.POST)

        if form.is_valid():
            print(request.POST)
            muestra= get_object_or_404(Muestras, id= request.POST.get('muestra'))
            temperaturaAmbiente= request.POST.get('temperaturaAmbiente')
            humedad= request.POST.get('humedad')
            criterio= request.POST.get('criterio')
            tiempoEnsayo=request.POST.get('tiempoEnsayo')
            tDesecacion= request.POST.get('tDesecacion')
            desviacion= request.POST.get('desviacion')
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
            
            ensayo= get_object_or_404(ListaEnsayos, ensayo= "humedad")
            
            if float(desviacion) >= 0.15:
                humedad= Humedad(
                    muestra= muestra, 
                    ensayo= ensayo,
                    temperaturaAmbiente= temperaturaAmbiente,
                    humedad= humedad,
                    equipos= equipos*****
                )
                
            print(ensayo)
            

    else:
        form = HumedadForm()

    return render(request, 'ensayos/humedad.html', {'form': form})