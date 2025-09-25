from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from .forms import *
from django.contrib.auth.decorators import login_required


# Create your views here.
#Equipos
@login_required
def equipos (request):
    equipos= Equipos.objects.all().order_by()
    
    return render (request, "equipos/equipos.html",{
        'equipos': equipos
        
    })
    
#Alta de nuevos equipos
@login_required
def nuevoEquipo (request):
    if request.method == "POST":
        form= EquiposForm(request.POST)
        
        if form.is_valid():
            form.save()

            return redirect ("equipos")
        else:
            # Si el formulario es inválido, simplemente lo renderizamos con los errores
            print(form.errors)
            return render(request, "equipos/configurarEquipo.html", {
                'form': form,  # Aquí pasamos el form con errores
            })
               
    else:
        form= EquiposForm()
    
    return render (request, "equipos/configurarEquipo.html",{
        'form': EquiposForm,
    })

#Editar equipos
@login_required
def editarEquipo (request, id_equipo):
     
    equipo= get_object_or_404(Equipos, id=id_equipo)
    equiposAsociados = EquipoAsociado.objects.filter(equipoAsociado=equipo)
    print(equipoAsociado)

    if request.method =="POST":
        form = EquiposForm(request.POST, instance=equipo)

        if form.is_valid():
        
            form.save()

            return redirect("equipos")

    else:
        form = EquiposForm(instance=equipo)
    
    return render (request, "equipos/configurarEquipo.html",{
        'equipo': equipo,
        'form': form,
        'equiposAsociados': equiposAsociados
        
    })


#Eliminar equipo
@login_required
def eliminarEquipo(request, id_equipo):
    if request.method == "POST":
        equipo = get_object_or_404(Equipos, id=id_equipo)

        equipo.delete()
        return redirect('equipos')
    else:
        print("hubo un problema")
        return redirect('equipos')

    
@login_required
def equipoAsociado(request, id_equipoAsociado):
    equipoAsociado= get_object_or_404(Equipos, id= id_equipoAsociado)
    form= EquiposAsociadosForm()
    print(equipoAsociado)
    
    if request.method == "POST":
        form = EquiposAsociadosForm(request.POST)
        print("POST recibido:", request.POST)
        print("is_valid:", form.is_valid())  # Esto es lo raro
        print("Errores:", form.errors)
        
        if form.is_valid():
            obj = form.save(commit=False)
            obj.equipoAsociado = equipoAsociado
            obj.save()
            print("guardado")
            
            return redirect("editarEquipo", equipoAsociado.id )
        else:
            print("No valido")

        
    
    return render (request, 'equipos/equipoAsociado.html',{
        "equipoAsociado": equipoAsociado,
        "form": form
    })


@login_required
def eliminarEquipoAsociado(request, id_equipo):
    equipoAsociado= EquipoAsociado.objects.get(id= id_equipo)
    equipo= equipoAsociado.equipoAsociado

    equipoAsociado.delete()
    print("Borrado")

    return redirect("editarEquipo", equipo.id )
