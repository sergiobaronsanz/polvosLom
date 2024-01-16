
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from muestras.forms import DescripcionMuestraForm, MuestrasForm
from .models import Muestras, DescripcionMuestra
from ensayos.models import Resultados

# Create your views here.

"""def seleccionExpediente(request):
    if request.method == 'POST':
        form = MuestrasForm(request.POST)
        if form.is_valid():
            # Guardar el formulario si es válido
            form.save()
            return redirect("/muestras/descripcion")
    else:
        form = MuestrasForm()

    return render(request, 'seleccionExpediente.html', {'form': form})"""

def recepcionMuestra(request):
    if request.method == 'POST':
        form = DescripcionMuestraForm(request.POST, request.FILES)
        if form.is_valid():
            # Guardar el formulario si es válido
            form.save()
            
            #Actualizar el estado de la muestra
            id_muestra= request.POST['muestra']
            muestra= Muestras.objects.get(id= id_muestra)
            muestra.estado= "3"
            muestra.save()
            
            
    else:
        form = DescripcionMuestraForm()

    return render(request, 'recepcionMuestra.html', {'form': form})
    
    
def verMuestra(request, muestra_id):
    
    muestra= get_object_or_404(Muestras, id= muestra_id)
    
    #Sacamos la descripción de la muestra
    descripcion= get_object_or_404(DescripcionMuestra, muestra=muestra)   
    
    #Sacamos los resultados 
    resultados= get_list_or_404(Resultados, muestra= muestra)
    
    return render(request, 'verMuestra.html', {
        "muestra": muestra,
        "descripcion": descripcion,
        "resultados": resultados
    })