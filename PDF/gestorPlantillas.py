
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import os
import unicodedata
from playwright.sync_api import sync_playwright
from jinja2 import Environment, FileSystemLoader
import os
import tempfile
from polvosLom import settings
import webbrowser
from django.utils import timezone
from django.db.models import Count, Q, F, ExpressionWrapper, FloatField
import json
from django.db.models import Sum

from expedientes.models import Empresa, Expedientes
from muestras.models import Muestras
from django.db.models.functions import ExtractMonth
from ensayos.models import *





class InformePDF:

    def __init__(self, periodo, usuario):
        self.periodo = periodo
        self.usuario = usuario
        self.ruta = os.path.dirname(__file__)

    def build(self):

        env = Environment(
            loader=FileSystemLoader(self.ruta)
        )

        ########### Rutas ###########
        template = env.get_template("plantillaReporte.html")
        bootstrap_css = "file:///" + os.path.join(self.ruta, "static", "css", "bootstrap.min.css").replace("\\", "/")
        bootstrap_js = "file:///" + os.path.join(self.ruta, "static", "js", "bootstrap.bundle.min.js").replace("\\", "/")
        chart_pie_js= "file:///" + os.path.join(self.ruta, "static", "js", "chart-pie-demo.js").replace("\\", "/")

        bar_chart_js= "file:///" + os.path.join(self.ruta, "static", "js", "barChart.js").replace("\\", "/")

        line_chart_js= "file:///" + os.path.join(self.ruta, "static", "js", "lineChart.js").replace("\\", "/")

        icons= "file:///" + os.path.join(self.ruta, "static", "icons", "bootstrap-icons.css").replace("\\", "/")


        Chart= "file:///" + os.path.join(self.ruta, "static", "js", "Chart.js").replace("\\", "/")

        mapa= os.path.join(self.ruta, "static", "js", "spain-provinces.geojson")

        donut="file:///" + os.path.join(self.ruta, "static", "js", "donutChart.js").replace("\\", "/")
        empresasChar= "file:///" + os.path.join(self.ruta, "static", "js", "empresasChar.js").replace("\\", "/")


        ########### Variables ###########
        #Fecha actual
        año_actual = timezone.now().year
        top_empresas = Empresa.objects.filter(
                muestras__fecha__year=año_actual
            ).annotate(
                total_muestras=Count('muestras')
            ).order_by('-total_muestras')[:5]
        
        #Empresas
        empresasTop= []
        colores= ["primary", "success", "info", "secondary", "warning"]
        bucle= 0
        for empresa in top_empresas:
            empresasTop.append({'empresa': empresa.empresa, 'nMuestras': empresa.total_muestras, 'color': colores[bucle]})
            bucle = bucle + 1
        
        top_empresas_json= json.dumps(empresasTop)

        #Mapa
        with open(mapa, encoding="utf-8") as f:
            mapa = json.load(f)
        mapa = json.dumps(mapa)

        ########### Genaración de variables #######
        year= int(self.periodo[0])
        yearAnterior= year -1
        datos= GeneradorVariables(year)

        datosEvolucion= datos.evolucionGeneral()
        datosEvolucion_json= json.dumps(datosEvolucion)

        muestrasMensual=datos.muestrasMensual()
        expedientesMensual= datos.expedientesMensual()

        muestrasMensual_json= json.dumps(muestrasMensual)
        expedientesMensual_json= json.dumps(expedientesMensual)

        promedioMensual = {
            "promedioMuestras": round(int(datosEvolucion["muestras"]) / 12, 1),
            "promedioExpedientes": round(int(datosEvolucion["expedientes"]) / 12, 1),
            "empresasNuevas": datos.empresasNuevas(),
        }

        comparativaAnual= datos.comparativaAnual()
        comparativaAnual_json= json.dumps(comparativaAnual)

        year_json= json.dumps(year)
        yearAnterior_json= json.dumps(yearAnterior)

        calculosComparativa= datos.calculosComparativa()

        calculosEnsayos= datos.calculosEnsayos()
        calculosEnsayos_json= json.dumps(calculosEnsayos)




        ########### Render template ###########
        html = template.render(
            periodo=self.periodo,
            usuario_nombre=self.usuario.first_name,
            usuario_apellido=self.usuario.last_name,
            # 👇 usa esto en debug (mejor con Django static si puedes)
            logo_path="file:///" + os.path.join(self.ruta, "Imagenes", "LOGO.png").replace("\\", "/"),
            bootstrap_css=bootstrap_css,
            bootstrap_js=bootstrap_js,
            chart_pie_js= chart_pie_js,
            icons=icons,
            Chart=Chart,
            bar_chart_js=bar_chart_js,
            line_chart_js=line_chart_js,
            top_empresas= top_empresas,
            top_empresas_json= top_empresas_json,
            mapa=mapa,
            donut=donut,
            empresasChar=empresasChar,
            promedioMensual= promedioMensual,
            

            #Variables
            year= year,
            year_json= year_json,
            yearAnterior= yearAnterior,
            yearAnterior_json= yearAnterior_json,
            datosEvolucion=datosEvolucion,
            datosEvolucion_json= datosEvolucion_json,

            muestrasMensual= muestrasMensual_json,
            expedientesMensual= expedientesMensual_json,
            comparativaAnual= comparativaAnual_json,
            calculosComparativa= calculosComparativa,
            calculosEnsayos= calculosEnsayos,
            calculosEnsayos_json= calculosEnsayos_json,

        )

        # =========================
        # 🧪 MODO DEBUG
        # =========================
        prueba= True
        if prueba:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as f:
                f.write(html.encode("utf-8"))
                temp_path = f.name

            print("🧪 Debug HTML:", temp_path)

            # 👇 abre automáticamente en navegador
            webbrowser.open(f"file://{temp_path}")

            return None  # no genera PDF

        # =========================
        # 📄 MODO PRODUCCIÓN
        # =========================
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage"]
            )

            page = browser.new_page()

            # usar archivo temporal (clave para imágenes)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as f:
                f.write(html.encode("utf-8"))
                temp_path = f.name

            page.goto(f"file://{temp_path}")
            page.wait_for_load_state("networkidle")
            page.wait_for_function("window.chartRendered === true")

            # Forzar viewport exacto A4 en píxeles (96dpi)
            page.set_viewport_size({"width": 794, "height": 1123})

            pdf = page.pdf(
                format="A4",
                print_background=True,
                margin={
                    "top": "0mm",
                    "bottom": "0mm",
                    "left": "0mm",
                    "right": "0mm"
                }
            )

            browser.close()

        return pdf


class GeneradorVariables:
    def __init__(self, year):
        self.year = year

    def evolucionGeneral(self):
        # Número total de muestras del año
        nMuestras = Muestras.objects.filter(
            fecha__year=self.year
        ).count()

        nExpedientes = Expedientes.objects.filter(
            fecha__year=self.year
        ).count()

        nEmpresas = Expedientes.objects.filter(
            fecha__year=self.year
        ).values('empresa').distinct().count()

        return {
            "muestras": nMuestras,
            "expedientes": nExpedientes,
            "empresas": nEmpresas
        }
        
    
    def muestrasMensual(self):
        #Número de muestras realizadas por mes
        # Agrupar por mes y contar
        muestras_por_mes_qs = (
            Muestras.objects
                .filter(fecha__year=self.year)
                .annotate(mes=ExtractMonth('fecha'))
                .values('mes')
                .annotate(total=Count('id'))
                .order_by('mes')
            )

        muestras_por_mes_dict= {mes:0 for mes in range(1,13)}

        for item in muestras_por_mes_qs:
            muestras_por_mes_dict[item['mes']]= item['total']

        muestrasPorMes = [muestras_por_mes_dict[mes] for mes in range(1, 13)]

        return muestrasPorMes
    

    def expedientesMensual(self):
        #Número de muestras realizadas por mes
        # Agrupar por mes y contar
        expedientes_por_mes_qs = (
            Expedientes.objects
                .filter(fecha__year=self.year)
                .annotate(mes=ExtractMonth('fecha'))
                .values('mes')
                .annotate(total=Count('id'))
                .order_by('mes')
            )

        expedientes_por_mes_dict= {mes:0 for mes in range(1,13)}

        for item in expedientes_por_mes_qs:
            expedientes_por_mes_dict[item['mes']]= item['total']

        expedientesPorMes = [expedientes_por_mes_dict[mes] for mes in range(1, 13)]

        return expedientesPorMes


    def empresasNuevas (self):
        empresasNuevas = (
            Muestras.objects
            .filter(
                id_muestra=1,
                fecha__year=self.year
            )
            .values('empresa')
            .distinct()
            .count()
        )
        
        return empresasNuevas
    

    def comparativaAnual (self):
        yearAnterior= self.year - 1
        
        nMuestrasAnterior = Muestras.objects.filter(
            fecha__year=yearAnterior
        ).count()

        nExpedientesAnterior = Expedientes.objects.filter(
            fecha__year=yearAnterior
        ).count()

        nEmpresasAnterior = Expedientes.objects.filter(
            fecha__year=yearAnterior
        ).values('empresa').distinct().count()

        return {
            "muestras": nMuestrasAnterior,
            "expedientes": nExpedientesAnterior,
            "empresas": nEmpresasAnterior
        }


    def calculosComparativa (self):
        evolucion = self.evolucionGeneral()
        comparativa = self.comparativaAnual()

        muestras_actual = evolucion['muestras']
        muestras_anterior = comparativa['muestras']

        expedientes_actual = evolucion['expedientes']
        expedientes_anterior = comparativa['expedientes']

        empresas_actual = evolucion['empresas']
        empresas_anterior = comparativa['empresas']


        incrementoMuestras = (
            (muestras_actual - muestras_anterior)
            / muestras_anterior
        ) * 100

        incrementoExpedientes = (
            (expedientes_actual - expedientes_anterior)
            / expedientes_anterior
        ) * 100

        incrementoEmpresas = (
            (empresas_actual - empresas_anterior)
            / empresas_anterior
        ) * 100


        incrementoMuestras = f"{incrementoMuestras:+.1f}%"
        incrementoExpedientes = f"{incrementoExpedientes:+.1f}%"
        incrementoEmpresas = f"{incrementoEmpresas:+.1f}%"


        return {
            "incrementoMuestras": incrementoMuestras,
            "incrementoExpedientes": incrementoExpedientes,
            "incrementoEmpresas": incrementoEmpresas,
        }


    def calculosEnsayos(self):

        colors = [
            '#1E3A8A',
            '#2563EB',
            '#3B82F6',
            '#60A5FA',
            '#93C5FD',
            '#2E95AA',
            '#14B8A6',
            '#22C55E',
            '#84CC16',
            '#F59E0B',
            '#EF4444'
        ]

        # TMIC
        tmic = TMIc.objects.filter(fechaFin__year=self.year)
        nTmic = tmic.count()
        hTmic = float(tmic.aggregate(
            total=Sum('horasEnsayo')
        )['total'] or 0)
        normativa = ListaEnsayos.objects.get(ensayo="TMIc")
        normaTmic= normativa.normativa
                

        # TMIN
        tmin = TMIn.objects.filter(fechaFin__year=self.year)
        nTmin = tmin.count()
        hTmin = float(tmin.aggregate(
            total=Sum('horasEnsayo')
        )['total'] or 0)

        # EMI
        emi = EMI.objects.filter(fechaFin__year=self.year)
        nEmi = emi.count()
        hEmi = float(emi.aggregate(
            total=Sum('horasEnsayo')
        )['total'] or 0)

        # LIE
        lie = LIE.objects.filter(fechaFin__year=self.year)
        nLie = lie.count()
        hLie = float(lie.aggregate(
            total=Sum('horasEnsayo')
        )['total'] or 0)

        # PMAX
        pmax = Pmax.objects.filter(fechaFin__year=self.year)
        nPmax = pmax.count()
        hPmax = float(pmax.aggregate(
            total=Sum('horasEnsayo')
        )['total'] or 0)

        # CLO
        clo = CLO.objects.filter(fechaFin__year=self.year)
        nClo = clo.count()
        hClo = float(clo.aggregate(
            total=Sum('horasEnsayo')
        )['total'] or 0)

        # N1
        n1 = N1.objects.filter(fechaFin__year=self.year)
        nN1 = n1.count()
        hN1 = float(n1.aggregate(
            total=Sum('horasEnsayo')
        )['total'] or 0)

        # N2
        n2 = N2.objects.filter(fechaFin__year=self.year)
        nN2 = n2.count()
        hN2 = float(n2.aggregate(
            total=Sum('horasEnsayo')
        )['total'] or 0)

        # N4
        n4 = N4.objects.filter(fechaFin__year=self.year)
        nN4 = n4.count()
        hN4 = float(n4.aggregate(
            total=Sum('horasEnsayo')
        )['total'] or 0)

        # O1
        o1 = O1.objects.filter(fechaFin__year=self.year)
        nO1 = o1.count()
        hO1 = float(o1.aggregate(
            total=Sum('horasEnsayo')
        )['total'] or 0)

        # REC
        rec = REC.objects.filter(fechaFin__year=self.year)
        nRec = rec.count()
        hRec = float(rec.aggregate(
            total=Sum('horasEnsayo')
        )['total'] or 0)

        # Totales
        totalEnsayos = (
            nTmic + nTmin + nEmi + nLie + nPmax +
            nClo + nN1 + nN2 + nN4 + nO1 + nRec
        )

        totalHoras = (
            hTmic + hTmin + hEmi + hLie + hPmax +
            hClo + hN1 + hN2 + hN4 + hO1 + hRec
        )

        # Porcentajes
        if totalEnsayos > 0:
            pTmic = int(round((nTmic / totalEnsayos) * 100))
            pTmin = int(round((nTmin / totalEnsayos) * 100))
            pEmi = int(round((nEmi / totalEnsayos) * 100))
            pLie = int(round((nLie / totalEnsayos) * 100))
            pPmax = int(round((nPmax / totalEnsayos) * 100))
            pClo = int(round((nClo / totalEnsayos) * 100))
            pN1 = int(round((nN1 / totalEnsayos) * 100))
            pN2 = int(round((nN2 / totalEnsayos) * 100))
            pN4 = int(round((nN4 / totalEnsayos) * 100))
            pO1 = int(round((nO1 / totalEnsayos) * 100))
            pRec = int(round((nRec / totalEnsayos) * 100))
        else:
            pTmic = pTmin = pEmi = pLie = pPmax = 0
            pClo = pN1 = pN2 = pN4 = pO1 = pRec = 0

        # Lista ordenada
        ensayosOrdenados = [
            {
                "nombre": "TMIC",
                "ensayos": nTmic,
                "horas": int(round(hTmic, 0)),
                "porcentaje": pTmic,
                "color": colors[0]
            },
            {
                "nombre": "TMIN",
                "ensayos": nTmin,
                "horas": int(round(hTmin, 0)),
                "porcentaje": pTmin,
                "color": colors[1]
            },
            {
                "nombre": "EMI",
                "ensayos": nEmi,
                "horas": int(round(hEmi, 0)),
                "porcentaje": pEmi,
                "color": colors[2]
            },
            {
                "nombre": "LIE",
                "ensayos": nLie,
                "horas": int(round(hLie, 0)),
                "porcentaje": pLie,
                "color": colors[3]
            },
            {
                "nombre": "PMAX",
                "ensayos": nPmax,
                "horas": int(round(hPmax, 0)),
                "porcentaje": pPmax,
                "color": colors[4]
            },
            {
                "nombre": "CLO",
                "ensayos": nClo,
                "horas": int(round(hClo, 0)),
                "porcentaje": pClo,
                "color": colors[5]
            },
            {
                "nombre": "N1",
                "ensayos": nN1,
                "horas": int(round(hN1, 0)),
                "porcentaje": pN1,
                "color": colors[6]
            },
            {
                "nombre": "N2",
                "ensayos": nN2,
                "horas": int(round(hN2, 0)),
                "porcentaje": pN2,
                "color": colors[7]
            },
            {
                "nombre": "N4",
                "ensayos": nN4,
                "horas": int(round(hN4, 0)),
                "porcentaje": pN4,
                "color": colors[8]
            },
            {
                "nombre": "O1",
                "ensayos": nO1,
                "horas": int(round(hO1, 0)),
                "porcentaje": pO1,
                "color": colors[9]
            },
            {
                "nombre": "REC",
                "ensayos": nRec,
                "horas": int(round(hRec, 0)),
                "porcentaje": pRec,
                "color": colors[10]
            },
        ]

        ensayosOrdenados = sorted(
            ensayosOrdenados,
            key=lambda x: x['ensayos'],
            reverse=True
        )

        return {
            "totalEnsayos": totalEnsayos,
            "totalHoras": int(round(totalHoras, 0)),
            "ensayosOrdenados": ensayosOrdenados,
            
            "TMIC": {
                "horas": int(round(hTmic, 0)),
                "porcentaje": pTmic,
                "normativa": normaTmic,
            },
        }


    def equipos (self):
        tmic= Equipos.objects.filter(ensayos__ensayo = "TMIc")





############ QUEDA QUE TERMINEMOS LOS ENSAYOS (TMIN, LIE, EMI, PMAX) EN CALCULOS COMPARATIVA Y LUEGO QUE SE GESTIONEN TODOS LOS EQUIPOS









class mapaGenerator (): 
    def crearMapa():
        # 🔹 ver carpeta actual (por si necesitas comprobar ruta)
        print("Carpeta actual:", os.getcwd())

        # =====================================================
        # 🔹 FUNCIÓN PARA LIMPIAR NOMBRES (IMPORTANTE)
        # =====================================================
        def limpiar(texto):
            if pd.isna(texto):
                return texto
            texto = texto.lower()
            texto = ''.join(
                c for c in unicodedata.normalize('NFD', texto)
                if unicodedata.category(c) != 'Mn'
            )
            return texto.strip()

        # =====================================================
        # 1️⃣ CARGAR MAPA
        # =====================================================
        mapa = gpd.read_file("spain-provinces.geojson")

        # 🔹 limpiar nombres del mapa
        mapa["name_clean"] = mapa["name"].apply(limpiar)

        # =====================================================
        # 2️⃣ TUS DATOS (CAMBIA ESTO POR LOS TUYOS)
        # =====================================================
        clientes = pd.DataFrame({
            "name": [
                "Madrid", "Barcelona", "vaLencia", "Sevilla",
                "Zaragoza", "malaga", "Las Palmas", "Santa cruz de tenerife", "valladolid", "lugo", "leon", "ibiza", "cadiz"
            ],
            "clientes": [120, 95, 80, 60, 40, 55, 30, 25, 80, 70, 100, 40, 90]
        })

        # 🔹 limpiar nombres de tus datos
        clientes["name_clean"] = clientes["name"].apply(limpiar)

        # =====================================================
        # 3️⃣ UNIR DATOS AL MAPA
        # =====================================================
        mapa = mapa.merge(clientes[["name_clean", "clientes"]], on="name_clean", how="left")

        # rellenar provincias sin datos
        mapa["clientes"] = mapa["clientes"].fillna(0)

        # =====================================================
        # 4️⃣ SEPARAR CANARIAS (para inset)
        # =====================================================
        canarias = mapa[mapa["name_clean"].isin(["las palmas", "santa cruz de tenerife"])]

        # quitar canarias del mapa principal
        resto = mapa[~mapa["name_clean"].isin(["las palmas", "santa cruz de tenerife"])]

        # =====================================================
        # 5️⃣ CREAR FIGURA
        # =====================================================
        fig, ax = plt.subplots(figsize=(8,10))

        # 🔹 MAPA PRINCIPAL (SIN CANARIAS)
        resto.plot(
            column="clientes",
            cmap="Blues",
            linewidth=0.8,
            edgecolor="black",
            legend=False,
            ax=ax
        )

        ax.axis("off")

        # opcional: encuadre mejor la península
        ax.set_xlim(-15, 6)
        ax.set_ylim(36, 44)

        # =====================================================
        # 6️⃣ INSET CANARIAS
        # =====================================================
        ax_inset = fig.add_axes([0.20, 0.29, 0.15, 0.10])

        canarias.plot(
            column="clientes",
            cmap="Blues",
            linewidth=0.8,
            edgecolor="black",
            ax=ax_inset
        )

        # quitar ejes pero mantener borde
        ax_inset.set_xticks([])
        ax_inset.set_yticks([])

        # borde del recuadro
        for spine in ax_inset.spines.values():
            spine.set_edgecolor("black")
            spine.set_linewidth(1.2)

        # =====================================================
        # 7️⃣ GUARDAR Y MOSTRAR
        # =====================================================
        #plt.savefig("mapa_clientes.png", dpi=300, bbox_inches="tight", transparent=True)
        plt.show()