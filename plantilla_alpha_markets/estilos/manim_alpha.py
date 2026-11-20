"""Estilo ALPHA MARKETS para Manim Community (skills manim-composer + manimce-best-practices).
Gráficos, ejes, fórmulas y diagramas animados que luego se insertan en el vídeo con scripts/insertos.py.

uso (desde la carpeta de la plantilla):
    manim -qh -t --media_dir tmp/manim estilos/manim_alpha.py EjemploAlpha
      -qh  → 1080x1080 a 30 fps para la caja de escena (o 1080x1920 con ALPHA_FORMATO=completa)
      -t   → fondo TRANSPARENTE (.mov con alfa): el gráfico flota sobre el fondo de la plantilla
    luego copia el .mov de tmp/manim/videos/... a insertos/ y añádelo a insertos.json.

En tus escenas:  from manim_alpha import *   (pon el .py de la escena dentro de estilos/)
    with fuentes():          # registra Anton, Montserrat, Inter y Marker
        Text("6.300M $", font=ANTON, color=MINT)
"""
import os
from contextlib import ExitStack, contextmanager
from manim import *

_D = os.path.dirname(os.path.abspath(__file__))
_F = os.path.normpath(os.path.join(_D, '..', 'fonts'))

# --- lienzo: "escena" = 1080x1080 (para la caja central, por defecto) | "completa" = 1080x1920 vertical ---
#     PowerShell: $env:ALPHA_FORMATO="completa"; manim ...
FORMATO = os.environ.get('ALPHA_FORMATO', 'escena')
config.pixel_width = 1080
config.pixel_height = 1920 if FORMATO == 'completa' else 1080
config.frame_rate = 30
config.frame_width = 9          # 1 unidad = 120 px
config.frame_height = 16 if FORMATO == 'completa' else 9
config.background_color = "#040706"

# --- paleta (la misma que template.html) ---
BG = "#040706"; INK = "#F4FFF9"; MUTE = "#8FA39A"
MINT = "#34F5B0"; PIST = "#B6E36A"; ROJO = "#FF5A5F"; HIELO = "#9FE4FF"; ORO = "#F0B90B"
LINEA = "#1E4D3D"; RELLENO = "#121E1A"

# --- fuentes (nombres de familia para Text(font=...)) ---
#   MONT   = Montserrat Black Italic (titulares, como .h / .wm1)   MONT_B = Montserrat ExtraBold (etiquetas, como .lab)
ANTON = "Anton"; MONT = "Montserrat Alpha Black"; MONT_B = "Montserrat Alpha XBold"; INTER = "Inter Alpha Bold"
MARKER = "Permanent Marker"
_ARCH = ['ttf/Anton-Regular.ttf', 'ttf/MontserratAlpha-BlackItalic.ttf', 'ttf/MontserratAlpha-ExtraBold.ttf',
         'ttf/InterAlpha-Bold.ttf', 'ttf/PermanentMarker-Regular.ttf']


@contextmanager
def fuentes():
    with ExitStack() as st:
        for a in _ARCH:
            st.enter_context(register_font(os.path.join(_F, a)))
        yield


def tarjeta(w, h, color=LINEA):
    """Tarjeta redondeada como las .card de la plantilla."""
    return RoundedRectangle(corner_radius=0.3, width=w, height=h, fill_color=RELLENO, fill_opacity=0.85,
                            stroke_color=color, stroke_width=3)


def cifra(texto, color=MINT, size=140):
    """Cifra grande estilo bolsa, con contorno negro."""
    return Text(texto, font=ANTON, color=color, font_size=size).set_stroke(BLACK, width=10, background=True)


class EjemploAlpha(Scene):
    """Demo: barras que crecen + cifra clave. Plantilla para tus propios gráficos."""
    def construct(self):
        with fuentes():
            titulo = Text("BITCOIN 2026", font=MONT, slant=ITALIC, color=INK, font_size=64).to_edge(UP, buff=0.5)
            ax = Axes(x_range=[0, 5, 1], y_range=[0, 100, 25], x_length=7, y_length=5,
                      axis_config={"color": MUTE, "stroke_width": 3}, tips=False).to_edge(DOWN, buff=0.5)
            vals = [22, 41, 35, 88]
            barras = VGroup(*[Rectangle(width=0.95, height=ax.y_axis.unit_size * v, fill_color=MINT if i == 3 else PIST,
                                        fill_opacity=0.95, stroke_width=0).move_to(ax.c2p(i + 1, 0), aligned_edge=DOWN)
                              for i, v in enumerate(vals)])
            dato = cifra("+88%").next_to(barras[-1], UP, buff=0.3)
            dato.shift(RIGHT * min(0, config.frame_width / 2 - 0.4 - dato.get_right()[0]))   # nunca fuera del encuadre
            self.play(Write(titulo), Create(ax), run_time=0.8)
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in barras], lag_ratio=0.18), run_time=1.4, rate_func=rate_functions.ease_out_back)
            self.play(FadeIn(dato, scale=1.6), run_time=0.4, rate_func=rate_functions.ease_out_back)
            self.wait(0.8)
