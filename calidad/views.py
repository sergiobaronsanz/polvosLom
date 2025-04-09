from django.shortcuts import render, redirect, get_object_or_404
from .forms import *


# Create your views here.
#Equipos
def equipos (request):
    equipos= Equipos.objects.all().order_by()
    
    return render (request, "equipos/equipos.html",{
        'equipos': equipos
        
    })
    
#Alta de nuevos equipos
def nuevoEquipo (request):
    if request.method == "POST":
        form= EquiposForm(request.POST)
        
        if form.is_valid():
            form.save()

            return redirect ("equipos")
               
    else:
        form= EquiposForm()
    
    return render (request, "equipos/configurarEquipo.html",{
        'equipos': equipos,
        'form': EquiposForm,
        
    })

#Editar equipos
def editarEquipo (request, id_equipo):
     
    equipo= get_object_or_404(Equipos, id=id_equipo)

    if request.method =="POST":
        form = EquiposForm(request.POST, instance=equipo)

        if form.is_valid():
        
            form.save()

            return redirect("equipos")

    else:
        form = EquiposForm(instance=equipo)
    
    return render (request, "equipos/configurarEquipo.html",{
        'equipos': equipos,
        'form': form,
        
    })


#Eliminar equipo
def eliminarEquipo(request, id_equipo):
    if request.method == "POST":
        equipo = get_object_or_404(Equipos, id=id_equipo)

        equipo.delete()
        return redirect('equipos')
    else:
        print("hubo un problema")
        return redirect('equipos')

    