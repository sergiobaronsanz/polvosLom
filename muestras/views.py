
from django.shortcuts import render, redirect
from muestras.forms import DescripcionMuestraForm, MuestrasForm
from .models import Muestras

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
    