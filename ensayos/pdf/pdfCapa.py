"""#VARIABLES
nombreEnsayo = "TMIcapa (POENS 551)"
nombreNorma= "UNE-EN ISO/IEC 80079-20-2:2016"
material= "CARBAICAR"
identificacion= "ERC-15"
tratada= True
temperatura = "23"
humedad = "36"
equipos= ["PO0069", "PO0082", "PO0087"]
resultados = []
numeroFilas= 15
TI = 300"""

from fpdf import FPDF
from datetime import datetime as dia
import os

class pdfTMIc():
        def __init__(self,nombreEnsayo,nombreNorma,material,identificacion,tratada,temperatura, humedad, equipos, resultados,numeroFilas,operario):
                self.nombreEnsayo = nombreEnsayo
                self.nombreNorma= nombreNorma
                self.material= material
                self.identificacion= identificacion
                self.tratada= tratada
                self.temperatura = temperatura
                self.humedad = humedad
                self.equipos= equipos
                self.resultados = resultados
                self.numeroFilas=numeroFilas
                self.operario = operario
                self.TI = 300
                self.rutaAbsoluta = os.path.dirname(__file__)
   

    #Función tratamiento de muestra:
        def tratamiento(self):
                if self.tratada:
                        return ("tratada")
                else:
                        return ("s/recibida")

    #Función filas tabla resultado:
        def filastabla(self):
                for valor in self.resultados:
                        self.pdf.cell(w=5, h= 8,border= "L", fill = 0)
                        self.pdf.cell(w=36, h= 8,border= 1,align= "C",txt= valor[0], #Columna 1 Tª plato
                                fill = 0)
                        self.pdf.cell(w=36, h= 8,border= 1,align= "C",txt= valor[1], #columna 2 Tª Max
                                fill = 0)
                        self.pdf.cell(w=27, h= 8,border= 1,align= "C",txt= valor[2],
                                fill = 0)
                        self.pdf.cell(w=45, h= 8,border= 1, align= "C",txt= valor[3],
                                fill = 0)
                        self.pdf.cell(w=36, h= 8,border= 1, align= "C",txt= valor[4],
                                fill = 0)
                        self.pdf.multi_cell(w=5, h= 8,border= "R", fill = 0)

        def pdf(self):
                
                self.pdf = FPDF(orientation = 'P', unit= 'mm', format = 'A4')
                self.pdf.add_page()
                fechaActual= dia. today().strftime('%Y-%m-%d')
        
                #TEXTO 
                self.pdf.set_font('Arial', '', 12)
                #IMAGEN
                self.pdf.image(self.rutaAbsoluta + '/Imagenes/LOGO.png', x=8, y= 8, w=30, h=30, link="http://www.lom.upm.es")

                #Celdas Cabecera
                self.pdf.cell(w=35, h= 12,border= 0,
                        align= "C", fill = 0)
                self.pdf.cell(w= 100, h= 12, txt = self.nombreEnsayo,border= 1, 
                        align= "C", fill = 0)
                self.pdf.multi_cell(w=0, h= 12, txt = "Fecha:",border= "RT", 
                        align= "L", fill = 0)

                self.pdf.cell(w=35, h= 12,border= 0,
                        align= "C", fill = 0)
                self.pdf.cell(w=100, h= 12, txt = self.nombreNorma,border= "LRB", 
                        align= "C", fill = 0)
                self.pdf.multi_cell(w=0, h= 12, txt = fechaActual,border= "RB", 
                        align= "C", fill = 0)

                #Celda I/D muestra
                self.pdf.multi_cell(w=0, h= 5,border= 0,
                        align= "C", fill = 0)
                self.pdf.cell(w=130, h= 8,border= 0, txt= f"Material: {self.material}",
                        align= "J", fill = 0)
                self.pdf.multi_cell(w=60, h= 8,border= 0, txt= f"Identificación: {self.identificacion}",
                        align= "J", fill = 0)

                #Celda Tratamiento de muestras  
                self.pdf.set_font('Arial', 'B', 12) 
                self.pdf.cell(w=65, h= 8,border= "LT", txt= "MUESTRA DE POLVO",
                        align= "J", fill = 0)

                self.pdf.set_font('Arial', '', 12)    
                self.pdf.multi_cell(w=125, h= 8,border= "TR", txt= f"La muestra se ensaya {self.tratamiento()}",
                        align= "J", fill = 0)


                #Celda Condiciones ambientales  
                self.pdf.set_font('Arial', 'B', 12) 
                self.pdf.multi_cell(w=190, h= 8,border= "LRT", txt= "CONDICIONES AMBIENTALES",
                        align= "J", fill = 0)

                self.pdf.set_font('Arial', '', 12)    
                self.pdf.cell(w=95, h= 8,border= "L", txt= f"Temperatura: {self.temperatura} ºC",
                        align= "C", fill = 0)

                self.pdf.multi_cell(w=95, h= 8,border= "R", txt= f"Humedad: {self.humedad} %",
                        align= "C", fill = 0)


                #Celda Equipos
                self.pdf.set_font('Arial', 'B', 12) 
                self.pdf.multi_cell(w=190, h= 8,border= "LRT", txt= "EQUIPOS DE ENSAYO",
                        align= "J", fill = 0)
                self.pdf.set_font('Arial', '', 12)
                self.pdf.cell(w=63, h= 8,border= "LB", txt= f"Registrador de Tª: {self.equipos[0]}",
                        align= "J", fill = 0)
                self.pdf.cell(w=63, h= 8,border= "B", txt= f"Cronometro: {self.equipos[1]}",
                        align= "C", fill = 0)
                self.pdf.multi_cell(w=64, h= 8,border= "BR", txt= f"Termohigrómetro: {self.equipos[2]}",
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
                self.pdf.cell(w=36, h= 8,border= 1,align= "C", 
                        txt= "Tª Plato", fill = 0)
                self.pdf.cell(w=36, h= 8,border= 1,align= "C", 
                        txt= "Tª Max", fill = 0)
                self.pdf.cell(w=27, h= 8,border= 1,align= "C", 
                        txt= "¿Ignición?", fill = 0)
                self.pdf.cell(w=45, h= 8,border= 1, align= "C",
                        txt= "Visual/termopar", fill = 0)
                self.pdf.cell(w=36, h= 8,border= 1, align= "C",
                        txt= "Tiempo", fill = 0)

                self.pdf.multi_cell(w=5, h= 8,border= "R", fill = 0)

                #Resultados tabla (Habría que incluir esto en una clase con las variables)
                self.filastabla()

                
                #Cálculos resultados
                if int(self.resultados[len(self.resultados)-1][0]) >= 400:
                        self.TI= ">400"
                else:
                        self.TI= int(self.resultados[len(self.resultados)-1][0])
                        

                #Celda con Resultados
                self.pdf.multi_cell(w=190, h= 5,border= "LR", fill = 0)
                self.pdf.set_font('Arial', 'B', 12) 
                self.pdf.multi_cell(w=190, h= 8,border= "LRT", txt= "RESULTADOS",
                        align= "J", fill = 0)
                self.pdf.set_font('Arial', '', 12) 
                self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= f"Menor temperatura a la que se produce ignición:     {str(self.TI)} ºC* ",
                        align= "J", fill = 0)
                if self.TI != ">400":
                        self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= f"Mayor temperatura a la que se produce ignición:     {str(self.TI+10)} ºC ",
                                align= "J", fill = 0)
                else:
                       self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= f"Mayor temperatura a la que se produce ignición:     N/D ",
                                align= "J", fill = 0) 
                self.pdf.multi_cell(w=190, h= 8,border= "LR", txt= f"*Se realiza la comprobación en tres ensayos adicionales",
                        align= "J", fill = 0)

                #Celda resultado final       
                self.pdf.set_font('Arial', 'B', 14) 
                self.pdf.multi_cell(w=190, h= 8,border= 1, txt= f"TEMPERATURA MÍNIMA DE IGNICIÓN EN CAPA:     {str(self.TI)} ºC ",
                        align= "C", fill = 0)
                #Firma
                self.pdf.set_font('Arial', '', 14) 
                self.pdf.cell(w=95, h= 8,border= 1, txt= f"Conforme:",
                        align= "J", fill = 0)
                self.pdf.multi_cell(w=95, h= 8,border= 1, txt= f"Realizado: {self.operario}",
                        align= "J", fill = 0)
                try:
                        self.pdf.output(self.rutaAbsoluta + f"/Archivos/{self.identificacion} {fechaActual} CAPA .pdf")
                except:
                        (print ("El archivo ya existe"))

#archivo=pdfTMIc("TMIcapa (POENS 551)","UNE-EN ISO/IEC 80079-20-2:2016","CARBAICAR","ERC-15",True,"93","36",["PO0069", "PO0082", "PO0087"],0,10)
#archivo.pdf()