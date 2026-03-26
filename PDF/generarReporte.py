from PDF.gestorPlantillas import InformePDF

class ReportGenerator():
    def __init__(self, periodo, usuario):
        self.periodo= periodo
        self.usuario= usuario

    def reporte(self):
        reporte= InformePDF(self.periodo, self.usuario)
        output= reporte.build()

        return output


