from fpdf import FPDF
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import os
import unicodedata


class InformePDF(FPDF):

    def __init__(self, periodo, usario):
        super().__init__()
        self.periodo = periodo
        self.usuario= usario
        self.azulFuerte = (25, 43, 92)     # #192B5C
        self.azulMedio  = (95, 107, 139)   # #5F6B8B
        self.turquesa   = (46, 149, 170)   # #2E95AA
        self.gris       = (168, 180, 197)  # #A8B4C5
        self.blanco     = (238, 242, 244)  # #EEF2F4
        self.rutaAbsoluta = os.path.dirname(__file__)


    # -------------------------
    # MÉTODO PRINCIPAL
    # -------------------------
    def build(self):
        # Portada
        self.add_page()
        self._portada()

        return self.output(dest="S").encode("latin1")
    

    # -------------------------
    # footer
    # -------------------------
    def footer(self):
        pass

    # -------------------------
    # SECCIONES
    # -------------------------
    def _portada(self):

        # ===== TITULO =====
        self.set_font("Helvetica", "B", 24)
        self.set_text_color(*self.azulFuerte)

        texto = "Informe de resultados obtenidos en el área de Sustancias Inflamables"

        bloque_ancho = 120
        x = (self.w - bloque_ancho) / 4

        self.set_xy(x, 15)
        self.multi_cell(
            w=bloque_ancho,
            h=12,
            txt=texto,
            align="L"
        )

        # ===== PERIODO =====
        if len(self.periodo) == 2:
            nombrePeriodo = f"Entre el {self.periodo[0]} y el {self.periodo[1]}"
        else:
            nombrePeriodo = f"Año {self.periodo[0]}"

        self.set_font("Helvetica", "B", 20)
        self.set_text_color(*self.turquesa)

        self.set_x(x)  # mantiene centrado respecto al bloque
        self.multi_cell(
            w=bloque_ancho,
            h=10,
            txt=nombrePeriodo,
            align="L"
        )

        # ===== LOGO =====
        image_path = os.path.join(self.rutaAbsoluta, "Imagenes", "LOGO.png")

        ancho_imagen = 140
        alto_imagen = 140

        x_img = (self.w - ancho_imagen) / 2
        y_img = (self.h - alto_imagen) / 2   # centrado vertical visual

        self.image(
            image_path,
            x=x_img,
            y=y_img,
            w=ancho_imagen,
            h=alto_imagen,
            link="http://www.lom.upm.es"
        )

        self.set_y(-30)
        self.set_font("Helvetica", "", 12)

        #miniLogo
        ancho_imagen= 15
        posicionX= 5

        self.image(image_path, y= self.y-5, x= posicionX, w=ancho_imagen, h=ancho_imagen)
        
        cursorX= ancho_imagen + posicionX
        self.set_x(cursorX)
        self.set_text_color(*self.azulFuerte)
        self.cell(w=((self.w-cursorX)/2), h=5, txt="Laboratorio Oficial J.M. Madariaga", align= "L")
        self.cell(w=((self.w-cursorX)/2)-posicionX, h=5, txt=f"Generado por {self.usuario.first_name} {self.usuario.last_name}", align= "R")

    def _indice(self):
        self._titulo("Índice")

        secciones = [
            "Resumen ejecutivo",
            "Ventas",
            "Finanzas"
        ]

        self.set_font("Helvetica", "", 12)
        for s in secciones:
            self.cell(0, 8, s, 0, 1)

    def _prologo(self):
        self._titulo("Resumen ejecutivo")

        self.set_font("Helvetica", "", 12)
        self.multi_cell(0, 8, "Aquí va el resumen generado dinámicamente.")

    def _resumenEjecutivo(self): #Se compara año anterior vs año nuevo (si es año completo genial, si no, se compara periodo del año anterior conn periodo de este)
        pass
    
    def _resumen(self):
        self._titulo("Ventas")
        self.multi_cell(0, 8, "Datos de ventas...")

    def _mapa(self):
        self._titulo("Finanzas")
        self.multi_cell(0, 8, "Datos financieros...")
    
    def _ensayos(self):
        self._titulo("Finanzas")
        self.multi_cell(0, 8, "Datos financieros...")

    # -------------------------
    # HELPERS
    # -------------------------
    def _titulo(self, texto):
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 10, texto, 0, 1)
        self.ln(4)



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