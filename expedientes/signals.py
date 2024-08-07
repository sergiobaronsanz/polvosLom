from muestras.models import Muestras, ListaEnsayos
from ensayos.models import *
from expedientes.models import Expedientes
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

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


@receiver(m2m_changed, sender=Muestras.listaEnsayos.through)
def crear_ensayos(sender, instance, action, **kwargs):
    if action == "post_add":
        #Sacamos los ensayos asignados a la muestra
        ensayos=instance.listaEnsayos.all()
        
        #Hacemos los grupos de la unidades
        lista_temperatura= ["TMIc", "TMIn"]
        lista_humedades= ["Humedad"]
        lista_granulo= ["Granulometria"]
        
        for ensayo in ensayos:
            if ensayo.ensayo in lista_humedades:
                resultados= Humedad.objects.create(
                    muestra= instance,
                    ensayo= ensayo,
                    unidad= "%",
                )

            if ensayo.ensayo in lista_granulo:
                resultados= Granulometria.objects.create(
                    muestra= instance,
                    ensayo= ensayo,
                    unidad= "um",
                )
            
            if ensayo.ensayo in lista_temperatura:
                if ensayo.ensayo == "TMIc":
                    resultados= TMIc.objects.create(
                        muestra= instance,
                        ensayo= ensayo,
                        unidad= "ºC",
                    )
                
            if ensayo.ensayo in lista_temperatura:
                if ensayo.ensayo == "TMIn":
                    resultados= TMIn.objects.create(
                        muestra= instance,
                        ensayo= ensayo,
                        unidad= "ºC",
                    )
                
        """
           if ensayo.ensayo in lista_temperatura:
                resultados= Resultados.objects.create(
                    muestra= instance,
                    ensayo= ensayo,
                    unidades= "ºC",
                )
            if ensayo.ensayo in lista_granulo:
                resultados= Resultados.objects.create(
                    muestra= instance,
                    ensayo= ensayo,
                    unidades= "um",
                )"""
        print("creado")
            




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

