
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


class InformePDF:

    def __init__(self, periodo, usuario):
        self.periodo = periodo
        self.usuario = usuario
        self.ruta = os.path.dirname(__file__)

    def build(self):

        env = Environment(
            loader=FileSystemLoader(self.ruta)
        )

        template = env.get_template("plantillaReporte.html")
        bootstrap_css = "file:///" + os.path.join(self.ruta, "static", "css", "bootstrap.min.css").replace("\\", "/")
        bootstrap_js = "file:///" + os.path.join(self.ruta, "static", "js", "bootstrap.bundle.min.js").replace("\\", "/")

        html = template.render(
            periodo=self.periodo,
            usuario_nombre=self.usuario.first_name,
            usuario_apellido=self.usuario.last_name,
            # 👇 usa esto en debug (mejor con Django static si puedes)
            logo_path="file:///" + os.path.join(self.ruta, "Imagenes", "LOGO.png").replace("\\", "/"),
            bootstrap_css=bootstrap_css,
            bootstrap_js=bootstrap_js,
        )

        # =========================
        # 🧪 MODO DEBUG
        # =========================
        prueba= False
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
            page.wait_for_timeout(1000)

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