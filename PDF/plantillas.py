from fpdf import FPDF
from ensayos.models import *
from muestras.models import *
import os
import math

class PlantillasEnsayo():
    def __init__(self, muestra):
        self.muestra= Muestras.objects.get(id= muestra)
        self.descripcion= DescripcionMuestra.objects.get(muestra=muestra)
        self.identificacion= f"{self.muestra.empresa.abreviatura} - {self.muestra.id_muestra}"
        self.rutaAbsoluta = os.path.dirname(__file__)


    def recepcion(self):
        fecha= self.descripcion.fecha_recepcion
        empresa= self.muestra.empresa
        expediente= self.muestra.expediente

        self.pdf = FPDF(orientation = 'P', unit= 'mm', format = 'A4')
        self.pdf.add_page()

        #IMAGEN
        image_path = os.path.join(self.rutaAbsoluta, 'Imagenes', 'LOGO.png')
        self.pdf.image(image_path, x=8, y=8, w=30, h=30, link="http://www.lom.upm.es", type='PNG')

        #CABECERA
        self.pdf.set_font('Arial', '', 20)
        self.pdf.multi_cell(w=195, h= 30,border= 0, txt="Parte de recepción de muestras", align= "C", fill = 0)

        
        #DATOS GENERALES
        self.pdf.set_font('Arial', '', 12)

        
        self.pdf.cell(w=95, h= 12,border= "LRT", txt=f"Remitente: {empresa.empresa}", align= "L", fill = 0)
        self.pdf.multi_cell(w=95, h= 12,border= "LRT", txt=f"Expediente: {expediente.expediente}", align= "L", fill = 0)

        self.pdf.cell(w=95, h= 12,border= "LR", txt=f"Procedencia: {self.descripcion.procedencia}", align= "L", fill = 0)
        self.pdf.multi_cell(w=95, h= 12,border= "LR", txt=f"Recibida por: *cambiar*", align= "L", fill = 0)

        self.pdf.cell(w=95, h= 12,border= "LR", txt= f"¿Se adjunta documentación? {self.descripcion.get_documentacion_display()}", align= "L", fill = 0)
        self.pdf.multi_cell(w=95, h= 12,border= "LR", txt=f"Etiquetado: {self.descripcion.get_etiquetado_display()}", align= "L", fill = 0)

        self.pdf.cell(w=95, h= 12,border= "LRB", txt=f"Fecha recepción: {fecha}", align= "L", fill = 0)
        self.pdf.multi_cell(w=95, h= 12,border= "LRB", txt=f"Identificación LOM: {empresa.abreviatura}-{self.muestra.id_muestra}", align= "L", fill = 0)
        self.pdf.multi_cell(w=95, h= 12,border= 0, align= "L", fill = 0)


        #ESTADO ENVÍO
        self.pdf.set_font('Arial', 'B', 12)
        self.pdf.cell(w=190, h= 12,border= "LRT", align= "C",txt=f"ESTADO ENVÍO")
        self.pdf.multi_cell(w=5, h= 12,border= "", fill = 0)

        self.pdf.set_font('Arial', '', 12)
        
        self.pdf.cell(w=190, h= 12,border= "LR", align= "L", txt=f"Envoltura exterior: {self.descripcion.envolturaExt}")
        self.pdf.multi_cell(w=5, h= 12,border= "", fill = 0)

        
        self.pdf.cell(w=190, h= 12,border= "LR", align= "L", txt=f"Envoltura interior: {self.descripcion.envolturaInt}")
        self.pdf.multi_cell(w=5, h= 12,border= "", fill = 0)

        
        self.pdf.cell(w=190, h= 12,border= "LR", align= "L", txt=f"Peso: {self.descripcion.peso} kg")
        self.pdf.multi_cell(w=5, h= 12,border= "", fill = 0)

        
        self.pdf.cell(w=190, h= 12,border= "LRB", align= "L", txt=f"Peso: {self.descripcion.estadoEnvio}")
        self.pdf.multi_cell(w=5, h= 12,border= "", fill = 0)

        #CARACTERISTICAS MUESTRA
        self.pdf.set_font('Arial', 'B', 12)
        
        self.pdf.cell(w=190, h= 12,border= "LR", align= "C",txt=f"CARACTERÍSTICAS MUESTRA")
        self.pdf.multi_cell(w=5, h= 12,border= "", fill = 0)

        self.pdf.set_font('Arial', '', 12)
        
        self.pdf.cell(w=190, h= 12,border= "LR", align= "L", txt=f"Aspecto general: {self.descripcion.aspectoMuestra}")
        self.pdf.multi_cell(w=5, h= 12,border= "", fill = 0)

        self.pdf.set_font('Arial', '', 12)
        
        self.pdf.cell(w=190, h= 12,border= "LR", align= "L", txt=f"Color, brillo: {self.descripcion.color}, {self.descripcion.brillo}")
        self.pdf.multi_cell(w=5, h= 12,border= "", fill = 0)

        self.pdf.set_font('Arial', '', 12)
        
        self.pdf.cell(w=190, h= 12,border= "LRB", align= "L", txt=f"Tamaño, homogeneidad: {self.descripcion.tamano}, {self.descripcion.homogeneidad}")
        self.pdf.multi_cell(w=5, h= 12,border= "", fill = 0)


        #OBSERVACIONES
        self.pdf.set_font('Arial', 'B', 12)
        
        self.pdf.cell(w=190, h= 12,border= "LR", align= "C",txt=f"OBSERVACIONES")
        self.pdf.multi_cell(w=5, h= 12,border= "", fill = 0)

        self.pdf.set_font('Arial', '', 12)
        
        self.pdf.multi_cell(w=190, h= 12,border= "LR", align= "L", txt=f"Observación: {self.descripcion.observacion}")

        self.pdf.set_font('Arial', '', 12)
        
        self.pdf.cell(w=190, h= 12,border= "LRB", align= "L", txt=f"La muestra se ensaya: {self.descripcion.formaEnsayo}")
        self.pdf.multi_cell(w=5, h= 12,border= "", fill = 0)


        self.pdf.multi_cell(w=5, h= 12,border= "", fill = 0)

        #Firma
        self.pdf.set_font('Arial', '', 14) 
        self.pdf.cell(w=95, h= 8,border= 1, txt= f"Conforme:",
                align= "J", fill = 0)
        self.pdf.multi_cell(w=95, h= 8,border= 1, txt= f"Realizado: {self.descripcion.usuario.firmas.firma}",###
                align= "J", fill = 0)
        
        
        # Agregar más contenido dinámico aquí...
        return self.pdf.output(dest='S').encode('latin1')  # Devuelve bytes 
    

    def tmic(self):
        ensayo= TMIc.objects.get(muestra= self.muestra)
        equipos=ensayo.equipos.all()
        resultados= ResultadosTMIc.objects.filter(ensayo= ensayo).order_by("id")
        ensayoForma= self.descripcion.get_formaEnsayo_display()
        fechaInicio= ensayo.fechaInicio
        fechaFin= ensayo.fechaFin

        self.pdf = FPDF(orientation = 'P', unit= 'mm', format = 'A4')
        self.pdf.add_page()

        #TEXTO 
        self.pdf.set_font('Arial', '', 12)
        #IMAGEN
        image_path = os.path.join(self.rutaAbsoluta, 'Imagenes', 'LOGO.png')
        self.pdf.image(image_path, x=8, y=8, w=30, h=30, link="http://www.lom.upm.es", type='PNG')
        #Celdas Cabecera
        self.pdf.cell(w=35, h= 12,border= 0,
                align= "C", fill = 0)
        self.pdf.set_font('Arial', '', 11)
        self.pdf.cell(w= 100, h= 12, txt = f'{ensayo.ensayo.ensayo} ({ensayo.ensayo.normativa})', border= 1, 
                align= "C", fill = 0)
        self.pdf.set_font('Arial', '', 12)
        if fechaInicio!= fechaFin:
            self.pdf.multi_cell(w=0, h= 12, txt = f"Fecha Inicio: {fechaInicio.strftime('%d/%m/%Y')}", border= "RT", 
                    align= "L", fill = 0)
        else:
            self.pdf.multi_cell(w=0, h= 12, txt = "Fecha:", border= "RT", 
                align= "L", fill = 0)

        self.pdf.cell(w=35, h= 12,border= 0,
                align= "C", fill = 0)
        self.pdf.cell(w=100, h= 12, txt = f'Nº Expediente: {ensayo.muestra.expediente.expediente}', border= "LRB", 
                align= "C", fill = 0)
        if fechaInicio == fechaFin:
            self.pdf.multi_cell(w=0, h= 12, txt = fechaInicio.strftime("%d/%m/%Y"), border= "RB", 
                    align= "C", fill = 0)
        else:
              self.pdf.multi_cell(w=0, h= 12, txt = f'Fecha fin: {fechaFin.strftime("%d/%m/%Y")} ', border= "RB", 
                    align= "L", fill = 0)

        #Celda I/D muestra
        self.pdf.multi_cell(w=0, h= 5,border= 0,
                align= "C", fill = 0)
        self.pdf.cell(w=130, h= 8,border= 0, txt= f"Material: {self.descripcion.id_fabricante}",
                align= "J", fill = 0)
        self.pdf.multi_cell(w=60, h= 8,border= 0, txt= f"Identificación: {self.identificacion}",
                align= "J", fill = 0)

        #Celda Tratamiento de muestras  
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.cell(w=65, h= 8,border= "LT", txt= "MUESTRA DE POLVO",
                align= "J", fill = 0)

        self.pdf.set_font('Arial', '', 12)    
        self.pdf.multi_cell(w=125, h= 8,border= "TR", txt= f"La muestra se ensaya {ensayoForma}",
                align= "J", fill = 0)


        #Celda Condiciones ambientales  
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LRT", txt= "CONDICIONES AMBIENTALES",
                align= "J", fill = 0)

        self.pdf.set_font('Arial', '', 12)    
        self.pdf.cell(w=60, h= 8,border= "L", txt= f"Temperatura: {ensayo.temperaturaAmbiente} ºC",
                align= "C", fill = 0)

        self.pdf.cell(w=70, h= 8,border= "", txt= f"Humedad: {ensayo.humedad} %",
                align= "C", fill = 0)
        
        self.pdf.multi_cell(w=60, h= 8,border= "R", txt= f"Presión: {ensayo.presion} mBar",
                align= "C", fill = 0)


        #Celda Equipos
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LRT", txt= "EQUIPOS DE ENSAYO",
                align= "J", fill = 0)
        self.pdf.set_font('Arial', '', 12)
        self.pdf.multi_cell(w=190, h= 8,border= "LBR", txt = "Equipos: " + " | ".join(equipo.codigo for equipo in equipos),###
                align= "J", fill = 0)



        #Celda Procedimiento
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= "PROCEDIMIENTO",
                align= "J", fill = 0)
        #Leyenda superior
        self.pdf.cell(w=5, h= 8,border= "L", fill = 0)    
        self.pdf.set_font('Arial', '', 12)
        self.pdf.cell(w=60, h= 8,border= "LT", txt= "Incrementos Tª 10 K", fill = 0)
        self.pdf.cell(w=45, h= 8,border= "T", txt= "Altura capa: 5 mm",fill = 0)
        self.pdf.cell(w=75, h= 8,border= "TR",txt= "Volumen (h=5, r=50)= 39,27 cm3", fill = 0)
        self.pdf.multi_cell(w=5, h= 8,border= "R", fill = 0)
        
        #Parámetros tabla
        self.pdf.cell(w=5, h= 8,border= "L", fill = 0)
        self.pdf.cell(w=29, h= 8,border= 1,align= "C", 
                txt= "Tª Plato", fill = 0)
        self.pdf.cell(w=29, h= 8,border= 1,align= "C", 
                txt= "Tª Max", fill = 0)
        self.pdf.cell(w=24, h= 8,border= 1,align= "C", 
                txt= "¿Ignición?", fill = 0)
        self.pdf.cell(w=40, h= 8,border= 1, align= "C",
                txt= "Visual/termopar", fill = 0)
        self.pdf.cell(w=29, h= 8,border= 1, align= "C",
                txt= "Tiempo TªMax", fill = 0)
        self.pdf.cell(w=29, h= 8,border= 1, align= "C",
                txt= "Tiempo", fill = 0)

        self.pdf.multi_cell(w=5, h= 8,border= "R", fill = 0)

        #Resultados tabla (Habría que incluir esto en una clase con las variables)
        for fila in resultados:
            print(fila)
        for fila in resultados:
            self.pdf.cell(w=5, h= 8,border= "L", fill = 0)
            self.pdf.cell(w=29, h= 8,border= 1,align= "C",txt= str(int(fila.tPlato)), 
                    fill = 0)
            self.pdf.cell(w=29, h= 8,border= 1,align= "C",txt= str(int(fila.tMaxima)),
                    fill = 0)
            self.pdf.cell(w=24, h= 8,border= 1,align= "C",txt= fila.get_resultado_display(),
                    fill = 0)
            self.pdf.cell(w=40, h= 8,border= 1, align= "C",txt= fila.get_tipoIgnicion_display(),
                    fill = 0)
            self.pdf.cell(w=29, h= 8,border= 1, align= "C",txt= str(int(fila.tiempoTmax)),
                    fill = 0)
            self.pdf.cell(w=29, h= 8,border= 1, align= "C",txt= str(int(fila.tiempoPrueba)),
                    fill = 0)
            self.pdf.multi_cell(w=5, h= 8,border= "R", fill = 0)
        
        try:
                if ensayo.funde != "1":
                        ti = int(float(ensayo.resultado))
                        ta = int(float(ensayo.resultado)) - 10
                else:
                        ti = "Funde a " + str(ensayo.resultado)
                        ta = "No funde a " + str(int(float(ensayo.resultado)) - 10)  
        except Exception as e:
            print(f"Error: {e}")
            ti= ensayo.resultado
            ta= "N/D"

        #Celda con Resultados
        self.pdf.multi_cell(w=190, h= 5,border= "LR", fill = 0)
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LRT", txt= "RESULTADOS",
                align= "J", fill = 0)
        self.pdf.set_font('Arial', '', 12) 
        
        if ti == ">400":
            self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= f"Menor temperatura a la que se produce ignición:     {ti} ºC* ",
                    align= "J", fill = 0)
        else:
            self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= f"Menor temperatura a la que se produce ignición:     {str(ti)} ºC* ",
                    align= "J", fill = 0)

        self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= f"Mayor temperatura a la que no se produce ignición:     {ta} ºC ",
                align= "J", fill = 0)

        #Celda resultado final       
        self.pdf.set_font('Arial', 'B', 14) 
        if ti == ">400":
            self.pdf.multi_cell(w=190, h= 8,border= 1, txt= f"TEMPERATURA MÍNIMA DE IGNICIÓN EN CAPA:     {ti} ºC ",
                    align= "C", fill = 0)
        else:
            self.pdf.multi_cell(w=190, h= 8,border= 1, txt= f"TEMPERATURA MÍNIMA DE IGNICIÓN EN CAPA:     {str(ti)} ºC ",
                    align= "C", fill = 0)
        #Firma
        self.pdf.set_font('Arial', '', 14) 
        self.pdf.cell(w=95, h= 8,border= 1, txt= f"Conforme:",
                align= "J", fill = 0)
        self.pdf.multi_cell(w=95, h= 8,border= 1, txt= f"Realizado: {ensayo.usuario.firmas.firma}",###
                align= "J", fill = 0)
        
        # Agregar más contenido dinámico aquí...
        return self.pdf.output(dest='S').encode('latin1')  # Devuelve bytes
        

    def tmin(self):
        ensayo= TMIn.objects.get(muestra= self.muestra)
        equipos=ensayo.equipos.all()
        resultados= ResultadosTMIn.objects.filter(ensayo= ensayo).order_by("id")
        ensayoForma= self.descripcion.get_formaEnsayo_display()
        fechaInicio= ensayo.fechaInicio
        fechaFin= ensayo.fechaFin

        self.pdf = FPDF(orientation = 'P', unit= 'mm', format = 'A4')
        self.pdf.add_page()
        #TEXTO 
        self.pdf.set_font('Arial', '', 12)
        #IMAGEN
        image_path = os.path.join(self.rutaAbsoluta, 'Imagenes', 'LOGO.png')
        self.pdf.image(image_path, x=8, y=8, w=30, h=30, link="http://www.lom.upm.es", type='PNG')
        #Celdas Cabecera
        self.pdf.cell(w=35, h= 12,border= 0,
                align= "C", fill = 0)
        self.pdf.set_font('Arial', '', 11)
        self.pdf.cell(w= 100, h= 12, txt = f'{ensayo.ensayo.ensayo} ({ensayo.ensayo.normativa})', border= 1, 
                align= "C", fill = 0)
        self.pdf.set_font('Arial', '', 12)
        if fechaInicio!= fechaFin:
            self.pdf.multi_cell(w=0, h= 12, txt = f"Fecha Inicio: {fechaInicio.strftime('%d/%m/%Y')}", border= "RT", 
                    align= "L", fill = 0)
        else:
            self.pdf.multi_cell(w=0, h= 12, txt = "Fecha:", border= "RT", 
                align= "L", fill = 0)

        self.pdf.cell(w=35, h= 12,border= 0,
                align= "C", fill = 0)
        self.pdf.cell(w=100, h= 12, txt = f'Nº Expediente: {ensayo.muestra.expediente.expediente}',border= "LRB", 
                align= "C", fill = 0)
        if fechaInicio == fechaFin:
            self.pdf.multi_cell(w=0, h= 12, txt = fechaInicio.strftime("%d/%m/%Y"), border= "RB", 
                    align= "C", fill = 0)
        else:
              self.pdf.multi_cell(w=0, h= 12, txt = f'Fecha fin: {fechaFin.strftime("%d/%m/%Y")} ', border= "RB", 
                    align= "L", fill = 0)

        #Celda I/D muestra
        self.pdf.multi_cell(w=0, h= 5,border= 0,
                align= "C", fill = 0)
        self.pdf.cell(w=130, h= 8,border= 0, txt= f"Material: {self.descripcion.id_fabricante}",
                align= "J", fill = 0)
        self.pdf.multi_cell(w=60, h= 8,border= 0, txt= f"Identificación: {self.identificacion}",
                align= "J", fill = 0)

        #Celda Tratamiento de muestras  
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.cell(w=65, h= 8,border= "LT", txt= "MUESTRA DE POLVO",
                align= "J", fill = 0)

        self.pdf.set_font('Arial', '', 12)    
        self.pdf.multi_cell(w=125, h= 8,border= "TR", txt= f"La muestra se ensaya {ensayoForma}",
                align= "J", fill = 0)


        #Celda Condiciones ambientales  
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LRT", txt= "CONDICIONES AMBIENTALES",
                align= "J", fill = 0)

        self.pdf.set_font('Arial', '', 12)    
        self.pdf.cell(w=60, h= 8,border= "L", txt= f"Temperatura: {ensayo.temperaturaAmbiente} ºC",
                align= "C", fill = 0)

        self.pdf.cell(w=70, h= 8,border= "", txt= f"Humedad: {ensayo.humedad} %",
                align= "C", fill = 0)
        
        self.pdf.multi_cell(w=60, h= 8,border= "R", txt= f"Presión: {ensayo.presion} mBar",
                align= "C", fill = 0)


        #Celda Equipos
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LRT", txt= "EQUIPOS DE ENSAYO",
                align= "J", fill = 0)
        self.pdf.set_font('Arial', '', 12)
        self.pdf.multi_cell(w=190, h= 8,border= "LBR", txt = "Equipos: " + " | ".join(equipo.codigo for equipo in equipos),###
                align= "J", fill = 0)



        #Celda Procedimiento
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= "PROCEDIMIENTO",
                align= "J", fill = 0)
        #Leyenda Masa de polvo
        self.pdf.cell(w=5, h= 8,border= "L", fill = 0)    
        self.pdf.set_font('Arial', '', 12)
        self.pdf.cell(w=30, h= 8,border= "LT", txt= "Masas:", fill = 0, align= "C")
        self.pdf.cell(w=60, h= 8,border= "TR",txt= "0,05; 0,1; 0,2; 0,3; 0,5 g", fill = 0,align= "C")
        self.pdf.cell(w=30, h= 8,border= "LT", txt= "Presiones:", fill = 0, align= "C")
        self.pdf.cell(w=60, h= 8,border= "TR",txt= "10; 20; 30; 50 kPa", fill = 0, align= "C")
        self.pdf.multi_cell(w=5, h= 8,border= "R", fill = 0)

        #Leyenda Presión
        self.pdf.cell(w=5, h= 8,border= "L", fill = 0)    
        self.pdf.set_font('Arial', '', 12)
        self.pdf.cell(w=60, h= 8,border= "LTRB",txt= "Incrementos: +50 ºC", fill = 0, align= "C")
        self.pdf.cell(w=120, h= 8,border= "TRB",txt= "*Decrementos: Tª>300ºC: -20ºC  |  Tª<300ºC: -10ºC", fill = 0, align= "C")
        self.pdf.multi_cell(w=5, h= 8,border= "R", fill = 0)

        #Espacio
        self.pdf.multi_cell(w=190, h= 8,border= "LR", fill = 0)
        
        #Parámetros tabla
        self.pdf.cell(w=5, h= 8,border= "L", fill = 0)
        self.pdf.cell(w=45, h= 8,border= 1,align= "C", 
                txt= "Tª Horno(ºC)", fill = 0)
        self.pdf.cell(w=45, h= 8,border= 1,align= "C", 
                txt= "Peso(g)", fill = 0)
        self.pdf.cell(w=45, h= 8,border= 1,align= "C", 
                txt= "Presión (kPa)", fill = 0)
        self.pdf.cell(w=45, h= 8,border= 1, align= "C",
                txt= "Resultado", fill = 0)

        self.pdf.multi_cell(w=5, h= 8,border= "R", fill = 0)

        #Resultados tabla (Habría que incluir esto en una clase con las variables)

        for fila in resultados:
                self.pdf.cell(w=5, h= 8,border= "L", fill = 0)
                self.pdf.cell(w=45, h= 8,border= 1,align= "C",txt= str(int(fila.tHorno)), 
                        fill = 0)
                self.pdf.cell(w=45, h= 8,border= 1,align= "C",txt= str(int(fila.peso)),
                        fill = 0)
                self.pdf.cell(w=45, h= 8,border= 1,align= "C",txt= str(int(fila.presion)),
                        fill = 0)
                self.pdf.cell(w=45, h= 8,border= 1, align= "C",txt= str(fila.get_resultado_display()),
                        fill = 0)
                self.pdf.multi_cell(w=5, h= 8,border= "R", fill = 0)

        print(ensayo.resultado)
        try:
            ti= int(float(ensayo.resultado))
            if ti >= 280:
                ta= int(float(ensayo.resultado)) + 20
            else:
                ta= int(float(ensayo.resultado)) + 10
        except:
            ti= ensayo.resultado
            ta= "N/D"
        print(ti)

        #Celda con Resultados
        self.pdf.multi_cell(w=190, h= 5,border= "LR", fill = 0)
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LRT", txt= "RESULTADOS",
                align= "J", fill = 0)
        self.pdf.set_font('Arial', '', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= f"Menor temperatura a la que se produce ignición (ti):     {str(ta)} ºC ",
                align= "J", fill = 0)
        
        try:
                if ti > 300:
                        self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= f"*Temperatura minima de ignición en nube, al ser mayor de 300ºC:      {str(ti)} ºC ",
                                align= "J", fill = 0)
                        #Celda resultado final       
                        self.pdf.set_font('Arial', 'B', 14) 
                        self.pdf.multi_cell(w=190, h= 8,border= 1, txt= f"TEMPERATURA MÍNIMA DE IGNICIÓN EN NUBE:     {str(ti)} ºC ",
                                align= "C", fill = 0)
                else:
                        self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= f"*Temperatura minima de ignición en nube, al ser menor de 300ºC:     {str(ti)} ºC ",
                                align= "J", fill = 0)
                        #Celda resultado final       
                        self.pdf.set_font('Arial', 'B', 14) 
                        self.pdf.multi_cell(w=190, h= 8,border= 1, txt= f"TEMPERATURA MÍNIMA DE IGNICIÓN EN NUBE:     {str(ti)} ºC ",
                                align= "C", fill = 0)
        except:
                self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= f"*Temperatura mínima de ignición en nube:      {str(ti)} ºC ",
                                align= "J", fill = 0)
                        #Celda resultado final       
                self.pdf.set_font('Arial', 'B', 14) 
                self.pdf.multi_cell(w=190, h= 8,border= 1, txt= f"TEMPERATURA MÍNIMA DE IGNICIÓN EN NUBE:     {str(ti)} ºC ",
                        align= "C", fill = 0)
        #Firma
        self.pdf.set_font('Arial', '', 14) 
        self.pdf.cell(w=95, h= 8,border= 1, txt= f"Conforme:",
                align= "J", fill = 0)
        self.pdf.multi_cell(w=95, h= 8,border= 1, txt= f"Realizado: {ensayo.usuario.firmas.firma}",###
                align= "J", fill = 0)
        
        # Agregar más contenido dinámico aquí...
        return self.pdf.output(dest='S').encode('latin1')  # Devuelve bytes
    

    def humedad(self):
        ensayo= Humedad.objects.get(muestra= self.muestra)
        equipos=ensayo.equipos.all()
        resultados= ResultadosHumedad.objects.filter(ensayo= ensayo).order_by("id")
        ensayoForma= self.descripcion.get_formaEnsayo_display()
        fechaInicio= ensayo.fechaInicio
        fechaFin= ensayo.fechaFin

        self.pdf = FPDF(orientation = 'P', unit= 'mm', format = 'A4')
        self.pdf.add_page()
        #TEXTO 
        self.pdf.set_font('Arial', '', 12)
        #IMAGEN
        image_path = os.path.join(self.rutaAbsoluta, 'Imagenes', 'LOGO.png')
        self.pdf.image(image_path, x=8, y=8, w=30, h=30, link="http://www.lom.upm.es", type='PNG')
        #Celdas Cabecera
        self.pdf.cell(w=35, h= 12,border= 0,
                align= "C", fill = 0)
        self.pdf.set_font('Arial', '', 11)
        self.pdf.cell(w= 100, h= 12, txt = f'{ensayo.ensayo.ensayo} ({ensayo.ensayo.normativa})', border= 1, 
                align= "C", fill = 0)
        self.pdf.set_font('Arial', '', 12)
        if fechaInicio!= fechaFin:
            self.pdf.multi_cell(w=0, h= 12, txt = f"Fecha Inicio: {fechaInicio.strftime('%d/%m/%Y')}", border= "RT", 
                    align= "L", fill = 0)
        else:
            self.pdf.multi_cell(w=0, h= 12, txt = "Fecha:", border= "RT", 
                align= "L", fill = 0)

        self.pdf.cell(w=35, h= 12,border= 0,
                align= "C", fill = 0)
        self.pdf.cell(w=100, h= 12, txt = f'Nº Expediente: {ensayo.muestra.expediente.expediente}',border= "LRB", 
                align= "C", fill = 0)
        if fechaInicio == fechaFin:
            self.pdf.multi_cell(w=0, h= 12, txt = fechaInicio.strftime("%d/%m/%Y"), border= "RB", 
                    align= "C", fill = 0)
        else:
              self.pdf.multi_cell(w=0, h= 12, txt = f'Fecha fin: {fechaFin.strftime("%d/%m/%Y")} ', border= "RB", 
                    align= "L", fill = 0)

        #Celda I/D muestra
        self.pdf.multi_cell(w=0, h= 5,border= 0,
                align= "C", fill = 0)
        self.pdf.cell(w=130, h= 8,border= 0, txt= f"Material: {self.descripcion.id_fabricante}",
                align= "J", fill = 0)
        self.pdf.multi_cell(w=60, h= 8,border= 0, txt= f"Identificación: {self.identificacion}",
                align= "J", fill = 0)

        #Celda Tratamiento de muestras  
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.cell(w=65, h= 8,border= "LT", txt= "MUESTRA DE POLVO",
                align= "J", fill = 0)

        self.pdf.set_font('Arial', '', 12)    
        self.pdf.multi_cell(w=125, h= 8,border= "TR", txt= f"La muestra se ensaya {ensayoForma}",
                align= "J", fill = 0)


        #Celda Equipos
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LRT", txt= "EQUIPOS DE ENSAYO",
                align= "J", fill = 0)
        self.pdf.set_font('Arial', '', 12)
        self.pdf.multi_cell(w=190, h= 8,border= "LBR", txt = "Equipos: " + " | ".join(equipo.codigo for equipo in equipos),###
                align= "J", fill = 0)
        
        #Celda Configuración equipo
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LRT", txt= "CONFIGURACIÓN EQUIPO",
                align= "J", fill = 0)
        self.pdf.set_font('Arial', '', 12)
        self.pdf.multi_cell(w=190, h= 8,border= "LR", txt = f"Criterio de desconexión: {ensayo.get_criterio_display()}",###
                align= "J", fill = 0)
        self.pdf.multi_cell(w=190, h= 8,border= "LBR", txt = f"Temperatura de desecación: {str(int(float(ensayo.tDesecacion)))} ºC",###
                align= "J", fill = 0)



        #Celda Resultados
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= "RESULTADOS",
                align= "J", fill = 0)
        
        self.pdf.multi_cell(w=190, h= 8,border= "RL", fill = 0)
        
        #Si el ensayo se ha podido hacer
        if ensayo.resultado != "N/D":
                self.pdf.set_font('Arial', '', 12) 
                for i,fila in enumerate(resultados[:3]):
                        self.pdf.cell(w=5, h= 8,border= "L", fill = 0)
                        self.pdf.cell(w=180, h= 8,border= 0,align= "L",txt= f'Humedad {i+1}: {str(float(fila.resultado))} %', 
                                fill = 0)
                        self.pdf.multi_cell(w=5, h= 8,border= "R", fill = 0)

                self.pdf.multi_cell(w=190, h= 8,border= "RL", fill = 0)


                self.pdf.cell(w=5, h= 8,border= "L", fill = 0)
                self.pdf.cell(w=180, h= 8,border= 0,align= "L",txt= f'Desviacion típica: {str(float(ensayo.desviacion))} %', 
                        fill = 0)
                self.pdf.multi_cell(w=5, h= 8,border= "R", fill = 0)
                

                if (float(ensayo.desviacion)<= 0.15):
                        self.pdf.cell(w=5, h= 8,border= "L", fill = 0)
                        self.pdf.cell(w=180, h= 8,border= 0,align= "L",txt= f'Ensayo válido al tener una desviación menor de 0.15%', 
                                fill = 0)
                        self.pdf.multi_cell(w=5, h= 8,border= "R", fill = 0) 
                else:
                        self.pdf.cell(w=5, h= 8,border= "L", fill = 0)
                        self.pdf.cell(w=180, h= 8,border= 0,align= "L",txt= f'Al tener un desviación superior a 0.15% el ensayo requiero de 10 resultados', 
                                fill = 0)
                        self.pdf.multi_cell(w=5, h= 8,border= "R", fill = 0) 

                        for i,fila in enumerate(resultados[3:]):
                                self.pdf.cell(w=5, h= 8,border= "L", fill = 0)

                                self.pdf.cell(w=180, h= 8,border= 0,align= "L",txt= f'Humedad {i+4}: {str(float(fila.resultado))} %', 
                                        fill = 0)
                                self.pdf.multi_cell(w=5, h= 8,border= "R", fill = 0)
                
                self.pdf.set_font('Arial', 'B', 12) 
                
                self.pdf.multi_cell(w=190, h= 8,border= "RL", fill = 0)
                self.pdf.cell(w=5, h= 8,border= "L", fill = 0)
                self.pdf.cell(w=180, h= 8,border= 0,align= "L",txt= f'HUMEDAD MEDIA: {str(float(ensayo.resultado))} %', 
                        fill = 0)
                self.pdf.multi_cell(w=5, h= 8,border= "R", fill = 0)
                self.pdf.multi_cell(w=190, h= 8,border= "RL", fill = 0)
        
        #Si el ensayo no se ha podido hacer        
        else:
                for i,fila in enumerate(resultados[:3]):
                        self.pdf.cell(w=5, h= 8,border= "L", fill = 0)
                        self.pdf.cell(w=180, h= 8,border= 0,align= "L",txt= f'Humedad {i+1}: {fila.resultado}', 
                                fill = 0)
                        self.pdf.multi_cell(w=5, h= 8,border= "R", fill = 0)

                self.pdf.multi_cell(w=190, h= 8,border= "RL", fill = 0)

                self.pdf.cell(w=5, h= 8,border= "L", fill = 0)
                self.pdf.cell(w=180, h= 8,border= 0,align= "L",txt= f'El ensayo no se puede hacer', 
                        fill = 0)
                self.pdf.multi_cell(w=5, h= 8,border= "R", fill = 0)

                self.pdf.set_font('Arial', 'B', 12) 
                
                self.pdf.multi_cell(w=190, h= 8,border= "RL", fill = 0)
                self.pdf.cell(w=5, h= 8,border= "L", fill = 0)
                self.pdf.cell(w=180, h= 8,border= 0,align= "L",txt= f'HUMEDAD MEDIA: {ensayo.resultado} %', 
                        fill = 0)
                self.pdf.multi_cell(w=5, h= 8,border= "R", fill = 0)
                self.pdf.multi_cell(w=190, h= 8,border= "RL", fill = 0)

             
        #Firma
        self.pdf.set_font('Arial', '', 14) 
        self.pdf.cell(w=95, h= 8,border= 1, txt= f"Conforme:",
                align= "J", fill = 0)
        self.pdf.multi_cell(w=95, h= 8,border= 1, txt= f"Realizado: {ensayo.usuario.firmas.firma}",###
                align= "J", fill = 0)
        
        # Agregar más contenido dinámico aquí...
        return self.pdf.output(dest='S').encode('latin1')  # Devuelve bytes


    def granulometria(self):
        try:
                ensayo = Granulometria.objects.get(muestra=self.muestra)
                
                if ensayo.archivo:  # Verifica si el archivo está presente
                        with ensayo.archivo.open('rb') as file:  # Abre el archivo como binario
                                contenido = file.read()
                                return contenido  # Retorna el contenido binario del archivo
                else:
                        return None  # Si no hay archivo, retorna None

        except Granulometria.DoesNotExist:
                return print("Granulometría no existe")  # Si no encuentra el objeto, retorna None


    def lie(self):
        ensayo= LIE.objects.get(muestra= self.muestra)
        equipos=ensayo.equipos.all()
        resultados= ResultadosLIE.objects.filter(ensayo= ensayo).order_by("id")
        ensayoForma= self.descripcion.get_formaEnsayo_display()
        fechaInicio= ensayo.fechaInicio
        fechaFin= ensayo.fechaFin

        self.pdf = FPDF(orientation = 'P', unit= 'mm', format = 'A4')
        self.pdf.add_page()
        #TEXTO 
        self.pdf.set_font('Arial', '', 12)
        #IMAGEN
        image_path = os.path.join(self.rutaAbsoluta, 'Imagenes', 'LOGO.png')
        self.pdf.image(image_path, x=8, y=8, w=30, h=30, link="http://www.lom.upm.es", type='PNG')
        #Celdas Cabecera
        self.pdf.cell(w=35, h= 12,border= 0,
                align= "C", fill = 0)
        self.pdf.set_font('Arial', '', 11)
        self.pdf.cell(w= 100, h= 12, txt = f'{ensayo.ensayo.ensayo} ({ensayo.ensayo.normativa})', border= 1, 
                align= "C", fill = 0)
        self.pdf.set_font('Arial', '', 12)
        if fechaInicio!= fechaFin:
            self.pdf.multi_cell(w=0, h= 12, txt = f"Fecha Inicio: {fechaInicio.strftime('%d/%m/%Y')}", border= "RT", 
                    align= "L", fill = 0)
        else:
            self.pdf.multi_cell(w=0, h= 12, txt = "Fecha:", border= "RT", 
                align= "L", fill = 0)

        self.pdf.cell(w=35, h= 12,border= 0,
                align= "C", fill = 0)
        self.pdf.cell(w=100, h= 12, txt = f'Nº Expediente: {ensayo.muestra.expediente.expediente}',border= "LRB", 
                align= "C", fill = 0)
        if fechaInicio == fechaFin:
            self.pdf.multi_cell(w=0, h= 12, txt = fechaInicio.strftime("%d/%m/%Y"), border= "RB", 
                    align= "C", fill = 0)
        else:
              self.pdf.multi_cell(w=0, h= 12, txt = f'Fecha fin: {fechaFin.strftime("%d/%m/%Y")} ', border= "RB", 
                    align= "L", fill = 0)

        #Celda I/D muestra
        self.pdf.multi_cell(w=0, h= 5,border= 0,
                align= "C", fill = 0)
        self.pdf.cell(w=130, h= 8,border= 0, txt= f"Material: {self.descripcion.id_fabricante}",
                align= "J", fill = 0)
        self.pdf.multi_cell(w=60, h= 8,border= 0, txt= f"Identificación: {self.identificacion}",
                align= "J", fill = 0)

        #Celda Tratamiento de muestras  
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.cell(w=65, h= 8,border= "LT", txt= "MUESTRA DE POLVO",
                align= "J", fill = 0)

        self.pdf.set_font('Arial', '', 12)    
        self.pdf.multi_cell(w=125, h= 8,border= "TR", txt= f"La muestra se ensaya {ensayoForma}",
                align= "J", fill = 0)


        #Celda Condiciones ambientales  
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LRT", txt= "CONDICIONES AMBIENTALES",
                align= "J", fill = 0)

        self.pdf.set_font('Arial', '', 12)    
        self.pdf.cell(w=60, h= 8,border= "L", txt= f"Temperatura: {ensayo.temperaturaAmbiente} ºC",
                align= "C", fill = 0)
        
        self.pdf.cell(w=70, h= 8,border= "", txt= f"Temperatura en esfera: {ensayo.temperaturaEsfera} ºC",
                align= "C", fill = 0)

        self.pdf.multi_cell(w=60, h= 8,border= "R", txt= f"Humedad: {ensayo.humedad} %",
                align= "C", fill = 0)


        #Celda Equipos
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LRT", txt= "EQUIPOS DE ENSAYO",
                align= "J", fill = 0)
        self.pdf.set_font('Arial', '', 12)
        self.pdf.multi_cell(w=190, h= 8,border= "LR", txt = "Equipos: " + " | ".join(equipo.codigo for equipo in equipos),###
                align= "J", fill = 0)
        self.pdf.multi_cell(w=190, h= 8,border= "LBR", txt = f"Cerillas: {ensayo.get_cerillas_display()} (2kJ)",
                align= "J", fill = 0)


        #Celda Resultados
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= "RESULTADOS",
                align= "J", fill = 0)
        
        self.pdf.multi_cell(w=190, h= 8,border= "RL", fill = 0)
        
        #Parámetros tabla
        self.pdf.cell(w=5, h= 16,border= "L", fill = 0)
        self.pdf.cell(w=50, h= 16,border= 1,align= "C", 
                txt= "Concentración (g/m3)", fill = 0)
        self.pdf.cell(w=20, h= 16,border= 1,align= "C", 
                txt= "Peso (g)", fill = 0)
        self.pdf.cell(w=25, h= 16,border= 1,align= "C", 
                txt= "Pex (bar)", fill = 0)
        self.pdf.cell(w=25, h= 16,border= 1, align= "C",
                txt= "Pm (bar)", fill = 0)
        self.pdf.cell(w=30, h= 16,border= 1, align= "C",
                txt= "dP/dT (bar/s)", fill = 0)
        self.pdf.cell(w=30, h= 16,border= 1, align= "C",
                txt= "Resultado", fill = 0)

        self.pdf.multi_cell(w=5, h= 16,border= "R", fill = 0)

        #Resultados tabla (Habría que incluir esto en una clase con las variables)
        for fila in resultados:
            print(fila)
        for fila in resultados:
            self.pdf.cell(w=5, h= 8,border= "L", fill = 0)
            self.pdf.cell(w=50, h= 8,border= 1,align= "C",txt= str(int(fila.concentracion)), 
                    fill = 0)
            self.pdf.cell(w=20, h= 8,border= 1,align= "C",txt= str(int(fila.peso)),
                    fill = 0)
            self.pdf.cell(w=25, h= 8,border= 1,align= "C",txt= str(float(fila.pex)),
                    fill = 0)
            self.pdf.cell(w=25, h= 8,border= 1, align= "C",txt= str(float(fila.pm)),
                    fill = 0)
            self.pdf.cell(w=30, h= 8,border= 1, align= "C",txt= str(float(fila.dpdt)),
                    fill = 0)
            self.pdf.cell(w=30, h= 8,border= 1, align= "C",txt= fila.get_resultado_display(),
                    fill = 0)
            self.pdf.multi_cell(w=5, h= 8,border= "R", fill = 0)
        
        #Si el ensayo se ha podido hacer

        self.pdf.multi_cell(w=190, h= 8,border= "RL", fill = 0)

        #Celda con Resultados
        self.pdf.multi_cell(w=190, h= 5,border= "LR", fill = 0)
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LRT", txt= "RESULTADOS",
                align= "J", fill = 0)
        
        if ensayo.resultado != "N/D":
                posiblesValores= [10, 20, 30, 60, 125, 250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750, 3000, 3250, 3500, 3750, 4000]
                
                concentracionNo= int(ensayo.resultado)
                concentracionSi = next((val for val in posiblesValores if val > concentracionNo), None)
        else:
              concentracionNo= "N/D"
              concentracionSi= "N/D"
              

        
        self.pdf.set_font('Arial', '', 12) 
        
        self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= f"Menor concentración a la que hay inflamación: {concentracionSi} g/m3",
                align= "J", fill = 0)
        
        self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= f"Mayor concentración a la que no hay inflamación: {concentracionNo} g/m3",
                align= "J", fill = 0)
        
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= f"LIMITE INFERIOR EXPLOSION: {concentracionNo} g/m3",
                align= "J", fill = 0)
        
             
        #Firma
        self.pdf.set_font('Arial', '', 14) 
        self.pdf.cell(w=95, h= 8,border= 1, txt= f"Conforme:",
                align= "J", fill = 0)
        self.pdf.multi_cell(w=95, h= 8,border= 1, txt= f"Realizado: {ensayo.usuario.firmas.firma}",###
                align= "J", fill = 0)
        
        # Agregar más contenido dinámico aquí...
        return self.pdf.output(dest='S').encode('latin1')  # Devuelve bytes


    def pmax(self):
        ensayo= Pmax.objects.get(muestra= self.muestra)
        equipos=ensayo.equipos.all()
        resultados= ResultadosPmax.objects.filter(ensayo= ensayo).order_by("id")
        ensayoForma= self.descripcion.get_formaEnsayo_display()
        fechaInicio= ensayo.fechaInicio
        fechaFin= ensayo.fechaFin


        self.pdf = FPDF(orientation = 'P', unit= 'mm', format = 'A4')
        self.pdf.add_page()
        #TEXTO 
        self.pdf.set_font('Arial', '', 10)
        #IMAGEN
        image_path = os.path.join(self.rutaAbsoluta, 'Imagenes', 'LOGO.png')
        self.pdf.image(image_path, x=8, y=8, w=30, h=30, link="http://www.lom.upm.es", type='PNG')
        #Celdas Cabecera
        self.pdf.cell(w=35, h= 12,border= 0,
                align= "C", fill = 0)
        self.pdf.set_font('Arial', '', 11)
        self.pdf.cell(w= 100, h= 12, txt = f'{ensayo.ensayo.ensayo} ({ensayo.ensayo.normativa})', border= 1, 
                align= "C", fill = 0)
        self.pdf.set_font('Arial', '', 12)
        if fechaInicio!= fechaFin:
            self.pdf.multi_cell(w=0, h= 12, txt = f"Fecha Inicio: {fechaInicio.strftime('%d/%m/%Y')}", border= "RT", 
                    align= "L", fill = 0)
        else:
            self.pdf.multi_cell(w=0, h= 12, txt = "Fecha:", border= "RT", 
                align= "L", fill = 0)

        self.pdf.cell(w=35, h= 12,border= 0,
                align= "C", fill = 0)
        self.pdf.cell(w=100, h= 12, txt = f'Nº Expediente: {ensayo.muestra.expediente.expediente}',border= "LRB", 
                align= "C", fill = 0)
        if fechaInicio == fechaFin:
            self.pdf.multi_cell(w=0, h= 12, txt = fechaInicio.strftime("%d/%m/%Y"), border= "RB", 
                    align= "C", fill = 0)
        else:
              self.pdf.multi_cell(w=0, h= 12, txt = f'Fecha fin: {fechaFin.strftime("%d/%m/%Y")} ', border= "RB", 
                    align= "L", fill = 0)

        #Celda I/D muestra
        self.pdf.multi_cell(w=0, h= 5,border= 0,
                align= "C", fill = 0)
        self.pdf.cell(w=130, h= 8,border= 0, txt= f"Material: {self.descripcion.id_fabricante}",
                align= "J", fill = 0)
        self.pdf.multi_cell(w=60, h= 8,border= 0, txt= f"Identificación: {self.identificacion}",
                align= "J", fill = 0)

        #Celda Tratamiento de muestras  
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.cell(w=65, h= 8,border= "LT", txt= "MUESTRA DE POLVO",
                align= "J", fill = 0)

        self.pdf.set_font('Arial', '', 12)    
        self.pdf.multi_cell(w=125, h= 8,border= "TR", txt= f"La muestra se ensaya {ensayoForma}",
                align= "J", fill = 0)


        #Celda Condiciones ambientales  
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LRT", txt= "CONDICIONES AMBIENTALES",
                align= "J", fill = 0)

        self.pdf.set_font('Arial', '', 12)    
        self.pdf.cell(w=60, h= 8,border= "L", txt= f"Temperatura: {ensayo.temperaturaAmbiente} ºC",
                align= "C", fill = 0)
        
        self.pdf.cell(w=70, h= 8,border= "", txt= f"Temperatura en esfera: {ensayo.temperaturaEsfera} ºC",
                align= "C", fill = 0)

        self.pdf.multi_cell(w=60, h= 8,border= "R", txt= f"Humedad: {ensayo.humedad} %",
                align= "C", fill = 0)


        #Celda Equipos
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LRT", txt= "EQUIPOS DE ENSAYO",
                align= "J", fill = 0)
        self.pdf.set_font('Arial', '', 12)
        self.pdf.multi_cell(w=190, h= 8,border= "LR", txt = "Equipos: " + " | ".join(equipo.codigo for equipo in equipos),
                align= "J", fill = 0)
        self.pdf.multi_cell(w=190, h= 8,border= "LBR", txt = f"Cerillas: {ensayo.get_cerillas_display()} (10kJ)",
                align= "J", fill = 0)


        #Celda Resultados
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= "RESULTADOS",
                align= "J", fill = 0)
                
        #Parámetros tabla
        self.pdf.cell(w=5, h= 8,border= "L", fill = 0)
        self.pdf.cell(w=50, h= 8,border= 1,align= "C", 
                txt= "Concentración (g/m3)", fill = 0)
        self.pdf.cell(w=40, h= 8,border= 1,align= "C", 
                txt= "Peso (g)", fill = 0)
        self.pdf.cell(w=30, h= 8,border= 1, align= "C",
                txt= "Serie", fill = 0)
        self.pdf.cell(w=30, h= 8,border= 1, align= "C",
                txt= "Pm (bar)", fill = 0)
        self.pdf.cell(w=30, h= 8,border= 1, align= "C",
                txt= "dP/dT(bar/s)", fill = 0)

        self.pdf.multi_cell(w=5, h= 8,border= "R", fill = 0)
        

        for resultado in resultados:
                self.pdf.cell(w=5, h= 6,border= "L", fill = 0)
                self.pdf.cell(w=50, h= 6,border= 1,align= "C", 
                        txt= str(int(resultado.concentracion)), fill = 0)
                self.pdf.cell(w=40, h= 6,border= 1,align= "C", 
                        txt= str(resultado.peso), fill = 0)
                self.pdf.cell(w=30, h= 6,border= 1, align= "C",
                        txt= str(resultado.serie), fill = 0)
                self.pdf.cell(w=30, h= 6,border= 1,align= "C", 
                        txt= str(resultado.pm), fill = 0)
                self.pdf.cell(w=30, h= 6,border= 1, align= "C",
                        txt= str(resultado.dpdt), fill = 0)

                self.pdf.multi_cell(w=5, h= 6,border= "R", fill = 0)
        
        self.pdf.multi_cell(w=190, h= 6,border= "LR", fill = 0)


        #TABLA RESUMEN
        #tabla pMax
        self.pdf.cell(w=5, h= 6,border= "L", fill = 0)
        self.pdf.cell(w=40, h= 6,border= 1,align= "C", 
                txt= "P max", fill = 0)
        self.pdf.cell(w=40, h= 6,border= 1,align= "C", 
                txt= "Bar", fill = 0)
        self.pdf.cell(w=20, h= 20,border= 0, fill = 0)

        #Tabla dpdt
        self.pdf.cell(w=40, h= 6,border= 1,align= "C", 
                txt= "dP/dT max", fill = 0)
        self.pdf.cell(w=40, h= 6,border= 1,align= "C", 
                txt= "Bar/s", fill = 0)
        self.pdf.multi_cell(w=5, h= 6,border= "R", fill = 0)

        #pmax
        resultadosSerie1= resultados.filter(serie="1")
        resultadosSerie2= resultados.filter(serie="2")
        resultadosSerie3= resultados.filter(serie="3")

        valoresPm1= []
        valoresDpdt1=[]
        valoresPm2= []
        valoresDpdt2=[]
        valoresPm3= []
        valoresDpdt3=[]

        pmax1= 0
        pmax2= 0
        pmax3= 0

        dpdt1= 0
        dpdt2= 0
        dpdt3= 0

        for resultado in resultados:
            if resultado.serie == "1":
                valoresPm1.append(resultado.pm)
                valoresDpdt1.append(resultado.dpdt)
                pmax1= max(valoresPm1)
                dpdt1= max(valoresDpdt1)
                    

            elif resultado.serie== "2":
                valoresPm2.append(resultado.pm)
                valoresDpdt2.append(resultado.dpdt)
                pmax2= max(valoresPm2)
                dpdt2= max(valoresDpdt2)

            if resultado.serie== "3":
                valoresPm3.append(resultado.pm)
                valoresDpdt3.append(resultado.dpdt)
                pmax3= max(valoresPm3)
                dpdt3= max(valoresDpdt3)
                
        #Sacamos el valor de pmax y dpdt del ensayo
        pmMaxima= max(pmax1, pmax2, pmax3)
        dPdTMaxima= max(dpdt1,dpdt2,dpdt3)

        concentracionesPmax= []
        concentracionesDpdt= []

        #Buscamos la concentracion
        if ensayo.pmax != 0.0:
            for resultado in resultados:
                if resultado.pm == pmMaxima:
                    concentracionesPmax.append(resultado.concentracion)
                if resultado.dpdt == dPdTMaxima:
                    concentracionesDpdt.append(resultado.concentracion)
                
            print(concentracionesPmax, concentracionesDpdt)
        else:
            concentracionesPmax= ["-"]
            concentracionesDpdt= ["-"]


        self.pdf.cell(w=5, h= 6,border= "L", fill = 0)
        self.pdf.cell(w=40, h= 6,border= 1,align= "C", 
                txt= "Serie 1", fill = 0)
        self.pdf.cell(w=40, h= 6,border= 1,align= "C", 
                txt= str(pmax1), fill = 0)

        self.pdf.cell(w=20, h= 6,border= 0,align= "C", fill = 0)


        self.pdf.cell(w=40, h= 6,border= 1,align= "C", 
                txt= "Serie 1", fill = 0)
        self.pdf.cell(w=40, h= 6,border= 1,align= "C", 
                txt= str(dpdt1), fill = 0)
        self.pdf.multi_cell(w=5, h= 6,border= "R", fill = 0)



        self.pdf.cell(w=5, h= 6,border= "L", fill = 0)
        self.pdf.cell(w=40, h= 6,border= 1,align= "C", 
                txt= "Serie 2", fill = 0)
        self.pdf.cell(w=40, h= 6,border= 1,align= "C", 
                txt= str(pmax2), fill = 0)

        self.pdf.cell(w=20, h= 6,border= 0,align= "C", fill = 0)


        self.pdf.cell(w=40, h= 6,border= 1,align= "C", 
                txt= "Serie 2", fill = 0)
        self.pdf.cell(w=40, h= 6,border= 1,align= "C", 
                txt= str(dpdt2), fill = 0)
        self.pdf.multi_cell(w=5, h= 6,border= "R", fill = 0)


        self.pdf.cell(w=5, h= 6,border= "L", fill = 0)
        self.pdf.cell(w=40, h= 6,border= 1,align= "C", 
                txt= "Serie 3", fill = 0)
        self.pdf.cell(w=40, h= 6,border= 1,align= "C", 
                txt= str(pmax3), fill = 0)

        self.pdf.cell(w=20, h= 6,border= 0,align= "C", fill = 0)


        self.pdf.cell(w=40, h= 6,border= 1,align= "C", 
                txt= "Serie 3", fill = 0)
        self.pdf.cell(w=40, h= 6,border= 1,align= "C", 
                txt= str(dpdt3), fill = 0)
        self.pdf.multi_cell(w=5, h= 6,border= "R", fill = 0)



        self.pdf.cell(w=5, h= 6,border= "L", fill = 0)
        self.pdf.cell(w=40, h= 6,border= 1,align= "C", 
                txt= "Pmax media", fill = 0)
        self.pdf.cell(w=40, h= 6,border= 1,align= "C", 
                txt= str(ensayo.pmax), fill = 0)

        self.pdf.cell(w=20, h= 6,border= 0,align= "C", fill = 0)


        self.pdf.cell(w=40, h= 6,border= 1,align= "C", 
                txt= "dP/dT media", fill = 0)
        self.pdf.cell(w=40, h= 6,border= 1,align= "C", 
                txt= str(ensayo.dpdt), fill = 0)
        self.pdf.multi_cell(w=5, h= 6,border= "R", fill = 0)

        self.pdf.multi_cell(w=190, h= 6,border= "LR", fill = 0)


        self.pdf.multi_cell(w=190, h= 5,border= "LR", fill = 0)
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 6,border= "LRT", txt= "RESUMEN",
                align= "J", fill = 0)
                      
        
        self.pdf.set_font('Arial', '', 12)
        self.pdf.set_font('Arial', '', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= f"""La mayor Pmax registrada es de {pmMaxima} bar a una concentración de {', '.join(str(c) for c in concentracionesPmax)} g/m3; la mayor dPdT registrada es de {dPdTMaxima} bar/s a una concentración de {', '.join(str(c) for c in concentracionesDpdt)} g/m3""",   
                align= "J", fill = 0)
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= f"PRESIÓN MÁXIMA DE EXPLOSIÓN: {ensayo.pmax} bar",
                align= "J", fill = 0)
        self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= f"VELOCIDAD DE AUMENTO DE PRESIÓN: {ensayo.dpdt} dP/dT",
                align= "J", fill = 0)
        
        self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= f"kmax: {ensayo.kmax} bar·m/s",
                align= "J", fill = 0)
        
        
        
             
        #Firma
        self.pdf.set_font('Arial', '', 14) 
        self.pdf.cell(w=95, h= 6,border= 1, txt= f"Conforme:",
                align= "J", fill = 0)
        self.pdf.multi_cell(w=95, h= 6,border= 1, txt= f"Realizado: {ensayo.usuario.firmas.firma}",###
                align= "J", fill = 0)
        
        # Agregar más contenido dinámico aquí...
        return self.pdf.output(dest='S').encode('latin1')  # Devuelve bytes
    
    
    def emi(self):
        ensayo= EMI.objects.get(muestra= self.muestra)
        equipos=ensayo.equipos.all()
        resultados= ResultadosEMI.objects.filter(ensayo= ensayo).order_by("id")
        ensayoForma= self.descripcion.get_formaEnsayo_display()
        fechaInicio= ensayo.fechaInicio
        fechaFin= ensayo.fechaFin

        self.pdf = FPDF(orientation = 'P', unit= 'mm', format = 'A4')
        self.pdf.add_page()
        #TEXTO 
        self.pdf.set_font('Arial', '', 12)
        #IMAGEN
        image_path = os.path.join(self.rutaAbsoluta, 'Imagenes', 'LOGO.png')
        self.pdf.image(image_path, x=8, y=8, w=30, h=30, link="http://www.lom.upm.es", type='PNG')
        #Celdas Cabecera
        self.pdf.cell(w=35, h= 12,border= 0,
                align= "C", fill = 0)
        self.pdf.set_font('Arial', '', 11)
        self.pdf.cell(w= 100, h= 12, txt = f'{ensayo.ensayo.ensayo} ({ensayo.ensayo.normativa})', border= 1, 
                align= "C", fill = 0)
        self.pdf.set_font('Arial', '', 12)
        if fechaInicio!= fechaFin:
            self.pdf.multi_cell(w=0, h= 12, txt = f"Fecha Inicio: {fechaInicio.strftime('%d/%m/%Y')}", border= "RT", 
                    align= "L", fill = 0)
        else:
            self.pdf.multi_cell(w=0, h= 12, txt = "Fecha:", border= "RT", 
                align= "L", fill = 0)

        self.pdf.cell(w=35, h= 12,border= 0,
                align= "C", fill = 0)
        self.pdf.cell(w=100, h= 12, txt = f'Nº Expediente: {ensayo.muestra.expediente.expediente}',border= "LRB", 
                align= "C", fill = 0)
        if fechaInicio == fechaFin:
            self.pdf.multi_cell(w=0, h= 12, txt = fechaInicio.strftime("%d/%m/%Y"), border= "RB", 
                    align= "C", fill = 0)
        else:
              self.pdf.multi_cell(w=0, h= 12, txt = f'Fecha fin: {fechaFin.strftime("%d/%m/%Y")} ', border= "RB", 
                    align= "L", fill = 0)

        #Celda I/D muestra
        self.pdf.multi_cell(w=0, h= 5,border= 0,
                align= "C", fill = 0)
        self.pdf.cell(w=130, h= 8,border= 0, txt= f"Material: {self.descripcion.id_fabricante}",
                align= "J", fill = 0)
        self.pdf.multi_cell(w=60, h= 8,border= 0, txt= f"Identificación: {self.identificacion}",
                align= "J", fill = 0)

        #Celda Tratamiento de muestras  
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.cell(w=65, h= 8,border= "LT", txt= "MUESTRA DE POLVO",
                align= "J", fill = 0)

        self.pdf.set_font('Arial', '', 12)    
        self.pdf.multi_cell(w=125, h= 8,border= "TR", txt= f"La muestra se ensaya {ensayoForma}",
                align= "J", fill = 0)
        
        #Celda Tipo ensayo 
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.cell(w=65, h= 8,border= "LT", txt= "TIPO ENSAYO",
                align= "J", fill = 0)
        if ensayo.inductancia == "1":
            self.pdf.set_font('Arial', '', 12)    
            self.pdf.multi_cell(w=125, h= 8,border= "TR", txt= f"Ensayo realizado con una inductancia de 1 mH",
                    align= "J", fill = 0)
        else:
            self.pdf.set_font('Arial', '', 12)    
            self.pdf.multi_cell(w=125, h= 8,border= "TR", txt= f"Ensayo realizado sin inductancia",
                    align= "J", fill = 0) 


        #Celda Condiciones ambientales  
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LRT", txt= "CONDICIONES AMBIENTALES",
                align= "J", fill = 0)

        self.pdf.set_font('Arial', '', 12)    
        self.pdf.cell(w=60, h= 8,border= "L", txt= f"Temperatura: {ensayo.temperaturaAmbiente} ºC",
                align= "C", fill = 0)

        self.pdf.cell(w=70, h= 8,border= "", txt= f"Humedad: {ensayo.humedad} %",
                align= "C", fill = 0)
        
        self.pdf.multi_cell(w=60, h= 8,border= "R", txt= f"Presión: {ensayo.presion} mBar",
                align= "C", fill = 0)


        #Celda Equipos
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LRT", txt= "EQUIPOS DE ENSAYO",
                align= "J", fill = 0)
        self.pdf.set_font('Arial', '', 12)
        self.pdf.multi_cell(w=190, h= 8,border= "LBR", txt = "Equipos: " + " | ".join(equipo.codigo for equipo in equipos),###
                align= "J", fill = 0)


        #Celda Resultados
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= "RESULTADOS",
                align= "J", fill = 0)
        
        self.pdf.multi_cell(w=190, h= 8,border= "RL", fill = 0)
        
        #Parámetros tabla
        self.pdf.cell(w=5, h= 16,border= "L", fill = 0)
        self.pdf.cell(w=45, h= 16,border= 1,align= "C", 
                txt= "Concentración (mg)", fill = 0)
        self.pdf.cell(w=40, h= 16,border= 1,align= "C", 
                txt= "Energía (mJ)", fill = 0)
        self.pdf.cell(w=35, h= 16,border= 1,align= "C", 
                txt= "Retardo (ms)", fill = 0)
        self.pdf.cell(w=30, h= 16,border= 1, align= "C",
                txt= "Resultado", fill = 0)
        self.pdf.cell(w=30, h= 16,border= 1, align= "C",
                txt= "Nº Ensayo", fill = 0)

        self.pdf.multi_cell(w=5, h= 16,border= "R", fill = 0)

        #Resultados tabla (Habría que incluir esto en una clase con las variables)
        for fila in resultados:
            self.pdf.cell(w=5, h= 8,border= "L", fill = 0)
            self.pdf.cell(w=45, h= 8,border= 1,align= "C",txt= str(int(fila.concentracion)), 
                    fill = 0)
            self.pdf.cell(w=40, h= 8,border= 1,align= "C",txt= str(int(fila.energia)),
                    fill = 0)
            self.pdf.cell(w=35, h= 8,border= 1,align= "C",txt= str(int(fila.retardo)),
                    fill = 0)
            self.pdf.cell(w=30, h= 8,border= 1, align= "C",txt= str(fila.get_resultado_display()),
                    fill = 0)
            self.pdf.cell(w=30, h= 8,border= 1, align= "C",txt= str(fila.numeroEnsayo),
                    fill = 0)

            self.pdf.multi_cell(w=5, h= 8,border= "R", fill = 0)
        
        #Si el ensayo se ha podido hacer

        self.pdf.multi_cell(w=190, h= 8,border= "RL", fill = 0)

        #Celda con Resultados
        self.pdf.multi_cell(w=190, h= 5,border= "LR", fill = 0)
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LRT", txt= "RESULTADOS",
                align= "J", fill = 0)
        
        
        resultadoEmi= str(ensayo.resultado)

        if ensayo.resultado != "N/D":
                posiblesValores= [1000,300,100,30,10,3,1]
                energiaSi=1001
                for resultado in resultados:
                        if resultado.resultado == "1" and int(resultado.energia) < energiaSi:
                                energiaSi= resultado.energia                 

                if int(energiaSi) != 1:
                        energiaNo = next((val for val in posiblesValores if val < int(energiaSi)), None)
                else:
                        energiaNo= "-"
        else:
              energiaNo= "1000"
              energiaSi= "N/D"
              resultadoEmi= "N/D"
              
        
        
        self.pdf.set_font('Arial', '', 12) 

        self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= f"Menor energía a la que hay inflamación: {energiaSi} mJ (E2)",
                align= "J", fill = 0)
        
        self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= f"Mayor energía a la que no hay inflamación: {energiaNo} mJ (E1)",
                align= "J", fill = 0)
        
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= f"ENERGÍA MÍNIMA DE INFLAMACIÓN: {resultadoEmi} mJ",
                align= "J", fill = 0)
        
             
        #Firma
        self.pdf.set_font('Arial', '', 14) 
        self.pdf.cell(w=95, h= 8,border= 1, txt= f"Conforme:",
                align= "J", fill = 0)
        self.pdf.multi_cell(w=95, h= 8,border= 1, txt= f"Realizado: {ensayo.usuario.firmas.firma}",###
                align= "J", fill = 0)
        
        # Agregar más contenido dinámico aquí...
        return self.pdf.output(dest='S').encode('latin1')  # Devuelve bytes
    

    def emiSin(self):
        ensayo= EMIsin.objects.get(muestra= self.muestra)
        equipos=ensayo.equipos.all()
        resultados= ResultadosEMIsin.objects.filter(ensayo= ensayo).order_by("id")
        ensayoForma= self.descripcion.get_formaEnsayo_display()
        fechaInicio= ensayo.fechaInicio
        fechaFin= ensayo.fechaFin

        self.pdf = FPDF(orientation = 'P', unit= 'mm', format = 'A4')
        self.pdf.add_page()
        #TEXTO 
        self.pdf.set_font('Arial', '', 12)
        #IMAGEN
        image_path = os.path.join(self.rutaAbsoluta, 'Imagenes', 'LOGO.png')
        self.pdf.image(image_path, x=8, y=8, w=30, h=30, link="http://www.lom.upm.es", type='PNG')
        #Celdas Cabecera
        self.pdf.cell(w=35, h= 12,border= 0,
                align= "C", fill = 0)
        self.pdf.set_font('Arial', '', 11)
        self.pdf.cell(w= 100, h= 12, txt = f'{ensayo.ensayo.ensayo} ({ensayo.ensayo.normativa})', border= 1, 
                align= "C", fill = 0)
        self.pdf.set_font('Arial', '', 12)
        if fechaInicio!= fechaFin:
            self.pdf.multi_cell(w=0, h= 12, txt = f"Fecha Inicio: {fechaInicio.strftime('%d/%m/%Y')}", border= "RT", 
                    align= "L", fill = 0)
        else:
            self.pdf.multi_cell(w=0, h= 12, txt = "Fecha:", border= "RT", 
                align= "L", fill = 0)

        self.pdf.cell(w=35, h= 12,border= 0,
                align= "C", fill = 0)
        self.pdf.cell(w=100, h= 12, txt = f'Nº Expediente: {ensayo.muestra.expediente.expediente}',border= "LRB", 
                align= "C", fill = 0)
        if fechaInicio == fechaFin:
            self.pdf.multi_cell(w=0, h= 12, txt = fechaInicio.strftime("%d/%m/%Y"), border= "RB", 
                    align= "C", fill = 0)
        else:
              self.pdf.multi_cell(w=0, h= 12, txt = f'Fecha fin: {fechaFin.strftime("%d/%m/%Y")} ', border= "RB", 
                    align= "L", fill = 0)

        #Celda I/D muestra
        self.pdf.multi_cell(w=0, h= 5,border= 0,
                align= "C", fill = 0)
        self.pdf.cell(w=130, h= 8,border= 0, txt= f"Material: {self.descripcion.id_fabricante}",
                align= "J", fill = 0)
        self.pdf.multi_cell(w=60, h= 8,border= 0, txt= f"Identificación: {self.identificacion}",
                align= "J", fill = 0)

        #Celda Tratamiento de muestras  
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.cell(w=65, h= 8,border= "LT", txt= "MUESTRA DE POLVO",
                align= "J", fill = 0)

        self.pdf.set_font('Arial', '', 12)    
        self.pdf.multi_cell(w=125, h= 8,border= "TR", txt= f"La muestra se ensaya {ensayoForma}",
                align= "J", fill = 0)
        
        #Celda Tipo ensayo 
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.cell(w=65, h= 8,border= "LT", txt= "TIPO ENSAYO",
                align= "J", fill = 0)
        if ensayo.inductancia == "1":
            self.pdf.set_font('Arial', '', 12)    
            self.pdf.multi_cell(w=125, h= 8,border= "TR", txt= f"Ensayo realizado con una inductancia de 1 mH",
                    align= "J", fill = 0)
        else:
            self.pdf.set_font('Arial', '', 12)    
            self.pdf.multi_cell(w=125, h= 8,border= "TR", txt= f"Ensayo realizado sin inductancia",
                    align= "J", fill = 0) 


        #Celda Condiciones ambientales  
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LRT", txt= "CONDICIONES AMBIENTALES",
                align= "J", fill = 0)

        self.pdf.set_font('Arial', '', 12)    
        self.pdf.cell(w=60, h= 8,border= "L", txt= f"Temperatura: {ensayo.temperaturaAmbiente} ºC",
                align= "C", fill = 0)

        self.pdf.cell(w=70, h= 8,border= "", txt= f"Humedad: {ensayo.humedad} %",
                align= "C", fill = 0)
        
        self.pdf.multi_cell(w=60, h= 8,border= "R", txt= f"Presión: {ensayo.presion} mBar",
                align= "C", fill = 0)


        #Celda Equipos
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LRT", txt= "EQUIPOS DE ENSAYO",
                align= "J", fill = 0)
        self.pdf.set_font('Arial', '', 12)
        self.pdf.multi_cell(w=190, h= 8,border= "LBR", txt = "Equipos: " + " | ".join(equipo.codigo for equipo in equipos),###
                align= "J", fill = 0)


        #Celda Resultados
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= "RESULTADOS",
                align= "J", fill = 0)
        
        self.pdf.multi_cell(w=190, h= 8,border= "RL", fill = 0)
        
        #Parámetros tabla
        self.pdf.cell(w=5, h= 16,border= "L", fill = 0)
        self.pdf.cell(w=45, h= 16,border= 1,align= "C", 
                txt= "Concentración (mg)", fill = 0)
        self.pdf.cell(w=40, h= 16,border= 1,align= "C", 
                txt= "Energía (mJ)", fill = 0)
        self.pdf.cell(w=35, h= 16,border= 1,align= "C", 
                txt= "Retardo (ms)", fill = 0)
        self.pdf.cell(w=30, h= 16,border= 1, align= "C",
                txt= "Resultado", fill = 0)
        self.pdf.cell(w=30, h= 16,border= 1, align= "C",
                txt= "Nº Ensayo", fill = 0)

        self.pdf.multi_cell(w=5, h= 16,border= "R", fill = 0)

        #Resultados tabla (Habría que incluir esto en una clase con las variables)
        for fila in resultados:
            self.pdf.cell(w=5, h= 8,border= "L", fill = 0)
            self.pdf.cell(w=45, h= 8,border= 1,align= "C",txt= str(int(fila.concentracion)), 
                    fill = 0)
            self.pdf.cell(w=40, h= 8,border= 1,align= "C",txt= str(int(fila.energia)),
                    fill = 0)
            self.pdf.cell(w=35, h= 8,border= 1,align= "C",txt= str(int(fila.retardo)),
                    fill = 0)
            self.pdf.cell(w=30, h= 8,border= 1, align= "C",txt= str(fila.get_resultado_display()),
                    fill = 0)
            self.pdf.cell(w=30, h= 8,border= 1, align= "C",txt= str(fila.numeroEnsayo),
                    fill = 0)

            self.pdf.multi_cell(w=5, h= 8,border= "R", fill = 0)
        
        #Si el ensayo se ha podido hacer

        self.pdf.multi_cell(w=190, h= 8,border= "RL", fill = 0)

        #Celda con Resultados
        self.pdf.multi_cell(w=190, h= 5,border= "LR", fill = 0)
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LRT", txt= "RESULTADOS",
                align= "J", fill = 0)
        
        
        resultadoEmi= str(ensayo.resultado)

        if ensayo.resultado != "N/D":
                posiblesValores= [1000,300,100,30,10,3,1]
                energiaSi=1001
                for resultado in resultados:
                        if resultado.resultado == "1" and int(resultado.energia) < energiaSi:
                                energiaSi= resultado.energia                 

                if int(energiaSi) != 1:
                        energiaNo = next((val for val in posiblesValores if val < int(energiaSi)), None)
                else:
                        energiaNo= "-"
        else:
              energiaNo= "1000"
              energiaSi= "N/D"
              resultadoEmi= "N/D"
              
        
        
        self.pdf.set_font('Arial', '', 12) 

        self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= f"Menor energía a la que hay inflamación: {energiaSi} mJ (E2)",
                align= "J", fill = 0)
        
        self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= f"Mayor energía a la que no hay inflamación: {energiaNo} mJ (E1)",
                align= "J", fill = 0)
        
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= f"ENERGÍA MÍNIMA DE INFLAMACIÓN: {resultadoEmi} mJ",
                align= "J", fill = 0)
        
             
        #Firma
        self.pdf.set_font('Arial', '', 14) 
        self.pdf.cell(w=95, h= 8,border= 1, txt= f"Conforme:",
                align= "J", fill = 0)
        self.pdf.multi_cell(w=95, h= 8,border= 1, txt= f"Realizado: {ensayo.usuario.firmas.firma}",###
                align= "J", fill = 0)
        
        # Agregar más contenido dinámico aquí...
        return self.pdf.output(dest='S').encode('latin1')  # Devuelve bytes
    

    def rec(self):
        ensayo= REC.objects.get(muestra= self.muestra)
        equipos=ensayo.equipos.all()
        resultados= ResultadosREC.objects.filter(ensayo= ensayo).order_by("id")
        ensayoForma= self.descripcion.get_formaEnsayo_display()
        fechaInicio= ensayo.fechaInicio
        fechaFin= ensayo.fechaFin

        self.pdf = FPDF(orientation = 'P', unit= 'mm', format = 'A4')
        self.pdf.add_page()
        #TEXTO 
        self.pdf.set_font('Arial', '', 12)
        #IMAGEN
        logo_path = os.path.join(self.rutaAbsoluta, 'Imagenes', 'LOGO.png')
        self.pdf.image(logo_path, x=8, y=8, w=30, h=30, link="http://www.lom.upm.es", type='PNG')
        #Celdas Cabecera
        self.pdf.cell(w=35, h= 12,border= 0,
                align= "C", fill = 0)
        self.pdf.set_font('Arial', '', 11)
        self.pdf.cell(w= 100, h= 12, txt = f'{ensayo.ensayo.ensayo} ({ensayo.ensayo.normativa})', border= 1, 
                align= "C", fill = 0)
        self.pdf.set_font('Arial', '', 12)
        if fechaInicio!= fechaFin:
            self.pdf.multi_cell(w=0, h= 12, txt = f"Fecha Inicio: {fechaInicio.strftime('%d/%m/%Y')}", border= "RT", 
                    align= "L", fill = 0)
        else:
            self.pdf.multi_cell(w=0, h= 12, txt = "Fecha:", border= "RT", 
                align= "L", fill = 0)

        self.pdf.cell(w=35, h= 12,border= 0,
                align= "C", fill = 0)
        self.pdf.cell(w=100, h= 12, txt = f'Nº Expediente: {ensayo.muestra.expediente.expediente}',border= "LRB", 
                align= "C", fill = 0)
        if fechaInicio == fechaFin:
            self.pdf.multi_cell(w=0, h= 12, txt = fechaInicio.strftime("%d/%m/%Y"), border= "RB", 
                    align= "C", fill = 0)
        else:
              self.pdf.multi_cell(w=0, h= 12, txt = f'Fecha fin: {fechaFin.strftime("%d/%m/%Y")} ', border= "RB", 
                    align= "L", fill = 0)
              

        #Celda I/D muestra
        self.pdf.multi_cell(w=0, h= 5,border= 0,
                align= "C", fill = 0)
        self.pdf.cell(w=130, h= 8,border= 0, txt= f"Material: {self.descripcion.id_fabricante}",
                align= "J", fill = 0)
        self.pdf.multi_cell(w=60, h= 8,border= 0, txt= f"Identificación: {self.identificacion}",
                align= "J", fill = 0)

        #Celda Tratamiento de muestras  
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.cell(w=65, h= 8,border= "LT", txt= "MUESTRA DE POLVO",
                align= "J", fill = 0)

        self.pdf.set_font('Arial', '', 12)    
        self.pdf.multi_cell(w=125, h= 8,border= "TR", txt= f"La muestra se ensaya {ensayoForma}",
                align= "J", fill = 0)


        #Celda Condiciones ambientales  
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LRT", txt= "CONDICIONES AMBIENTALES",
                align= "J", fill = 0)

        self.pdf.set_font('Arial', '', 12)    
        self.pdf.cell(w=60, h= 8,border= "L", txt= f"Temperatura: {ensayo.temperaturaAmbiente} ºC",
                align= "C", fill = 0)

        self.pdf.cell(w=70, h= 8,border= "", txt= f"Humedad: {ensayo.humedad} %",
                align= "C", fill = 0)
        
        self.pdf.multi_cell(w=60, h= 8,border= "R", txt= f"Presión: {ensayo.presion} mBar",
                align= "C", fill = 0)


        #Celda Equipos
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LRT", txt= "EQUIPOS DE ENSAYO",
                align= "J", fill = 0)
        self.pdf.set_font('Arial', '', 12)
        self.pdf.multi_cell(w=190, h= 8,border= "LBR", txt = "Equipos: " + " | ".join(equipo.codigo for equipo in equipos),###
                align= "J", fill = 0)


        #Celda Resultados
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= "RESULTADOS",
                align= "J", fill = 0)
        
        self.pdf.multi_cell(w=190, h= 8,border= "RL", fill = 0)
        
        #Parámetros tabla
        self.pdf.cell(w=5, h= 16,border= "L", fill = 0)
        self.pdf.cell(w=60, h= 16,border= 1,align= "C", 
                txt= "Tensión (V)", fill = 0)
        self.pdf.cell(w=60, h= 16,border= 1,align= "C", 
                txt= "Tiempo (s)", fill = 0)
        self.pdf.cell(w=60, h= 16,border= 1, align= "C",
                txt= "Resultado (Mohm)", fill = 0)

        self.pdf.multi_cell(w=5, h= 16,border= "R", fill = 0)

        listaResultados1= []
        listaResultados2= []
        #Resultados tabla (Habría que incluir esto en una clase con las variables)
        for fila in resultados:
            self.pdf.cell(w=5, h= 8,border= "L", fill = 0)

            self.pdf.cell(w=60, h= 8,border= 1,align= "C",txt= str(int(fila.tension)), 
                    fill = 0)
            self.pdf.cell(w=60, h= 8,border= 1,align= "C",txt= str(int(fila.tiempo)),
                    fill = 0)
            self.pdf.cell(w=60, h= 8,border= 1,align= "C",txt= str(float(fila.resultado)),
                    fill = 0)

            self.pdf.multi_cell(w=5, h= 8,border= "R", fill = 0)

            if fila.nPrueba == "1":
                listaResultados1.append(fila.resultado)
            else:
                listaResultados2.append(fila.resultado)
        
        
        
        #Si el ensayo se ha podido hacer

        self.pdf.multi_cell(w=190, h= 8,border= "RL", fill = 0)

        #Celda con Resultados
        self.pdf.multi_cell(w=190, h= 5,border= "LR", fill = 0)
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LRT", txt= "RESULTADOS",
                align= "J", fill = 0)
        
        
        resultado= ensayo.resultado
        menorResistencia1= min(listaResultados1)
        menorResistencia2 = min(listaResultados2)

        valorMedioMenorResistencia= ((menorResistencia1 + menorResistencia2)/2)* 1000000

        menorResistencia= "{:.2E}".format(valorMedioMenorResistencia)

        print(f'el resultado es: {resultado}')

        if resultado != 0:
                resultadoRec= "{:.2E}".format(resultado)
        
        
        self.pdf.set_font('Arial', 'B', 12) 

        self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= f"Media de las resistencias mínimas medidas(rs): {menorResistencia} ohm",
                align= "J", fill = 0)
        
        self.pdf.multi_cell(w=190, h= 30,border= "LR", fill = 0)
        
        formulaImage_path = os.path.join(self.rutaAbsoluta, 'Imagenes', 'formulaRec.png')

        # Medidas de la imagen
        image_width = 50
        image_height = 15

        # Calcular posición horizontal para centrar
        page_width = self.pdf.w - 2 * self.pdf.l_margin  # Ancho de la página sin márgenes
        x_position = (page_width - image_width) / 2 + self.pdf.l_margin  # Centrar considerando los márgenes

        # Obtener la posición actual después del texto
        y_position = self.pdf.get_y() - (10 + image_height)  # +10 para dejar un pequeño espacio después del texto

        #volvemos el cursor a después de la imagen
        self.pdf.set_y(y_position + image_height + 10)

        # Insertar la imagen centrada
        self.pdf.image(formulaImage_path, x=x_position, y=y_position, w=image_width, h=image_height, link="http://www.lom.upm.es", type='PNG')

        clasificacion=""
        if resultado <= 1000:
            clasificacion= "clasifica como polvo IIIC, clasifica como polvo conductivo"
        else:
            clasificacion= "clasifica como polvo IIIB, polvo no conductivo"

        self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= f"RESISTIVIDAD ELECTRICA EN CAPA: {resultadoRec} ohm · m, {clasificacion}",
                align= "J", fill = 0)
        
        
        
        self.pdf.multi_cell(w=190, h= 8,border= "LR", fill = 0)
             
        #Firma
        self.pdf.set_font('Arial', '', 14) 
        self.pdf.cell(w=95, h= 8,border= 1, txt= f"Conforme:",
                align= "J", fill = 0)
        self.pdf.multi_cell(w=95, h= 8,border= 1, txt= f"Realizado: {ensayo.usuario.firmas.firma}",###
                align= "J", fill = 0)
        
        # Agregar más contenido dinámico aquí...
        return self.pdf.output(dest='S').encode('latin1')  # Devuelve bytes
        
   
    def clo(self):
        ensayo= CLO.objects.get(muestra= self.muestra)
        equipos=ensayo.equipos.all()
        resultados= ResultadosCLO.objects.filter(ensayo= ensayo).order_by("id")
        ensayoForma= self.descripcion.get_formaEnsayo_display()
        fechaInicio= ensayo.fechaInicio
        fechaFin= ensayo.fechaFin

        self.pdf = FPDF(orientation = 'P', unit= 'mm', format = 'A4')
        self.pdf.add_page()
        #TEXTO 
        self.pdf.set_font('Arial', '', 12)
        #IMAGEN
        image_path = os.path.join(self.rutaAbsoluta, 'Imagenes', 'LOGO.png')
        self.pdf.image(image_path, x=8, y=8, w=30, h=30, link="http://www.lom.upm.es", type='PNG')
        #Celdas Cabecera
        self.pdf.cell(w=35, h= 12,border= 0,
                align= "C", fill = 0)
        self.pdf.cell(w= 100, h= 12, txt = f'{ensayo.ensayo.ensayo} \n ({ensayo.ensayo.normativa})', border= 1, 
                align= "C", fill = 0)
        if fechaInicio!= fechaFin:
            self.pdf.multi_cell(w=0, h= 12, txt = f"Fecha Inicio: {fechaInicio.strftime('%d/%m/%Y')}", border= "RT", 
                    align= "L", fill = 0)
        else:
            self.pdf.multi_cell(w=0, h= 12, txt = "Fecha:", border= "RT", 
                align= "L", fill = 0)

        self.pdf.cell(w=35, h= 12,border= 0,
                align= "C", fill = 0)
        self.pdf.cell(w=100, h= 12, txt = f'Nº Expediente: {ensayo.muestra.expediente.expediente}',border= "LRB", 
                align= "C", fill = 0)
        if fechaInicio == fechaFin:
            self.pdf.multi_cell(w=0, h= 12, txt = fechaInicio.strftime("%d/%m/%Y"), border= "RB", 
                    align= "C", fill = 0)
        else:
              self.pdf.multi_cell(w=0, h= 12, txt = f'Fecha fin: {fechaFin.strftime("%d/%m/%Y")} ', border= "RB", 
                    align= "L", fill = 0)

        #Celda I/D muestra
        self.pdf.multi_cell(w=0, h= 5,border= 0,
                align= "C", fill = 0)
        self.pdf.cell(w=130, h= 8,border= 0, txt= f"Material: {self.descripcion.id_fabricante}",
                align= "J", fill = 0)
        self.pdf.multi_cell(w=60, h= 8,border= 0, txt= f"Identificación: {self.identificacion}",
                align= "J", fill = 0)

        #Celda Tratamiento de muestras  
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.cell(w=65, h= 8,border= "LT", txt= "MUESTRA DE POLVO",
                align= "J", fill = 0)

        self.pdf.set_font('Arial', '', 12)    
        self.pdf.multi_cell(w=125, h= 8,border= "TR", txt= f"La muestra se ensaya {ensayoForma}",
                align= "J", fill = 0)


        #Celda Condiciones ambientales  
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LRT", txt= "CONDICIONES AMBIENTALES",
                align= "J", fill = 0)

        self.pdf.set_font('Arial', '', 12)    
        self.pdf.cell(w=60, h= 8,border= "L", txt= f"Temperatura: {ensayo.temperaturaAmbiente} ºC",
                align= "C", fill = 0)
        
        self.pdf.cell(w=70, h= 8,border= "", txt= f"Temperatura en esfera: {ensayo.temperaturaEsfera} ºC",
                align= "C", fill = 0)

        self.pdf.multi_cell(w=60, h= 8,border= "R", txt= f"Humedad: {ensayo.humedad} %",
                align= "C", fill = 0)


        #Celda Equipos
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LRT", txt= "EQUIPOS DE ENSAYO",
                align= "J", fill = 0)
        self.pdf.set_font('Arial', '', 12)
        self.pdf.multi_cell(w=190, h= 8,border= "LR", txt = "Equipos: " + " | ".join(equipo.codigo for equipo in equipos),
                align= "J", fill = 0)
        self.pdf.multi_cell(w=190, h= 8,border= "LBR", txt = f"Cerillas: {ensayo.get_cerillas_display()} (2kJ)",
                align= "J", fill = 0)


        #Celda Resultados
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= "RESULTADOS",
                align= "J", fill = 0)
        
        self.pdf.multi_cell(w=190, h= 8,border= "RL", fill = 0)
        
        #Parámetros tabla
        self.pdf.cell(w=5, h= 16,border= "L", fill = 0)
        self.pdf.cell(w=45, h= 16,border= 1,align= "C", 
                txt= "Concentración (g/m3)", fill = 0)
        self.pdf.cell(w=20, h= 16,border= 1,align= "C", 
                txt= "Peso (g)", fill = 0)
        self.pdf.cell(w=20, h= 16,border= 1,align= "C", 
                txt= "Pex (bar)", fill = 0)
        self.pdf.cell(w=20, h= 16,border= 1, align= "C",
                txt= "Pm (bar)", fill = 0)
        self.pdf.cell(w=30, h= 16,border= 1, align= "C",
                txt= "dP/dT (bar/s)", fill = 0)
        self.pdf.cell(w=20, h= 16,border= 1, align= "C",
                txt= "Oxígeno", fill = 0)
        self.pdf.cell(w=25, h= 16,border= 1, align= "C",
                txt= "Resultado", fill = 0)

        self.pdf.multi_cell(w=5, h= 16,border= "R", fill = 0)

        #Resultados tabla (Habría que incluir esto en una clase con las variables)
        for fila in resultados:
            print(fila)
        for fila in resultados:
            self.pdf.cell(w=5, h= 8,border= "L", fill = 0)
            self.pdf.cell(w=45, h= 8,border= 1,align= "C",txt= str(int(fila.concentracion)), 
                    fill = 0)
            self.pdf.cell(w=20, h= 8,border= 1,align= "C",txt= str(int(fila.peso)),
                    fill = 0)
            self.pdf.cell(w=20, h= 8,border= 1,align= "C",txt= str(float(fila.pex)),
                    fill = 0)
            self.pdf.cell(w=20, h= 8,border= 1, align= "C",txt= str(float(fila.pm)),
                    fill = 0)
            self.pdf.cell(w=30, h= 8,border= 1, align= "C",txt= str(int(fila.dpdt)),
                    fill = 0)
            self.pdf.cell(w=20, h= 8,border= 1, align= "C",txt= str(int(fila.oxigeno)),
                    fill = 0)
            self.pdf.cell(w=25, h= 8,border= 1, align= "C",txt= fila.get_resultado_display(),
                    fill = 0)
            self.pdf.multi_cell(w=5, h= 8,border= "R", fill = 0)
        
        #Si el ensayo se ha podido hacer

        self.pdf.multi_cell(w=190, h= 8,border= "RL", fill = 0)

        #Celda con Resultados
        self.pdf.multi_cell(w=190, h= 5,border= "LR", fill = 0)
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LRT", txt= "RESULTADOS",
                align= "J", fill = 0)
        
        def calculoConcentraciones(oxigeno):
            listaConcentraciones=[]
            for resultado in resultados:
                if resultado.oxigeno == int(oxigeno):
                    listaConcentraciones.append(int(resultado.concentracion))
                    listaConcentraciones = list(set(listaConcentraciones))

            return (listaConcentraciones)
        
        if ensayo.resultado != "N/D":
              oxigenoNo= str(ensayo.resultado)
              oxigenoSi= str(int(ensayo.resultado) + 1)
              
              concentracionesNo=calculoConcentraciones(oxigenoNo)
              concentracionesSi=calculoConcentraciones(oxigenoSi)
              
              
                
        else:
              oxigenoNo= "N/D"
              oxigenoSi= "N/D"
        
        

        
        self.pdf.set_font('Arial', '', 12) 
        
        self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= f"Menor concentración de oxígeno a la que hay explosión: {oxigenoSi}% a las concentraciones de {','.join(map(str, concentracionesSi))}",
                align= "J", fill = 0)
        
        self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= f"Mayor concentración de oxígeno a la que no hay explosión: {oxigenoNo}% a las concentraciones de {','.join(map(str, concentracionesNo))}",
                align= "J", fill = 0)
        
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= f"LIMITE INFERIOR EXPLOSION: {oxigenoNo} %",
                align= "J", fill = 0)
        
             
        #Firma
        self.pdf.set_font('Arial', '', 14) 
        self.pdf.cell(w=95, h= 8,border= 1, txt= f"Conforme:",
                align= "J", fill = 0)
        self.pdf.multi_cell(w=95, h= 8,border= 1, txt= f"Realizado: {ensayo.usuario.firmas.firma}",###
                align= "J", fill = 0)
        
        # Agregar más contenido dinámico aquí...
        return self.pdf.output(dest='S').encode('latin1')  # Devuelve bytes


    def N4(self):
        ensayo= N4.objects.get(muestra= self.muestra)
        equipos=ensayo.equipos.all()
        resultados= ResultadosN4.objects.filter(ensayo= ensayo).order_by("id")
        ensayoForma= self.descripcion.get_formaEnsayo_display()
        fechaInicio= ensayo.fechaInicio
        fechaFin= ensayo.fechaFin

        resultado1 = None
        resultado2 = None
        resultado3 = None
        resultado4 = None

        for resultado in resultados:  # Aquí debe haber un ":" al final de la línea
                print(resultado.celda)
                print(resultado.tConsigna)
                if resultado.celda == "2" and resultado.tConsigna == "3":
                        resultado1 = resultado
                if resultado.celda == "1" and resultado.tConsigna == "3":
                        resultado2 = resultado
                if resultado.celda == "2" and resultado.tConsigna == "2":
                        resultado3 = resultado
                if resultado.celda == "2" and resultado.tConsigna == "1":
                        resultado4 = resultado


        self.pdf = FPDF(orientation = 'P', unit= 'mm', format = 'A4')
        self.pdf.add_page()
        #TEXTO 
        self.pdf.set_font('Arial', '', 12)
        #IMAGEN
        image_path = os.path.join(self.rutaAbsoluta, 'Imagenes', 'LOGO.png')
        self.pdf.image(image_path, x=8, y=8, w=30, h=30, link="http://www.lom.upm.es", type='PNG')
        #Celdas Cabecera
        self.pdf.cell(w=35, h= 12,border= 0,
                align= "C", fill = 0)
        self.pdf.set_font('Arial', '', 11)
        self.pdf.cell(w= 100, h= 12, txt = f'{ensayo.ensayo.ensayo} ({ensayo.ensayo.normativa})', border= 1, 
                align= "C", fill = 0)
        self.pdf.set_font('Arial', '', 12)
        if fechaInicio!= fechaFin:
            self.pdf.multi_cell(w=0, h= 12, txt = f"Fecha Inicio: {fechaInicio.strftime('%d/%m/%Y')}", border= "RT", 
                    align= "L", fill = 0)
        else:
            self.pdf.multi_cell(w=0, h= 12, txt = "Fecha:", border= "RT", 
                align= "L", fill = 0)

        self.pdf.cell(w=35, h= 12,border= 0,
                align= "C", fill = 0)
        self.pdf.cell(w=100, h= 12, txt = f'Nº Expediente: {ensayo.muestra.expediente.expediente}',border= "LRB", 
                align= "C", fill = 0)
        if fechaInicio == fechaFin:
            self.pdf.multi_cell(w=0, h= 12, txt = fechaInicio.strftime("%d/%m/%Y"), border= "RB", 
                    align= "C", fill = 0)
        else:
              self.pdf.multi_cell(w=0, h= 12, txt = f'Fecha fin: {fechaFin.strftime("%d/%m/%Y")} ', border= "RB", 
                    align= "L", fill = 0)

        #Celda I/D muestra
        self.pdf.multi_cell(w=0, h= 5,border= 0,
                align= "C", fill = 0)
        self.pdf.cell(w=130, h= 8,border= 0, txt= f"Material: {self.descripcion.id_fabricante}",
                align= "J", fill = 0)
        self.pdf.multi_cell(w=60, h= 8,border= 0, txt= f"Identificación: {self.identificacion}",
                align= "J", fill = 0)

        #Celda Tratamiento de muestras  
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.cell(w=65, h= 8,border= "LT", txt= "MUESTRA DE POLVO",
                align= "J", fill = 0)

        self.pdf.set_font('Arial', '', 12)    
        self.pdf.multi_cell(w=125, h= 8,border= "TR", txt= f"La muestra se ensaya {ensayoForma}",
                align= "J", fill = 0)


        #Celda Condiciones ambientales  
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LRT", txt= "CONDICIONES AMBIENTALES",
                align= "J", fill = 0)

        self.pdf.set_font('Arial', '', 12)    
        self.pdf.cell(w=95, h= 8,border= "L", txt= f"Temperatura: {ensayo.temperaturaAmbiente} ºC",
                align= "C", fill = 0)

        self.pdf.multi_cell(w=95, h= 8,border= "R", txt= f"Humedad: {ensayo.humedad} %",
                align= "C", fill = 0)


        #Celda Equipos
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LRT", txt= "EQUIPOS DE ENSAYO",
                align= "J", fill = 0)
        self.pdf.set_font('Arial', '', 12)
        self.pdf.multi_cell(w=190, h= 8,border= "LBR", txt = "Equipos: " + " | ".join(equipo.codigo for equipo in equipos),###
                align= "J", fill = 0)


        #Celda Resultados
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= "PROCEDIMIENTO",
                align= "J", fill = 0)
        
        

        #Primera prueba temperatura 140ºC a 100 mm
        if resultado1:
                self.pdf.set_font('Arial', '', 12) 
                self.pdf.cell(w=5, h= 8,border= "L",
                        align= "C", fill = 0)
                self.pdf.cell(w=90, h= 8,border= 0, txt= "Temperatura del ensayo: 140 ºC(+-2ºC)",
                        align= "C", fill = 0)
                self.pdf.cell(w=90, h= 8,border= 0, txt= "Celda 100 mm de lado",
                        align= "C", fill = 0)
                self.pdf.multi_cell(w=5, h= 8, border= "R",
                        align= "C", fill = 0)
                
                self.pdf.cell(w=5, h= 8,border= "L",
                        align= "C", fill = 0)
                self.pdf.cell(w=180, h= 8,border= 0, txt= "¿Tras 24h, supera los 200ºC?",
                        align= "L", fill = 0)
                self.pdf.multi_cell(w=5, h= 8, border= "R",
                        align= "C", fill = 0)

                self.pdf.cell(w=5, h= 8, border= "L",
                        align= "C", fill = 0)
                
                if int(resultado1.tMax) >= 200:
                        self.pdf.cell(w=180, h= 8,border= 0, txt= f"La muestra supera los 200ºC, siendo la temperatura máxima alcanzada de {resultado1.tMax} ºC",
                                align= "L", fill = 0)
                else:
                        self.pdf.cell(w=180, h= 8,border= 0, txt= f"La muestra no supera los 200ºC, siendo la temperatura máxima alcanzada de {resultado1.tMax} ºC",
                                        align= "L", fill = 0)
                                
                self.pdf.multi_cell(w=5, h= 8, border= "R",
                        align= "C", fill = 0)

                self.pdf.multi_cell(w=190, h= 8,border= "LBR",
                        align= "J", fill = 0)
        
        #Segunda prueba temperatura 140ºC a 25 mm
        if resultado2:
                self.pdf.set_font('Arial', '', 12) 
                self.pdf.cell(w=5, h= 8,border= "L",
                        align= "C", fill = 0)
                self.pdf.cell(w=90, h= 8,border= 0, txt= "Temperatura del ensayo: 140 ºC (+-2ºC)",
                        align= "C", fill = 0)
                self.pdf.cell(w=90, h= 8,border= 0, txt= "Celda 25 mm de lado",
                        align= "C", fill = 0)
                self.pdf.multi_cell(w=5, h= 8, border= "R",
                        align= "C", fill = 0)
                
                self.pdf.cell(w=5, h= 8,border= "L",
                        align= "C", fill = 0)
                self.pdf.cell(w=180, h= 8,border= 0, txt= "¿Tras 24h, supera los 200ºC?",
                        align= "L", fill = 0)
                self.pdf.multi_cell(w=5, h= 8, border= "R",
                        align= "C", fill = 0)
                self.pdf.cell(w=5, h= 8, border= "L",
                        align= "C", fill = 0)
                
                if int(resultado2.tMax) >= 200:
                        self.pdf.cell(w=180, h= 8,border= 0, txt= f"La muestra supera los 200ºC, siendo la temperatura máxima alcanzada de {resultado2.tMax} ºC",
                                align= "L", fill = 0)
                else:
                        self.pdf.cell(w=180, h= 8,border= 0, txt= f"La muestra no supera los 200ºC, siendo la temperatura máxima alcanzada de {resultado2.tMax} ºC",
                                        align= "L", fill = 0)
                                
                self.pdf.multi_cell(w=5, h= 8, border= "R",
                        align= "C", fill = 0)   

                self.pdf.multi_cell(w=190, h= 8,border= "LBR",
                        align= "J", fill = 0)             

        #Tercera prueba temperatura 120ºC a 100 mm
        if resultado3:
                self.pdf.set_font('Arial', '', 12) 
                self.pdf.cell(w=5, h= 8,border= "L",
                        align= "C", fill = 0)
                self.pdf.cell(w=90, h= 8,border= 0, txt= "Temperatura del ensayo: 120 ºC(+-2ºC)",
                        align= "C", fill = 0)
                self.pdf.cell(w=90, h= 8,border= 0, txt= "Celda 100 mm de lado",
                        align= "C", fill = 0)
                self.pdf.multi_cell(w=5, h= 8, border= "R",
                        align= "C", fill = 0)
                
                self.pdf.cell(w=5, h= 8,border= "L",
                        align= "C", fill = 0)
                self.pdf.cell(w=180, h= 8,border= 0, txt= "¿Tras 24h, supera los 180ºC?",
                        align= "L", fill = 0)
                self.pdf.multi_cell(w=5, h= 8, border= "R",
                        align= "C", fill = 0)

                self.pdf.cell(w=5, h= 8, border= "L",
                        align= "C", fill = 0)
                
                if int(resultado3.tMax) >= 200:
                        self.pdf.cell(w=180, h= 8,border= 0, txt= f"La muestra supera los 180ºC, siendo la temperatura máxima alcanzada de {resultado3.tMax} ºC",
                                align= "L", fill = 0)
                else:
                        self.pdf.cell(w=180, h= 8,border= 0, txt= f"La muestra no supera los 180ºC, siendo la temperatura máxima alcanzada de {resultado3.tMax} ºC",
                                        align= "L", fill = 0)
                                
                self.pdf.multi_cell(w=5, h= 8, border= "R",
                        align= "C", fill = 0)
                
                self.pdf.multi_cell(w=190, h= 8,border= "LBR",
                        align= "J", fill = 0)

        #Cuarta prueba temperatura 100ºC a 100 mm
        if resultado4:
                self.pdf.set_font('Arial', '', 12) 
                self.pdf.cell(w=5, h= 8,border= "L",
                        align= "C", fill = 0)
                self.pdf.cell(w=90, h= 8,border= 0, txt= "Temperatura del ensayo: 100 ºC(+-2ºC)",
                        align= "C", fill = 0)
                self.pdf.cell(w=90, h= 8,border= 0, txt= "Celda 100 mm de lado",
                        align= "C", fill = 0)
                self.pdf.multi_cell(w=5, h= 8, border= "R",
                        align= "C", fill = 0)
                
                self.pdf.cell(w=5, h= 8,border= "L",
                        align= "C", fill = 0)
                self.pdf.cell(w=180, h= 8,border= 0, txt= "¿Tras 24h, supera los 160ºC?",
                        align= "L", fill = 0)
                self.pdf.multi_cell(w=5, h= 8, border= "R",
                        align= "C", fill = 0)

                self.pdf.cell(w=5, h= 8, border= "L",
                        align= "C", fill = 0)
                
                if int(resultado4.tMax) >= 200:
                        self.pdf.cell(w=180, h= 8,border= 0, txt= f"La muestra supera los 160ºC, siendo la temperatura máxima alcanzada de {resultado4.tMax} ºC",
                                align= "L", fill = 0)
                else:
                        self.pdf.cell(w=180, h= 8,border= 0, txt= f"La muestra no supera los 160ºC, siendo la temperatura máxima alcanzada de {resultado4.tMax} ºC",
                                        align= "L", fill = 0)
                                
                self.pdf.multi_cell(w=5, h= 8, border= "R",
                        align= "C", fill = 0)
                
                self.pdf.multi_cell(w=190, h= 8,border= "LBR",
                        align= "J", fill = 0)
        

                


        #Celda con Resultados
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LTR", txt= "RESULTADOS",
                align= "J", fill = 0)
        
        self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= f"Clasificación: {ensayo.get_resultado_display()}",
                align= "J", fill = 0)
        
        self.pdf.multi_cell(w=190, h= 8,border= "LR",
                        align= "J", fill = 0)
             
        #Firma
        self.pdf.set_font('Arial', '', 14) 
        self.pdf.cell(w=95, h= 8,border= 1, txt= f"Conforme:",
                align= "J", fill = 0)
        self.pdf.multi_cell(w=95, h= 8,border= 1, txt= f"Realizado: {ensayo.usuario.firmas.firma}",###
                align= "J", fill = 0)
        
        # Agregar más contenido dinámico aquí...
        return self.pdf.output(dest='S').encode('latin1')  # Devuelve bytes


    def N2(self):
        ensayo= N2.objects.get(muestra= self.muestra)
        equipos=ensayo.equipos.all()
        resultados= ResultadosN2.objects.filter(ensayo= ensayo).order_by("id")
        ensayoForma= self.descripcion.get_formaEnsayo_display()
        fechaInicio= ensayo.fechaInicio
        fechaFin= ensayo.fechaFin

        self.pdf = FPDF(orientation = 'P', unit= 'mm', format = 'A4')
        self.pdf.add_page()
        #TEXTO 
        self.pdf.set_font('Arial', '', 12)
        #IMAGEN
        image_path = os.path.join(self.rutaAbsoluta, 'Imagenes', 'LOGO.png')
        self.pdf.image(image_path, x=8, y=8, w=30, h=30, link="http://www.lom.upm.es", type='PNG')
        #Celdas Cabecera
        self.pdf.cell(w=35, h= 12,border= 0,
                align= "C", fill = 0)
        self.pdf.set_font('Arial', '', 11)
        self.pdf.cell(w= 100, h= 12, txt = f'{ensayo.ensayo.ensayo} ({ensayo.ensayo.normativa})', border= 1, 
                align= "C", fill = 0)
        self.pdf.set_font('Arial', '', 12)
        if fechaInicio!= fechaFin:
            self.pdf.multi_cell(w=0, h= 12, txt = f"Fecha Inicio: {fechaInicio.strftime('%d/%m/%Y')}", border= "RT", 
                    align= "L", fill = 0)
        else:
            self.pdf.multi_cell(w=0, h= 12, txt = "Fecha:", border= "RT", 
                align= "L", fill = 0)

        self.pdf.cell(w=35, h= 12,border= 0,
                align= "C", fill = 0)
        self.pdf.cell(w=100, h= 12, txt = f'Nº Expediente: {ensayo.muestra.expediente.expediente}',border= "LRB", 
                align= "C", fill = 0)
        if fechaInicio == fechaFin:
            self.pdf.multi_cell(w=0, h= 12, txt = fechaInicio.strftime("%d/%m/%Y"), border= "RB", 
                    align= "C", fill = 0)
        else:
              self.pdf.multi_cell(w=0, h= 12, txt = f'Fecha fin: {fechaFin.strftime("%d/%m/%Y")} ', border= "RB", 
                    align= "L", fill = 0)

        #Celda I/D muestra
        self.pdf.multi_cell(w=0, h= 5,border= 0,
                align= "C", fill = 0)
        self.pdf.cell(w=130, h= 8,border= 0, txt= f"Material: {self.descripcion.id_fabricante}",
                align= "J", fill = 0)
        self.pdf.multi_cell(w=60, h= 8,border= 0, txt= f"Identificación: {self.identificacion}",
                align= "J", fill = 0)

        #Celda Tratamiento de muestras  
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.cell(w=65, h= 8,border= "LT", txt= "MUESTRA DE POLVO",
                align= "J", fill = 0)

        self.pdf.set_font('Arial', '', 12)    
        self.pdf.multi_cell(w=125, h= 8,border= "TR", txt= f"La muestra se ensaya {ensayoForma}",
                align= "J", fill = 0)


        #Celda Condiciones ambientales  
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LRT", txt= "CONDICIONES AMBIENTALES",
                align= "J", fill = 0)

        self.pdf.set_font('Arial', '', 12)    
        self.pdf.cell(w=95, h= 8,border= "L", txt= f"Temperatura: {ensayo.temperaturaAmbiente} ºC",
                align= "C", fill = 0)

        self.pdf.multi_cell(w=95, h= 8,border= "R", txt= f"Humedad: {ensayo.humedad} %",
                align= "C", fill = 0)


        #Celda Equipos
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LRT", txt= "EQUIPOS DE ENSAYO",
                align= "J", fill = 0)
        self.pdf.set_font('Arial', '', 12)
        self.pdf.multi_cell(w=190, h= 8,border= "LBR", txt = "Equipos: " + " | ".join(equipo.codigo for equipo in equipos),###
                align= "J", fill = 0)


        #Celda Resultados
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= "PROCEDIEMIENTO",
                align= "J", fill = 0)
        

        self.pdf.multi_cell(w=190, h= 8,border= "LR",align= "L", 
                txt="El ensayo se realiza con un volumen de 2 ml, lanzando la muestra desde una altura de 1 m, se observa sI hay ignición en 5 min.",
                fill = 0)

        self.pdf.multi_cell(w=190, h= 8,border= "RL", fill = 0)
        
        #Parámetros tabla
        self.pdf.cell(w=40, h= 16,border= "L", fill = 0)
        self.pdf.cell(w=55, h= 16,border= 1,align= "C", 
                txt= "Número prueba", fill = 0)
        self.pdf.cell(w=55, h= 16,border= 1,align= "C", 
                txt= "¿Ignición?", fill = 0)

        self.pdf.multi_cell(w=40, h= 16,border= "R", fill = 0)

        #Resultados tabla (Habría que incluir esto en una clase con las variables)
        num=0
        for fila in resultados:
            num= num+1
            self.pdf.cell(w=40, h= 8,border= "L", fill = 0)
            self.pdf.cell(w=55, h= 8,border= 1,align= "C",txt= str(num), 
                    fill = 0)
            self.pdf.cell(w=55, h= 8,border= 1,align= "C",txt= fila.get_resultado_display(),
                    fill = 0)

            self.pdf.multi_cell(w=40, h= 8,border= "R", fill = 0)
        
        #Si el ensayo se ha podido hacer

        self.pdf.multi_cell(w=190, h= 8,border= "RL", fill = 0)

        #Celda con Resultados
        self.pdf.multi_cell(w=190, h= 5,border= "LR", fill = 0)
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LRT", txt= "RESULTADOS",
                align= "J", fill = 0)
        
        self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= f"Clasificación: {ensayo.get_resultado_display()}",
                align= "J", fill = 0)
        
        self.pdf.multi_cell(w=190, h= 8,border= "LR",
                align= "J", fill = 0)
        
        
        
             
        #Firma
        self.pdf.set_font('Arial', '', 14) 
        self.pdf.cell(w=95, h= 8,border= 1, txt= f"Conforme:",
                align= "J", fill = 0)
        self.pdf.multi_cell(w=95, h= 8,border= 1, txt= f"Realizado: {ensayo.usuario.firmas.firma}",###
                align= "J", fill = 0)
        
        # Agregar más contenido dinámico aquí...
        return self.pdf.output(dest='S').encode('latin1')  # Devuelve bytes
    
    
    def N1(self):
        ensayo= N1.objects.get(muestra= self.muestra)
        equipos=ensayo.equipos.all()
        resultados= ResultadosN1.objects.filter(ensayo= ensayo).order_by("id")
        ensayoForma= self.descripcion.get_formaEnsayo_display()
        fechaInicio= ensayo.fechaInicio
        fechaFin= ensayo.fechaFin

        self.pdf = FPDF(orientation = 'P', unit= 'mm', format = 'A4')
        self.pdf.add_page()
        #TEXTO 
        self.pdf.set_font('Arial', '', 12)
        #IMAGEN
        image_path = os.path.join(self.rutaAbsoluta, 'Imagenes', 'LOGO.png')
        self.pdf.image(image_path, x=8, y=8, w=30, h=30, link="http://www.lom.upm.es", type='PNG')
        #Celdas Cabecera
        self.pdf.cell(w=35, h= 12,border= 0,
                align= "C", fill = 0)
        self.pdf.set_font('Arial', '', 11)
        self.pdf.cell(w= 100, h= 12, txt = f'{ensayo.ensayo.ensayo} ({ensayo.ensayo.normativa})', border= 1, 
                align= "C", fill = 0)
        self.pdf.set_font('Arial', '', 12)
        if fechaInicio!= fechaFin:
            self.pdf.multi_cell(w=0, h= 12, txt = f"Fecha Inicio: {fechaInicio.strftime('%d/%m/%Y')}", border= "RT", 
                    align= "L", fill = 0)
        else:
            self.pdf.multi_cell(w=0, h= 12, txt = "Fecha:", border= "RT", 
                align= "L", fill = 0)

        self.pdf.cell(w=35, h= 12,border= 0,
                align= "C", fill = 0)
        self.pdf.cell(w=100, h= 12, txt = f'Nº Expediente: {ensayo.muestra.expediente.expediente}',border= "LRB", 
                align= "C", fill = 0)
        if fechaInicio == fechaFin:
            self.pdf.multi_cell(w=0, h= 12, txt = fechaInicio.strftime("%d/%m/%Y"), border= "RB", 
                    align= "C", fill = 0)
        else:
              self.pdf.multi_cell(w=0, h= 12, txt = f'Fecha fin: {fechaFin.strftime("%d/%m/%Y")} ', border= "RB", 
                    align= "L", fill = 0)

        #Celda I/D muestra
        self.pdf.multi_cell(w=0, h= 5,border= 0,
                align= "C", fill = 0)
        self.pdf.cell(w=130, h= 8,border= 0, txt= f"Material: {self.descripcion.id_fabricante}",
                align= "J", fill = 0)
        self.pdf.multi_cell(w=60, h= 8,border= 0, txt= f"Identificación: {self.identificacion}",
                align= "J", fill = 0)

        #Celda Tratamiento de muestras  
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.cell(w=65, h= 8,border= "LT", txt= "MUESTRA DE POLVO",
                align= "J", fill = 0)

        self.pdf.set_font('Arial', '', 12)    
        self.pdf.multi_cell(w=125, h= 8,border= "TR", txt= f"La muestra se ensaya {ensayoForma}",
                align= "J", fill = 0)


        #Celda Condiciones ambientales  
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LRT", txt= "CONDICIONES AMBIENTALES",
                align= "J", fill = 0)

        self.pdf.set_font('Arial', '', 12)    
        self.pdf.cell(w=95, h= 8,border= "L", txt= f"Temperatura: {ensayo.temperaturaAmbiente} ºC",
                align= "C", fill = 0)

        self.pdf.multi_cell(w=95, h= 8,border= "R", txt= f"Humedad: {ensayo.humedad} %",
                align= "C", fill = 0)


        #Celda Equipos
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LRT", txt= "EQUIPOS DE ENSAYO",
                align= "J", fill = 0)
        self.pdf.set_font('Arial', '', 12)
        self.pdf.multi_cell(w=190, h= 8,border= "LBR", txt = "Equipos: " + " | ".join(equipo.codigo for equipo in equipos),###
                align= "J", fill = 0)


        #Celda Resultados
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= "PROCEDIEMIENTO",
                align= "J", fill = 0)
        
        self.pdf.set_font('Arial', '', 12) 
        preseleccion= None
        if ensayo.pruebaPreseleccion== "1":
              preseleccion= "Si, se realiza prueba de velocidad"
        else:
              preseleccion= "No, la muestra no se clasifica"

        if (ensayo.tipoPolvo == "1"): #Polvo no metálico
                self.pdf.multi_cell(w=190, h= 8,border= "LR",align= "L", 
                        txt=f"El polvo es de tipo no metálico, se le aplica una llama durante 2 min, ¿El tiempo de propagación de la llama a lo largo de los 200mm del reguero es <2min? {preseleccion}",
                        fill = 0
                )

                ancho1= 30
                ancho2= 40
        else:
                self.pdf.multi_cell(w=190, h= 8,border= "LR",align= "L", 
                        txt=f"El polvo es de tipo metálico, se le aplica una llama durante 5 min, ¿El tiempo de propagación de la llama a lo largo de los 200mm del reguero es <20min? {preseleccion}",
                        fill = 0
                )

                ancho1= 35
                ancho2= 60

        self.pdf.multi_cell(w=190, h= 8,border= "RL", fill = 0)
        if resultados:
                self.pdf.set_font('Arial', 'B', 12) 
                self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= "Prueba velocidad de combustión",
                        align= "C", fill = 0)
                self.pdf.set_font('Arial', '', 12)
                #Parámetros tabla
                self.pdf.cell(w=ancho1, h= 16,border= "L", fill = 0)
                self.pdf.cell(w=ancho2, h= 16,border= 1,align= "C", 
                        txt= "Número prueba", fill = 0)
                self.pdf.cell(w=ancho2, h= 16,border= 1,align= "C", 
                        txt= "Tiempo(s)", fill = 0)
                if (ensayo.tipoPolvo == "1"):
                        self.pdf.cell(w=50, h= 16,border= 1,align= "C", 
                                txt= "¿Rebasa zona húmeda?", fill = 0)

                self.pdf.multi_cell(w=ancho1, h= 16,border= "R", fill = 0)

                #Resultados tabla (Habría que incluir esto en una clase con las variables)
                num=0
                for fila in resultados:
                        if fila.zonaHumeda and fila.zonaHumeda != "0":
                                resultadoZonaHumeda= fila.get_zonaHumeda_display()
                        else:
                                resultadoZonaHumeda= "-"
                                
                        if str(fila.tiempo) == "None":
                            tiempo= "-"
                            
                        else: 
                            tiempo= str(fila.tiempo)


                        num= num+1
                        self.pdf.cell(w=ancho1, h= 8,border= "L", fill = 0)
                        self.pdf.cell(w=ancho2, h= 8,border= 1,align= "C",txt= str(num), 
                                fill = 0)
                        
                        
                        self.pdf.cell(w=ancho2, h= 8,border= 1,align= "C",txt= str(tiempo),
                                fill = 0)
                        
                        if (ensayo.tipoPolvo == "1"):
                                self.pdf.cell(w=50, h= 8,border= 1,align= "C",txt= resultadoZonaHumeda,
                                        fill = 0)

                        self.pdf.multi_cell(w=ancho1, h= 8,border= "R", fill = 0)
        
        #Si el ensayo se ha podido hacer

        self.pdf.multi_cell(w=190, h= 8,border= "RL", fill = 0)

        #Celda con Resultados
        self.pdf.multi_cell(w=190, h= 5,border= "LR", fill = 0)
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LRT", txt= "RESULTADOS",
                align= "J", fill = 0)
        
        self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= f"Clasificación: {ensayo.get_resultado_display()}",
                align= "J", fill = 0)
        
        self.pdf.multi_cell(w=190, h= 8,border= "LR",
                align= "J", fill = 0)
        
        
        
             
        #Firma
        self.pdf.set_font('Arial', '', 14) 
        self.pdf.cell(w=95, h= 8,border= 1, txt= f"Conforme:",
                align= "J", fill = 0)
        self.pdf.multi_cell(w=95, h= 8,border= 1, txt= f"Realizado: {ensayo.usuario.firmas.firma}",###
                align= "J", fill = 0)
        
        # Agregar más contenido dinámico aquí...
        return self.pdf.output(dest='S').encode('latin1')  # Devuelve bytes
    

    def O1(self):
        ensayo= O1.objects.get(muestra= self.muestra)
        equipos=ensayo.equipos.all()
        resultados= ResultadosO1.objects.filter(ensayo= ensayo).order_by("id")
        ensayoForma= self.descripcion.get_formaEnsayo_display()
        fechaInicio= ensayo.fechaInicio
        fechaFin= ensayo.fechaFin

        self.pdf = FPDF(orientation = 'P', unit= 'mm', format = 'A4')
        self.pdf.add_page()
        #TEXTO 
        self.pdf.set_font('Arial', '', 12)
        #IMAGEN
        image_path = os.path.join(self.rutaAbsoluta, 'Imagenes', 'LOGO.png')
        self.pdf.image(image_path, x=8, y=8, w=30, h=30, link="http://www.lom.upm.es", type='PNG')
        #Celdas Cabecera
        self.pdf.cell(w=35, h= 12,border= 0,
                align= "C", fill = 0)
        self.pdf.set_font('Arial', '', 11)
        self.pdf.cell(w= 100, h= 12, txt = f'{ensayo.ensayo.ensayo} ({ensayo.ensayo.normativa})', border= 1, 
                align= "C", fill = 0)
        self.pdf.set_font('Arial', '', 12)
        if fechaInicio!= fechaFin:
            self.pdf.multi_cell(w=0, h= 12, txt = f"Fecha Inicio: {fechaInicio.strftime('%d/%m/%Y')}", border= "RT", 
                    align= "L", fill = 0)
        else:
            self.pdf.multi_cell(w=0, h= 12, txt = "Fecha:", border= "RT", 
                align= "L", fill = 0)

        self.pdf.cell(w=35, h= 12,border= 0,
                align= "C", fill = 0)
        self.pdf.cell(w=100, h= 12, txt = f'Nº Expediente: {ensayo.muestra.expediente.expediente}',border= "LRB", 
                align= "C", fill = 0)
        if fechaInicio == fechaFin:
            self.pdf.multi_cell(w=0, h= 12, txt = fechaInicio.strftime("%d/%m/%Y"), border= "RB", 
                    align= "C", fill = 0)
        else:
              self.pdf.multi_cell(w=0, h= 12, txt = f'Fecha fin: {fechaFin.strftime("%d/%m/%Y")} ', border= "RB", 
                    align= "L", fill = 0)

        #Celda I/D muestra
        self.pdf.multi_cell(w=0, h= 5,border= 0,
                align= "C", fill = 0)
        self.pdf.cell(w=130, h= 8,border= 0, txt= f"Material: {self.descripcion.id_fabricante}",
                align= "J", fill = 0)
        self.pdf.multi_cell(w=60, h= 8,border= 0, txt= f"Identificación: {self.identificacion}",
                align= "J", fill = 0)

        #Celda Tratamiento de muestras  
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.cell(w=65, h= 8,border= "LT", txt= "MUESTRA DE POLVO",
                align= "J", fill = 0)

        self.pdf.set_font('Arial', '', 12)    
        self.pdf.multi_cell(w=125, h= 8,border= "TR", txt= f"La muestra se ensaya {ensayoForma}",
                align= "J", fill = 0)


        #Celda Condiciones ambientales  
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LRT", txt= "CONDICIONES AMBIENTALES",
                align= "J", fill = 0)

        self.pdf.set_font('Arial', '', 12)    
        self.pdf.cell(w=95, h= 8,border= "L", txt= f"Temperatura: {ensayo.temperaturaAmbiente} ºC",
                align= "C", fill = 0)

        self.pdf.multi_cell(w=95, h= 8,border= "R", txt= f"Humedad: {ensayo.humedad} %",
                align= "C", fill = 0)


        #Celda Equipos
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LRT", txt= "EQUIPOS DE ENSAYO",
                align= "J", fill = 0)
        self.pdf.set_font('Arial', '', 12)
        self.pdf.multi_cell(w=190, h= 8,border= "LBR", txt = "Equipos: " + " | ".join(equipo.codigo for equipo in equipos),###
                align= "J", fill = 0)


        #Celda Resultados muestra referencia
        self.pdf.multi_cell(w=190, h= 8,border= "RL", fill = 0)
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= "ENSAYO REFERENCIA",
                align= "J", fill = 0)
        self.pdf.set_font('Arial', '', 12) 
        for resultado in resultados:
            if resultado.proporcion == "1":
                self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= f"Mezcla 30 g [30 % bromato potásico / 70 % celulosa]",
                        align= "J", fill = 0)
                self.pdf.cell(w=10, h= 8,border= "L")
                self.pdf.cell(w=25, h= 8,border= "", txt=f"T1: {resultado.tiempo1} s")
                self.pdf.cell(w=25, h= 8,border= "", txt=f"T2: {resultado.tiempo2} s")
                self.pdf.cell(w=25, h= 8,border= "", txt=f"T3: {resultado.tiempo3} s")
                self.pdf.cell(w=25, h= 8,border= "", txt=f"T4: {resultado.tiempo4} s")
                self.pdf.cell(w=25, h= 8,border= "", txt=f"T5: {resultado.tiempo5} s")
                self.pdf.cell(w=45, h= 8,border= "", align="R", txt=f"T7-3: {resultado.resultado} s")
                self.pdf.multi_cell(w=10, h= 8,border= "R")

            if resultado.proporcion == "2":
                self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= f"Mezcla 30 g [60 % bromato potásico / 40 % celulosa]",
                        align= "J", fill = 0)
                self.pdf.cell(w=10, h= 8,border= "L")
                self.pdf.cell(w=25, h= 8,border= "", txt=f"T1: {resultado.tiempo1} s")
                self.pdf.cell(w=25, h= 8,border= "", txt=f"T2: {resultado.tiempo2} s")
                self.pdf.cell(w=25, h= 8,border= "", txt=f"T3: {resultado.tiempo3} s")
                self.pdf.cell(w=25, h= 8,border= "", txt=f"T4: {resultado.tiempo4} s")
                self.pdf.cell(w=25, h= 8,border= "", txt=f"T5: {resultado.tiempo5} s")
                self.pdf.cell(w=45, h= 8,border= "", align="R", txt=f"T6-4: {resultado.resultado} s")
                self.pdf.multi_cell(w=10, h= 8,border= "R")
            if resultado.proporcion == "3":
                self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= f"Mezcla 30 g [40 % bromato potásico / 60 % celulosa]",
                        align= "J", fill = 0)
                self.pdf.cell(w=10, h= 8,border= "L")
                self.pdf.cell(w=25, h= 8,border= "", txt=f"T1: {resultado.tiempo1} s")
                self.pdf.cell(w=25, h= 8,border= "", txt=f"T2: {resultado.tiempo2} s")
                self.pdf.cell(w=25, h= 8,border= "", txt=f"T3: {resultado.tiempo3} s")
                self.pdf.cell(w=25, h= 8,border= "", txt=f"T4: {resultado.tiempo4} s")
                self.pdf.cell(w=25, h= 8,border= "", txt=f"T5: {resultado.tiempo5} s")
                self.pdf.cell(w=45, h= 8,border= "", align="R", txt=f"T4-6: {resultado.resultado} s")
                self.pdf.multi_cell(w=10, h= 8,border= "R")
        self.pdf.multi_cell(w=190, h= 8,border= "RL", fill = 0)
        
        #Celda Resultados muestra problema
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= "ENSAYO MUESTRA PROBLEMA",
                align= "J", fill = 0)
        self.pdf.set_font('Arial', '', 12) 
        for resultado in resultados:
            if resultado.proporcion == "4":
                self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= f"Mezcla 30 g [50 % muestra problema / 50 % celulosa]",
                        align= "J", fill = 0)
                self.pdf.cell(w=10, h= 8,border= "L")
                self.pdf.cell(w=25, h= 8,border= "", txt=f"T1: {resultado.tiempo1} s")
                self.pdf.cell(w=25, h= 8,border= "", txt=f"T2: {resultado.tiempo2} s")
                self.pdf.cell(w=25, h= 8,border= "", txt=f"T3: {resultado.tiempo3} s")
                self.pdf.cell(w=25, h= 8,border= "", txt=f"T4: {resultado.tiempo4} s")
                self.pdf.cell(w=25, h= 8,border= "", txt=f"T5: {resultado.tiempo5} s")
                self.pdf.cell(w=45, h= 8,border= "", align="R", txt=f"T5-5: {resultado.resultado} s")
                self.pdf.multi_cell(w=10, h= 8,border= "R")
            if resultado.proporcion == "5":
                self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= f"Mezcla 30 g [80 %  muestra problema / 20 % celulosa]",
                        align= "J", fill = 0)
                self.pdf.cell(w=10, h= 8,border= "L")
                self.pdf.cell(w=25, h= 8,border= "", txt=f"T1: {resultado.tiempo1} s")
                self.pdf.cell(w=25, h= 8,border= "", txt=f"T2: {resultado.tiempo2} s")
                self.pdf.cell(w=25, h= 8,border= "", txt=f"T3: {resultado.tiempo3} s")
                self.pdf.cell(w=25, h= 8,border= "", txt=f"T4: {resultado.tiempo4} s")
                self.pdf.cell(w=25, h= 8,border= "", txt=f"T5: {resultado.tiempo5} s")
                self.pdf.cell(w=45, h= 8,border= "", align="R", txt=f"T8-2: {resultado.resultado} s") 
                self.pdf.multi_cell(w=10, h= 8,border= "R")
        
        
        self.pdf.set_font('Arial', '', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "RL", fill = 0)

        #Celda con Resultados
        self.pdf.multi_cell(w=190, h= 5,border= "LR", fill = 0)
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LRT", txt= "RESULTADOS",
                align= "J", fill = 0)
        
        self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= f"Clasificación: {ensayo.get_resultado_display()}",
                align= "J", fill = 0)
        
        self.pdf.multi_cell(w=190, h= 8,border= "LR",
                align= "J", fill = 0)
        
        
        
             
        #Firma
        self.pdf.set_font('Arial', '', 14) 
        self.pdf.cell(w=95, h= 8,border= 1, txt= f"Conforme:",
                align= "J", fill = 0)
        self.pdf.multi_cell(w=95, h= 8,border= 1, txt= f"Realizado: {ensayo.usuario.firmas.firma}",###
                align= "J", fill = 0)
        
        # Agregar más contenido dinámico aquí...
        return self.pdf.output(dest='S').encode('latin1')  # Devuelve bytes
    

    def tratamiento(self):
        ensayo= Tratamiento.objects.get(muestra= self.muestra)
        ensayoForma= self.descripcion.get_formaEnsayo_display()

        self.pdf = FPDF(orientation = 'P', unit= 'mm', format = 'A4')
        self.pdf.add_page()
        #TEXTO 
        self.pdf.set_font('Arial', '', 12)
        #IMAGEN
        image_path = os.path.join(self.rutaAbsoluta, 'Imagenes', 'LOGO.png')
        self.pdf.image(image_path, x=8, y=8, w=30, h=30, link="http://www.lom.upm.es", type='PNG')
        #Celdas Cabecera
        self.pdf.cell(w=35, h= 12,border= 0,
                align= "C", fill = 0)
        self.pdf.set_font('Arial', '', 11)
        self.pdf.cell(w= 100, h= 12, txt = f'{ensayo.ensayo.ensayo} ({ensayo.ensayo.normativa})', border= 1, 
                align= "C", fill = 0)
        self.pdf.set_font('Arial', '', 12)
        self.pdf.multi_cell(w=55, h= 12, txt = "Fecha:", border= "RT", 
                align= "L", fill = 0)

        self.pdf.cell(w=35, h= 12,border= 0,
                align= "C", fill = 0)
        self.pdf.cell(w=100, h= 12, txt = f'Nº Expediente: {ensayo.muestra.expediente.expediente}',border= "LRB", 
                align= "C", fill = 0)
        self.pdf.multi_cell(w=55, h= 12, border= "RB", 
                align= "C", fill = 0)

        #Celda I/D muestra
        self.pdf.multi_cell(w=0, h= 5,border= 0,
                align= "C", fill = 0)
        self.pdf.cell(w=130, h= 8,border= 0, txt= f"Material: {self.descripcion.id_fabricante}",
                align= "J", fill = 0)
        self.pdf.multi_cell(w=60, h= 8,border= 0, txt= f"Identificación: {self.identificacion}",
                align= "J", fill = 0)

        #Celda Secado 
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LRT", txt= "SECADO",
                align= "J", fill = 0)
        if ensayo.secado == "2":
            self.pdf.set_font('Arial', '', 12) 

            self.pdf.cell(w=10, h= 8, border="L")
            self.pdf.cell(w=85, h= 8,border= "", txt= f"Fecha inicio: {ensayo.fechaSecadoInicio}",
                    align= "J", fill = 0)
            self.pdf.cell(w=85, h= 8,border= "", txt= f"Fecha fin: {ensayo.fechaSecadoFin}",
                    align= "J", fill = 0)
            self.pdf.multi_cell(w=10, h= 8, border="R")

            self.pdf.cell(w=10, h= 8, border="L")
            self.pdf.cell(w=170, h= 8,border= "", txt= f"Estufa: {ensayo.equipoSecado.get().codigo}",
                    align= "J", fill = 0)
            self.pdf.multi_cell(w=10, h= 8, border="R")
            
            self.pdf.cell(w=10, h= 8, border="L")
            self.pdf.cell(w=85, h= 8,border= "", txt= f"Tiempo: {ensayo.tiempo} h")
            self.pdf.cell(w=85, h= 8,border= "", txt= f"temperatura: {ensayo.temperatura} ºC")
            self.pdf.multi_cell(w=10, h= 8, border="R")
            self.pdf.multi_cell(w=190, h= 8, border="LR")
        else:
            self.pdf.set_font('Arial', '', 12) 
            self.pdf.cell(w=10, h= 8, border="L")
            self.pdf.cell(w=170, h= 8,border= "", txt= f"No se ha realizado secado",
                    align= "J", fill = 0)
            self.pdf.multi_cell(w=10, h= 8, border="R")      
        #Celda Molido 
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LRT", txt= "MOLIDO",
                align= "J", fill = 0)
        
        if ensayo.molido == "2":
            self.pdf.set_font('Arial', '', 12) 
            self.pdf.cell(w=10, h= 8, border="L")
            self.pdf.cell(w=85, h= 8,border= "", txt= f"Fecha inicio: {ensayo.fechaMolidoInicio}",
                    align= "J", fill = 0)
            self.pdf.cell(w=85, h= 8,border= "", txt= f"Fecha fin: {ensayo.fechaMolidoFin}",
                    align= "J", fill = 0)
            self.pdf.multi_cell(w=10, h= 8, border="R")

            self.pdf.cell(w=10, h= 8, border="L")
            self.pdf.cell(w=170, h= 8,border= "", txt= f"Molino: {ensayo.equipoMolido.get().codigo}",
                    align= "J", fill = 0)
            self.pdf.multi_cell(w=10, h= 8, border="R")
            self.pdf.multi_cell(w=190, h= 8, border="LR")   
        else:
            self.pdf.set_font('Arial', '', 12) 
            self.pdf.cell(w=10, h= 8, border="L")
            self.pdf.cell(w=170, h= 8,border= "", txt= f"No se ha realizado Molienda",
                    align= "J", fill = 0)
            self.pdf.multi_cell(w=10, h= 8, border="R")
            
        #Celda Tamizado
        
        self.pdf.set_font('Arial', 'B', 12) 
        self.pdf.multi_cell(w=190, h= 8,border= "LRT", txt= "TAMIZADO",
                align= "J", fill = 0)
        if ensayo.tamizado == "2":
            self.pdf.set_font('Arial', '', 12) 
            self.pdf.cell(w=10, h= 8, border="L")
            self.pdf.cell(w=85, h= 8,border= "", txt= f"Fecha inicio: {ensayo.fechaMolidoInicio}",
                    align= "J", fill = 0)
            self.pdf.cell(w=85, h= 8,border= "", txt= f"Fecha fin: {ensayo.fechaMolidoFin}",
                    align= "J", fill = 0)
            self.pdf.multi_cell(w=10, h= 8, border="R")

            self.pdf.cell(w=10, h= 8, border="L")
            self.pdf.cell(w=170, h= 8,border= "", txt= f"Tamizado: {ensayo.equipoTamizado.get().equipo_padre.codigo} | {ensayo.equipoTamizado.get().codigo} | {ensayo.equipoTamizado.get().equipo}",
                    align= "J", fill = 0)
            self.pdf.multi_cell(w=10, h= 8, border="R")
            self.pdf.multi_cell(w=190, h= 8, border="LR")   
        else:
            self.pdf.set_font('Arial', '', 12) 
            self.pdf.cell(w=10, h= 8, border="L")
            self.pdf.cell(w=170, h= 8,border= "", txt= f"No se ha realizado tamizado",
                    align= "J", fill = 0)
            self.pdf.multi_cell(w=10, h= 8, border="R")

        
        
             
        #Firma
        self.pdf.set_font('Arial', '', 14) 
        self.pdf.cell(w=95, h= 8,border= 1, txt= f"Conforme:",
                align= "J", fill = 0)
        self.pdf.multi_cell(w=95, h= 8,border= 1, txt= f"Realizado: {ensayo.usuario.firmas.firma}",###
                align= "J", fill = 0)
        
        # Agregar más contenido dinámico aquí...
        return self.pdf.output(dest='S').encode('latin1')  # Devuelve bytes