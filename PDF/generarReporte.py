from PDF.plantillaReporte import InformePDF

class ReportGenerator():
    def __init__(self, periodo):
        self.periodo= periodo

    def reporte(self):
        reporte= InformePDF(self.periodo)
        output= reporte.build()

        return output


