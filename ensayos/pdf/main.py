import pdfCapa

#VARIABLES
nombreEnsayo = "TMIcapa (POENS 551)"
nombreNorma= "UNE-EN ISO/IEC 80079-20-2:2016"
material= "Polvo de aluminio"
identificacion= "POL-1"
tratada= True
temperatura = "23"
humedad = "62"
equipos= ["PO0069", "PO0082", "PO0087"]
resultados = [["240","<240","NO","","33"],["300","<240","NO","","33"],["320","<240","NO","","33"],["360","<240","NO","","33"],["390","<240","SI","","33"],["380","<240","SI","","33"],["370","<240","NO","","33"],["370","<240","NO","","33"],["370","<240","NO","","33"],["350","<240","NO","","33"]]
operario= "SBS"
TI = 300
numeroFilas= len(resultados)

crearPdf= pdfCapa.pdfTMIc(nombreEnsayo,nombreNorma,material,identificacion,tratada,temperatura,humedad,equipos,resultados,numeroFilas,operario,)
crearPdf.pdf()
