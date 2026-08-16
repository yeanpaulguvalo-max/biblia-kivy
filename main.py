"""
Palabra del Día - versión Kivy
App que muestra versículos al azar y puede establecerlos como
fondo de pantalla usando WallpaperManager de Android (vía Pyjnius).
"""

import os
import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.utils import platform

# --- Datos de ejemplo (después se reemplaza con la base completa) ---
VERSICULOS = [
    {"libro": "Salmos", "cap": 23, "ver": 1,
     "texto": "Jehová es mi pastor; nada me faltará."},
    {"libro": "Juan", "cap": 3, "ver": 16,
     "texto": "Porque de tal manera amó Dios al mundo, que ha dado a su Hijo unigénito."},
    {"libro": "Filipenses", "cap": 4, "ver": 13,
     "texto": "Todo lo puedo en Cristo que me fortalece."},
    {"libro": "Proverbios", "cap": 3, "ver": 5,
     "texto": "Fíate de Jehová de todo tu corazón, y no te apoyes en tu propia prudencia."},
]


def crear_imagen_versiculo(texto, referencia, ruta_salida):
    """Genera una imagen 1080x1920 con el versículo, usando Pillow."""
    from PIL import Image, ImageDraw, ImageFont

    ancho, alto = 1080, 1920
    img = Image.new("RGB", (ancho, alto), color="#f2ede1")
    draw = ImageDraw.Draw(img)

    try:
        fuente_texto = ImageFont.truetype("DejaVuSerif.ttf", 54)
        fuente_ref = ImageFont.truetype("DejaVuSans-Bold.ttf", 32)
    except OSError:
        fuente_texto = ImageFont.load_default()
        fuente_ref = ImageFont.load_default()

    # Partir el texto en líneas que entren en el ancho disponible
    max_ancho = int(ancho * 0.78)
    palabras = texto.split(" ")
    lineas, linea_actual = [], ""
    for palabra in palabras:
        prueba = f"{linea_actual} {palabra}".strip()
        bbox = draw.textbbox((0, 0), prueba, font=fuente_texto)
        if bbox[2] - bbox[0] > max_ancho and linea_actual:
            lineas.append(linea_actual)
            linea_actual = palabra
        else:
            linea_actual = prueba
    if linea_actual:
        lineas.append(linea_actual)

    alto_linea = 74
    alto_bloque = len(lineas) * alto_linea
    y = (alto - alto_bloque) // 2

    for linea in lineas:
        bbox = draw.textbbox((0, 0), linea, font=fuente_texto)
        x = (ancho - (bbox[2] - bbox[0])) // 2
        draw.text((x, y), linea, font=fuente_texto, fill="#2e2620")
        y += alto_linea

    bbox = draw.textbbox((0, 0), referencia, font=fuente_ref)
    x = (ancho - (bbox[2] - bbox[0])) // 2
    draw.text((x, y + 40), referencia, font=fuente_ref, fill="#a8863b")

    img.save(ruta_salida)
    return ruta_salida


def establecer_fondo_pantalla(ruta_imagen):
    """Usa WallpaperManager de Android para cambiar el fondo directamente."""
    if platform != "android":
        print(f"[Simulado] Se establecería como fondo: {ruta_imagen}")
        return

    from jnius import autoclass

    WallpaperManager = autoclass("android.app.WallpaperManager")
    PythonActivity = autoclass("org.kivy.android.PythonActivity")
    BitmapFactory = autoclass("android.graphics.BitmapFactory")

    activity = PythonActivity.mActivity
    wallpaper_manager = WallpaperManager.getInstance(activity)
    bitmap = BitmapFactory.decodeFile(ruta_imagen)
    wallpaper_manager.setBitmap(bitmap)


class PantallaPrincipal(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=30, spacing=20, **kwargs)
        self.versiculo_actual = random.choice(VERSICULOS)

        self.label = Label(
            text=self._texto_formateado(),
            font_size="22sp",
            halign="center",
            valign="middle",
        )
        self.label.bind(size=self.label.setter("text_size"))
        self.add_widget(self.label)

        btn_nuevo = Button(text="Otro versículo", size_hint=(1, 0.15))
        btn_nuevo.bind(on_press=self.nuevo_versiculo)
        self.add_widget(btn_nuevo)

        self.btn_fondo = Button(text="Usar como fondo de pantalla", size_hint=(1, 0.15))
        self.btn_fondo.bind(on_press=self.cambiar_fondo)
        self.add_widget(self.btn_fondo)

    def _texto_formateado(self):
        v = self.versiculo_actual
        return f'"{v["texto"]}"\n\n{v["libro"]} {v["cap"]}:{v["ver"]}'

    def nuevo_versiculo(self, instance):
        self.versiculo_actual = random.choice(VERSICULOS)
        self.label.text = self._texto_formateado()

    def cambiar_fondo(self, instance):
        v = self.versiculo_actual
        referencia = f'{v["libro"]} {v["cap"]}:{v["ver"]}'
        ruta = os.path.join(App.get_running_app().user_data_dir, "fondo_temp.png")

        self.btn_fondo.text = "Generando..."
        crear_imagen_versiculo(v["texto"], referencia, ruta)
        establecer_fondo_pantalla(ruta)
        self.btn_fondo.text = "¡Fondo actualizado!"


class PalabraDelDiaApp(App):
    def build(self):
        return PantallaPrincipal()


if __name__ == "__main__":
    PalabraDelDiaApp().run()
