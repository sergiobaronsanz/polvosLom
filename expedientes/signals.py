from muestras.models import Muestras, ListaEnsayos, DescripcionMuestra
from ensayos.models import *
from expedientes.models import Expedientes
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, get_list_or_404



#Si recibimos muestra actualiazamos el estado
@receiver(post_save, sender=Muestras)
def actualizar_estado_expediente(sender, instance, created, **kwargs):
    #Comprobamos que todas las muestras estén listadas
    expediente = instance.expediente  # Obtén el expediente relacionado a la muestra
    muestras = Muestras.objects.filter(expediente= expediente)  # Obtén los estados de todas las muestras del expediente
    # Lógica para actualizar el estado del expediente basado en las muestras
    # Por ejemplo, si todas las muestras están terminadas, el expediente se marca como terminado
    if all(muestra.estado == '3' for muestra in muestras):
        expediente.estado = '3'  # Actualiza el estado del expediente a "Terminado"
        expediente.save()

#Creamos los ensayos si la lista de ensayo cambia
@receiver(m2m_changed, sender=Muestras.listaEnsayos.through)
def crear_ensayos(sender, instance, action, **kwargs):
    #Sacamos los ensayos asignados a la muestra
    ensayos=instance.listaEnsayos.all()      
    expediente= instance.expediente
    
    descripcionMuestra= DescripcionMuestra.objects.filter(muestra= instance)

    if action == "post_add":
         
        for ensayo in ensayos:
            if ensayo.ensayo == "Granulometria":
                if not Granulometria.objects.filter(muestra= instance).exists():
                    resultados= Granulometria.objects.create(
                        muestra= instance,
                        ensayo= ensayo,
                        unidad= "um",
                    )
                    if descripcionMuestra:
                        #Volvemos a poner la muestra y el expediente en estado de ensayando
                        instance.estado= "3"
                        instance.save()
                        expediente.estado= "3"
                        expediente.save()
                    else:
                        instance.estado= "1"
                        instance.save()
                        expediente.estado= "1"
                        expediente.save()
            
            if ensayo.ensayo == "TMIc":
                if not TMIc.objects.filter(muestra= instance).exists():
                    resultados= TMIc.objects.create(
                        muestra= instance,
                        ensayo= ensayo,
                        unidad= "ºC",
                    )
                    if descripcionMuestra:
                        #Volvemos a poner la muestra y el expediente en estado de ensayando
                        instance.estado= "3"
                        instance.save()
                        expediente.estado= "3"
                        expediente.save()
                    else:
                        instance.estado= "1"
                        instance.save()
                        expediente.estado= "1"
                        expediente.save()
                
            if ensayo.ensayo == "TMIn":
                if not TMIn.objects.filter(muestra= instance).exists():
                    resultados= TMIn.objects.create(
                        muestra= instance,
                        ensayo= ensayo,
                        unidad= "ºC",
                    )
                    if descripcionMuestra:
                        #Volvemos a poner la muestra y el expediente en estado de ensayando
                        instance.estado= "3"
                        instance.save()
                        expediente.estado= "3"
                        expediente.save()
                    else:
                        instance.estado= "1"
                        instance.save()
                        expediente.estado= "1"
                        expediente.save()

            if ensayo.ensayo == "LIE":
                if not LIE.objects.filter(muestra= instance).exists():
                    resultados= LIE.objects.create(
                        muestra= instance,
                        ensayo= ensayo,
                        unidad= "g/m3",
                    )
                    if descripcionMuestra:
                        #Volvemos a poner la muestra y el expediente en estado de ensayando
                        instance.estado= "3"
                        instance.save()
                        expediente.estado= "3"
                        expediente.save()
                    else:
                        instance.estado= "1"
                        instance.save()
                        expediente.estado= "1"
                        expediente.save()

            if ensayo.ensayo == "EMI":
                if not EMI.objects.filter(muestra= instance).exists():
                    resultados= EMI.objects.create(
                        muestra= instance,
                        ensayo= ensayo,
                        unidad= "mJ",
                    )
                    if descripcionMuestra:
                        #Volvemos a poner la muestra y el expediente en estado de ensayando
                        instance.estado= "3"
                        instance.save()
                        expediente.estado= "3"
                        expediente.save()
                    else:
                        instance.estado= "1"
                        instance.save()
                        expediente.estado= "1"
                        expediente.save()
            
            if ensayo.ensayo == "EMIsin":
                if not EMIsin.objects.filter(muestra= instance).exists():
                    resultados= EMIsin.objects.create(
                        muestra= instance,
                        ensayo= ensayo,
                        unidad= "mJ",
                    )
                    if descripcionMuestra:
                        #Volvemos a poner la muestra y el expediente en estado de ensayando
                        instance.estado= "3"
                        instance.save()
                        expediente.estado= "3"
                        expediente.save()
                    else:
                        instance.estado= "1"
                        instance.save()
                        expediente.estado= "1"
                        expediente.save()

            if ensayo.ensayo == "Pmax":
                if not Pmax.objects.filter(muestra= instance).exists():
                    resultados= Pmax.objects.create(
                        muestra= instance,
                        ensayo= ensayo,
                        unidadPmax= "g/m3",
                        unidadDpdt= "bar/s",
                    )
                    if descripcionMuestra:
                        #Volvemos a poner la muestra y el expediente en estado de ensayando
                        instance.estado= "3"
                        instance.save()
                        expediente.estado= "3"
                        expediente.save()
                    else:
                        instance.estado= "1"
                        instance.save()
                        expediente.estado= "1"
                        expediente.save()

            if ensayo.ensayo == "CLO":
                if not CLO.objects.filter(muestra= instance).exists():
                    resultados= CLO.objects.create(
                        muestra= instance,
                        ensayo= ensayo,
                        unidad= "%"
                    )
                    if descripcionMuestra:
                        #Volvemos a poner la muestra y el expediente en estado de ensayando
                        instance.estado= "3"
                        instance.save()
                        expediente.estado= "3"
                        expediente.save()
                    else:
                        instance.estado= "1"
                        instance.save()
                        expediente.estado= "1"
                        expediente.save()

            if ensayo.ensayo == "REC":
                if not REC.objects.filter(muestra= instance).exists():
                    resultados= REC.objects.create(
                        muestra= instance,
                        ensayo= ensayo,
                        unidad= "Mohm"
                    )
                    if descripcionMuestra:
                        #Volvemos a poner la muestra y el expediente en estado de ensayando
                        instance.estado= "3"
                        instance.save()
                        expediente.estado= "3"
                        expediente.save()
                    else:
                        instance.estado= "1"
                        instance.save()
                        expediente.estado= "1"
                        expediente.save()
            
            if ensayo.ensayo == "N1":
                if not N1.objects.filter(muestra= instance).exists():
                    resultados= N1.objects.create(
                        muestra= instance,
                        ensayo= ensayo,
                    )
                    if descripcionMuestra:
                        #Volvemos a poner la muestra y el expediente en estado de ensayando
                        instance.estado= "3"
                        instance.save()
                        expediente.estado= "3"
                        expediente.save()
                    else:
                        instance.estado= "1"
                        instance.save()
                        expediente.estado= "1"
                        expediente.save()

            if ensayo.ensayo == "N2":
                if not N2.objects.filter(muestra= instance).exists():
                    resultados= N2.objects.create(
                        muestra= instance,
                        ensayo= ensayo,
                    )
                    if descripcionMuestra:
                        #Volvemos a poner la muestra y el expediente en estado de ensayando
                        instance.estado= "3"
                        instance.save()
                        expediente.estado= "3"
                        expediente.save()
                    else:
                        instance.estado= "1"
                        instance.save()
                        expediente.estado= "1"
                        expediente.save()

            if ensayo.ensayo == "N4":
                if not N4.objects.filter(muestra= instance).exists():
                    resultados= N4.objects.create(
                        muestra= instance,
                        ensayo= ensayo,
                    )
                    if descripcionMuestra:
                        #Volvemos a poner la muestra y el expediente en estado de ensayando
                        instance.estado= "3"
                        instance.save()
                        expediente.estado= "3"
                        expediente.save()
                    else:
                        instance.estado= "1"
                        instance.save()
                        expediente.estado= "1"
                        expediente.save()

            if ensayo.ensayo == "O1":
                if not O1.objects.filter(muestra= instance).exists():
                    resultados= O1.objects.create(
                        muestra= instance,
                        ensayo= ensayo,
                    )
                    if descripcionMuestra:
                        #Volvemos a poner la muestra y el expediente en estado de ensayando
                        instance.estado= "3"
                        instance.save()
                        expediente.estado= "3"
                        expediente.save()
                    else:
                        instance.estado= "1"
                        instance.save()
                        expediente.estado= "1"
                        expediente.save()

            if ensayo.ensayo == "Tratamiento":
                if not Tratamiento.objects.filter(muestra= instance).exists():
                    resultados= Tratamiento.objects.create(
                        muestra= instance,
                        ensayo= ensayo,
                    )
                    if descripcionMuestra:
                        #Volvemos a poner la muestra y el expediente en estado de ensayando
                        instance.estado= "3"
                        instance.save()
                        expediente.estado= "3"
                        expediente.save()
                    else:
                        instance.estado= "1"
                        instance.save()
                        expediente.estado= "1"
                        expediente.save()
                
        porcentaje= porcentajeExpediente(expediente=expediente)
        expediente.porcentaje= porcentaje
        expediente.save()   

    if action == "post_remove":
        print("borrar")
        #Borramos el archivo creado para ello creamos una lista solo con el nombre de los ensayos y en minnúscula
        listaEnsayosnueva= []
        for ensayo in ensayos:
            listaEnsayosnueva.append(ensayo.ensayo.lower())
        
        if not "humedad" in listaEnsayosnueva:
            ensayoObjeto= Humedad.objects.filter(muestra= instance)
            if ensayoObjeto.exists():
                ensayoObjeto.delete()

        if not "granulometria" in listaEnsayosnueva:
            ensayoObjeto= Granulometria.objects.filter(muestra= instance)
            if ensayoObjeto.exists():
                ensayoObjeto.delete()

        if not "tmic" in listaEnsayosnueva:
            ensayoObjeto= TMIc.objects.filter(muestra= instance)
            if ensayoObjeto.exists():
                ensayoObjeto.delete()
        
        if not "tmin" in listaEnsayosnueva:
            ensayoObjeto= TMIn.objects.filter(muestra= instance)
            if ensayoObjeto.exists():
                ensayoObjeto.delete()

        if not "lie" in listaEnsayosnueva:
            ensayoObjeto= LIE.objects.filter(muestra= instance)
            if ensayoObjeto.exists():
                ensayoObjeto.delete()

        if not "emi" in listaEnsayosnueva:
            ensayoObjeto= EMI.objects.filter(muestra= instance)
            if ensayoObjeto.exists():
                ensayoObjeto.delete()

        if not "emisin" in listaEnsayosnueva:
            ensayoObjeto= EMIsin.objects.filter(muestra= instance)
            if ensayoObjeto.exists():
                ensayoObjeto.delete()

        if not "pmax" in listaEnsayosnueva:
            ensayoObjeto= Pmax.objects.filter(muestra= instance)
            if ensayoObjeto.exists():
                ensayoObjeto.delete()

        if not "clo" in listaEnsayosnueva:
            ensayoObjeto= CLO.objects.filter(muestra= instance)
            if ensayoObjeto.exists():
                ensayoObjeto.delete()
        
        if not "rec" in listaEnsayosnueva:
            ensayoObjeto= REC.objects.filter(muestra= instance)
            if ensayoObjeto.exists():
                ensayoObjeto.delete()

        if not "n1" in listaEnsayosnueva:
            ensayoObjeto= N1.objects.filter(muestra= instance)
            if ensayoObjeto.exists():
                ensayoObjeto.delete()
        
        if not "n2" in listaEnsayosnueva:
            ensayoObjeto= N2.objects.filter(muestra= instance)
            if ensayoObjeto.exists():
                ensayoObjeto.delete()

        if not "n4" in listaEnsayosnueva:
            ensayoObjeto= N4.objects.filter(muestra= instance)
            if ensayoObjeto.exists():
                ensayoObjeto.delete()

        if not "o1" in listaEnsayosnueva:
            ensayoObjeto= O1.objects.filter(muestra= instance)
            if ensayoObjeto.exists():
                ensayoObjeto.delete()

        if not "tratamiento" in listaEnsayosnueva:
            ensayoObjeto= Tratamiento.objects.filter(muestra= instance)
            if ensayoObjeto.exists():
                ensayoObjeto.delete()
        
        chequeo_expedientes_terminados(muestra=instance)  
        porcentaje= porcentajeExpediente(expediente=expediente)
        expediente.porcentaje= porcentaje
        expediente.save()   

#Cambio estado expediente, para pasar la muestra de estado de ensayando a revisión
def chequeo_expedientes_terminados(ensayo= None, muestra= None ):
    if ensayo:
        #Sacamos expediente
        expediente= ensayo.muestra.expediente
        #Vemos todas las muestras que tiene el expediente
        muestras= get_list_or_404(Muestras, expediente= expediente)
    if muestra:
        expediente= muestra.expediente
        muestras= get_list_or_404(Muestras, expediente= expediente)

    #Comprobamos que todos los ensayos hayan terminado y marcamos la muestra para revisión
    
    for muestra in muestras:
        estadoListadoEnsayos=[]
        ensayos_asignados = muestra.listaEnsayos.all()
        nombres = [e.ensayo.lower() for e in ensayos_asignados]
        print(ensayos_asignados)
        print(muestra)

        if "humedad" in nombres:
            ensayo = Humedad.objects.filter(muestra=muestra).first()
            if ensayo and ensayo.resultado:
                estadoListadoEnsayos.append(True)
            else:
                estadoListadoEnsayos.append(False)

        if "granulometria" in nombres:
            ensayo = Granulometria.objects.filter(muestra=muestra).first()
            if ensayo and ensayo.resultado:
                estadoListadoEnsayos.append(True)
            else:
                estadoListadoEnsayos.append(False)

        if "tmic" in nombres:
            ensayo = TMIc.objects.filter(muestra=muestra).first()
            if ensayo and ensayo.resultado:
                estadoListadoEnsayos.append(True)
            else:
                estadoListadoEnsayos.append(False)

        if "tmin" in nombres:
            ensayo = TMIn.objects.filter(muestra=muestra).first()
            if ensayo and ensayo.resultado:
                estadoListadoEnsayos.append(True)
            else:
                estadoListadoEnsayos.append(False)

        if "lie" in nombres:
            ensayo = LIE.objects.filter(muestra=muestra).first()
            if ensayo and ensayo.resultado:
                estadoListadoEnsayos.append(True)
            else:
                estadoListadoEnsayos.append(False)
        
        if "emi" in nombres:
            ensayo = EMI.objects.filter(muestra=muestra).first()
            if ensayo and ensayo.resultado:
                estadoListadoEnsayos.append(True)
            else:
                estadoListadoEnsayos.append(False)

        if "pmax" in nombres:
            ensayo = Pmax.objects.filter(muestra=muestra).first()
            if ensayo and ensayo.pmax and ensayo.dpdt and ensayo.kmax:
                estadoListadoEnsayos.append(True)
            else:
                estadoListadoEnsayos.append(False)

        if "clo" in nombres:
            ensayo = CLO.objects.filter(muestra=muestra).first()
            if ensayo and ensayo.resultado:
                estadoListadoEnsayos.append(True)
            else:
                estadoListadoEnsayos.append(False)

        if "rec" in nombres:
            ensayo = REC.objects.filter(muestra=muestra).first()
            if ensayo and ensayo.resultado:
                estadoListadoEnsayos.append(True)
            else:
                estadoListadoEnsayos.append(False)

        if "n1" in nombres:
            ensayo = N1.objects.filter(muestra=muestra).first()
            if ensayo and ensayo.resultado:
                estadoListadoEnsayos.append(True)
            else:
                estadoListadoEnsayos.append(False)

        if "n2" in nombres:
            ensayo = N2.objects.filter(muestra=muestra).first()
            if ensayo and ensayo.resultado:
                estadoListadoEnsayos.append(True)
            else:
                estadoListadoEnsayos.append(False)

        if "n4" in nombres:
            ensayo = N4.objects.filter(muestra=muestra).first()
            if ensayo and ensayo.resultado:
                estadoListadoEnsayos.append(True)
            else:
                estadoListadoEnsayos.append(False)

        if "o1" in nombres:
            ensayo = O1.objects.filter(muestra=muestra).first()
            if ensayo and ensayo.resultado:
                estadoListadoEnsayos.append(True)
            else:
                estadoListadoEnsayos.append(False)
        
        if "tratamiento" in nombres:
            ensayo = Tratamiento.objects.filter(muestra=muestra).first()
            if ensayo and (ensayo.molido or ensayo.tamizado or ensayo.secado):
                estadoListadoEnsayos.append(True)
            else:
                estadoListadoEnsayos.append(False)

        
        if "emisin" in nombres:
            ensayo = EMI.objects.filter(muestra=muestra).first()
            if ensayo and ensayo.resultado:
                estadoListadoEnsayos.append(True)
            else:
                estadoListadoEnsayos.append(False)

        if all(estadoListadoEnsayos):
            muestra.estado = "4"
            muestra.save()
        print(f"La lista de estado es: {estadoListadoEnsayos}")

    estadoListadoMuestras=[]
    for muestra in muestras:
        if muestra.estado == "4":
            estadoListadoMuestras.append(True)
        else:
            estadoListadoMuestras.append(False)
            
    if all(estadoListadoMuestras):
        expediente.estado= "4"
        expediente.save()
    else:
        expediente.estado= "3"
        expediente.save()
    
    
    print(f"Las muestras son: {muestras}")

#Ver porcentaje expediente
def porcentajeExpediente(ensayo= None, expediente= None):
    
    if ensayo:
        expediente= ensayo.muestra.expediente
    if expediente:
        expediente= expediente

    

    muestras= Muestras.objects.filter(expediente= expediente)

    #Sumamos la totalidad de las horas y las de los ensyayos terminados(los que tienen resultado)
    # Inicializar las listas de horas
    
    horasTotales = []
    horasTerminadas = []
    for muestra in muestras:
        #Sacamos la lista de ensayos
        listaEnsayos= muestra.listaEnsayos.all()
        # Iterar sobre la lista de ensayos
        for ensayo in listaEnsayos:    
            # Verificar si el ensayo es "humedad"
            if "humedad" in ensayo.ensayo.lower():
                humedad = Humedad.objects.filter(muestra=muestra).first()
                if humedad:
                    # Añadir las horas a la lista de horasTotales
                    horasTotales.append(humedad.horasEnsayo)
                    # Si el ensayo tiene resultado, añadir las horas a la lista de horasTerminadas
                    if humedad.resultado:
                        horasTerminadas.append(humedad.horasEnsayo)

            # Verificar si el ensayo es "granulometria"
            if "granulometria" in ensayo.ensayo.lower():
                granulometria = Granulometria.objects.filter(muestra=muestra).first()
                if granulometria:
                    horasTotales.append(granulometria.horasEnsayo)
                    if granulometria.resultado:
                        horasTerminadas.append(granulometria.horasEnsayo)

            # Verificar si el ensayo es "tmic"
            if "tmic" in ensayo.ensayo.lower():
                tmic = TMIc.objects.filter(muestra=muestra).first()
                if tmic:
                    horasTotales.append(tmic.horasEnsayo)
                    if tmic.resultado:
                        horasTerminadas.append(tmic.horasEnsayo)

            # Verificar si el ensayo es "tmin"
            if "tmin" in ensayo.ensayo.lower():
                tmin = TMIn.objects.filter(muestra=muestra).first()
                if tmin:
                    horasTotales.append(tmin.horasEnsayo)
                    if tmin.resultado:
                        horasTerminadas.append(tmin.horasEnsayo)

            # Verificar si el ensayo es "lie"
            if "lie" in ensayo.ensayo.lower():
                lie = LIE.objects.filter(muestra=muestra).first()
                if lie:
                    horasTotales.append(lie.horasEnsayo)
                    if lie.resultado:
                        horasTerminadas.append(lie.horasEnsayo)

            # Verificar si el ensayo es "emi"
            if "emi" in ensayo.ensayo.lower():
                emi = EMI.objects.filter(muestra=muestra).first()
                if emi:
                    horasTotales.append(emi.horasEnsayo)
                    if emi.resultado:
                        horasTerminadas.append(emi.horasEnsayo)

            # Verificar si el ensayo es "pmax"
            if "pmax" in ensayo.ensayo.lower():
                pmax = Pmax.objects.filter(muestra=muestra).first()
                if pmax:
                    horasTotales.append(pmax.horasEnsayo)
                    if pmax.pmax and pmax.dpdt and pmax.kmax:
                        horasTerminadas.append(pmax.horasEnsayo)

            # Verificar si el ensayo es "clo"
            if "clo" in ensayo.ensayo.lower():
                clo = CLO.objects.filter(muestra=muestra).first()
                if clo:
                    horasTotales.append(clo.horasEnsayo)
                    if clo.resultado:
                        horasTerminadas.append(clo.horasEnsayo)

            # Verificar si el ensayo es "rec"
            if "rec" in ensayo.ensayo.lower():
                rec = REC.objects.filter(muestra=muestra).first()
                if rec:
                    horasTotales.append(rec.horasEnsayo)
                    if rec.resultado:
                        horasTerminadas.append(rec.horasEnsayo)

            # Verificar si el ensayo es "n1"
            if "n1" in ensayo.ensayo.lower():
                n1 = N1.objects.filter(muestra=muestra).first()
                if n1:
                    horasTotales.append(n1.horasEnsayo)
                    if n1.resultado:
                        horasTerminadas.append(n1.horasEnsayo)

            # Verificar si el ensayo es "n2"
            if "n2" in ensayo.ensayo.lower():
                n2 = N2.objects.filter(muestra=muestra).first()
                if n2:
                    horasTotales.append(n2.horasEnsayo)
                    if n2.resultado:
                        horasTerminadas.append(n2.horasEnsayo)

            # Verificar si el ensayo es "n4"
            if "n4" in ensayo.ensayo.lower():
                n4 = N4.objects.filter(muestra=muestra).first()
                if n4:
                    horasTotales.append(n4.horasEnsayo)
                    if n4.resultado:
                        horasTerminadas.append(n4.horasEnsayo)

            # Verificar si el ensayo es "o1"
            if "o1" in ensayo.ensayo.lower():
                o1 = O1.objects.filter(muestra=muestra).first()
                if o1:
                    horasTotales.append(o1.horasEnsayo)
                    if o1.resultado:
                        horasTerminadas.append(o1.horasEnsayo)

            # Verificar si el ensayo es "tratamiento"
            if "tratamiento" in ensayo.ensayo.lower():
                tratamiento = Tratamiento.objects.filter(muestra=muestra).first()
                if tratamiento:
                    horasTotales.append(tratamiento.horasEnsayo)
                    if tratamiento.tamizado or tratamiento.molido or tratamiento.secado:
                        horasTerminadas.append(tratamiento.horasEnsayo)

            # Verificar si el ensayo es "emisin"
            if "emisin" in ensayo.ensayo.lower():
                emisin = EMI.objects.filter(muestra=muestra).first()
                if emisin:
                    horasTotales.append(emisin.horasEnsayo)
                    if emisin.resultado:
                        horasTerminadas.append(emisin.horasEnsayo)

        # Sumar todas las horas de los ensayos seleccionados
        totalHorasMuestra = sum(horasTotales)

        # Sumar solo las horas de los ensayos terminados
        totalHorasTerminadasMuestra = sum(horasTerminadas)

    horasTotales.append(totalHorasMuestra)
    horasTerminadas.append(totalHorasTerminadasMuestra)

    resultado= (sum(horasTerminadas)/sum(horasTotales))*100
        

    return resultado

    
@receiver(post_save, sender= Humedad)
def cambio_humedad(sender, instance, created, **kwargs):
    chequeo_expedientes_terminados(ensayo=instance)
    porcentaje= porcentajeExpediente(ensayo=instance)
    
    muestra= instance.muestra
    expediente= muestra.expediente
    expediente.porcentaje= porcentaje
    expediente.save()

@receiver(post_save, sender= Granulometria)
def cambio_granulometria(sender, instance, created, **kwargs):
    chequeo_expedientes_terminados(ensayo=instance)
    porcentaje= porcentajeExpediente(ensayo=instance)
    
    muestra= instance.muestra
    expediente= muestra.expediente
    expediente.porcentaje= porcentaje
    expediente.save()


@receiver(post_save, sender= TMIc)
def cambio_tmic(sender, instance, created, **kwargs):
    chequeo_expedientes_terminados(ensayo=instance)
    porcentaje= porcentajeExpediente(ensayo=instance)
    
    muestra= instance.muestra
    expediente= muestra.expediente
    expediente.porcentaje= porcentaje
    expediente.save()

@receiver(post_save, sender= TMIn)
def cambio_tmin(sender, instance, created, **kwargs):
    chequeo_expedientes_terminados(ensayo=instance)
    porcentaje= porcentajeExpediente(ensayo=instance)
    
    muestra= instance.muestra
    expediente= muestra.expediente
    expediente.porcentaje= porcentaje
    expediente.save()

@receiver(post_save, sender= LIE)
def cambio_lie(sender, instance, created, **kwargs):
    chequeo_expedientes_terminados(ensayo=instance)
    porcentaje= porcentajeExpediente(ensayo=instance)
    
    muestra= instance.muestra
    expediente= muestra.expediente
    expediente.porcentaje= porcentaje
    expediente.save()

@receiver(post_save, sender= EMI)
def cambio_emi(sender, instance, created, **kwargs):
    chequeo_expedientes_terminados(ensayo=instance)
    porcentaje= porcentajeExpediente(ensayo=instance)
    
    muestra= instance.muestra
    expediente= muestra.expediente
    expediente.porcentaje= porcentaje
    expediente.save()

@receiver(post_save, sender= Pmax)
def cambio_pmax(sender, instance, created, **kwargs):
    chequeo_expedientes_terminados(ensayo=instance)
    porcentaje= porcentajeExpediente(ensayo=instance)
    
    muestra= instance.muestra
    expediente= muestra.expediente
    expediente.porcentaje= porcentaje
    expediente.save()


@receiver(post_save, sender= CLO)
def cambio_clo(sender, instance, created, **kwargs):
    chequeo_expedientes_terminados(ensayo=instance)
    porcentaje= porcentajeExpediente(ensayo=instance)
    
    muestra= instance.muestra
    expediente= muestra.expediente
    expediente.porcentaje= porcentaje
    expediente.save()

@receiver(post_save, sender= REC)
def cambio_rec(sender, instance, created, **kwargs):
    chequeo_expedientes_terminados(ensayo=instance)
    porcentaje= porcentajeExpediente(ensayo=instance)
    
    muestra= instance.muestra
    expediente= muestra.expediente
    expediente.porcentaje= porcentaje
    expediente.save()

@receiver(post_save, sender= N1)
def cambio_n1(sender, instance, created, **kwargs):
    chequeo_expedientes_terminados(ensayo=instance)
    porcentaje= porcentajeExpediente(ensayo=instance)
    
    muestra= instance.muestra
    expediente= muestra.expediente
    expediente.porcentaje= porcentaje
    expediente.save()

@receiver(post_save, sender= N2)
def cambio_n2(sender, instance, created, **kwargs):
    chequeo_expedientes_terminados(ensayo=instance)
    porcentaje= porcentajeExpediente(ensayo=instance)
    
    muestra= instance.muestra
    expediente= muestra.expediente
    expediente.porcentaje= porcentaje
    expediente.save()

@receiver(post_save, sender= N4)
def cambio_n4(sender, instance, created, **kwargs):
    chequeo_expedientes_terminados(ensayo=instance)
    porcentaje= porcentajeExpediente(ensayo=instance)
    
    muestra= instance.muestra
    expediente= muestra.expediente
    expediente.porcentaje= porcentaje
    expediente.save()

@receiver(post_save, sender= O1)
def cambio_o1(sender, instance, created, **kwargs):
    chequeo_expedientes_terminados(ensayo=instance)
    porcentaje= porcentajeExpediente(ensayo=instance)
    
    muestra= instance.muestra
    expediente= muestra.expediente
    expediente.porcentaje= porcentaje
    expediente.save()

@receiver(post_save, sender= Tratamiento)
def cambio_tratamiento(sender, instance, created, **kwargs):
    chequeo_expedientes_terminados(ensayo=instance)
    porcentaje= porcentajeExpediente(ensayo=instance)
    
    muestra= instance.muestra
    expediente= muestra.expediente
    expediente.porcentaje= porcentaje
    expediente.save()

@receiver(post_save, sender= EMIsin)
def cambio_emisin(sender, instance, created, **kwargs):
    chequeo_expedientes_terminados(ensayo=instance)
    porcentaje= porcentajeExpediente(ensayo=instance)
    
    muestra= instance.muestra
    expediente= muestra.expediente
    expediente.porcentaje= porcentaje
    expediente.save()
    


"""   
#Creamos los ensayos cuando se crean las muestras
@receiver(m2m_changed, sender=Muestras.listaEnsayos.through)
def crear_ensayos(sender, instance, action, **kwargs):    
     
    if action:
    print(instance)
    ensayos_elegidos = [
        'Humedad', 'Granulometria', 'TMIc',
        'TMIn', 'LIE', 'EMI', 'Pmax', 'CLO',
        'N1', 'N2','N4', 'O1','REC']  # Lista con los nombres de los tipos de ensayos

    lista_ensayos= instance.listaEnsayos.all()
    print(lista_ensayos)
    
    
    
    
    for tipo_ensayo_nombre in ensayos_elegidos:
        print(tipo_ensayo_nombre)
        print(instance)
        try:
            pass
        except ListaEnsayos.DoesNotExist:
            print(f"Tipo de ensayo '{tipo_ensayo_nombre}' no encontrado. No se creará.")S
        
        

        # Crear el ensayo específico según el tipo
        ensayo_model = globals()[tipo_ensayo_nombre]
        ensayo_model.objects.create(muestra=instance)
        ensayo_model.save()
        print("Exito, ensayo guardado")"""

            # Puedes realizar más ajustes aquí según tus necesidades

