"""
Sistema de Brigadas Escolares — Multi-Brigada (Municipio Maracaibo).
Flujo: intro (bloques SBE neutros) → Login (neutro) → Selección de Brigada (2×2)
       → Transición (color de brigada) → App (sidebar + contenido).
Soporta 4 tipos: Gestión de Riesgo, Patrulla Escolar, Convivencia y Paz, Ecológica.
"""

import asyncio
import json
import os
import random
import sys
import flet as ft

from util_log import log

log("--- App SBE iniciando ---")
if sys.stdout:
    sys.stdout.flush()
if sys.stderr:
    sys.stderr.flush()

from theme import (
    TEMA_CLARO,
    TEMA_OSCURO,
    BRIGADAS,
    aplicar_paleta,
    aplicar_paleta_neutra,
    HEX_NEUTRA_PRIMARIO,
    HEX_NEUTRA_PRIMARIO_CLARO,
    HEX_NEUTRA_PRIMARIO_OSCURO,
    COLOR_FONDO_VERDE,
    COLOR_FONDO_GRADIENTE_INICIO,
)
from screens import screen_login, screen_register, screen_recovery
from screens import screen_dashboard, screen_brigade_select
from components import build_sidebar

TRANSITION_TEXT = "#FFFFFF"
if getattr(sys, 'frozen', False):
    # Si la app está empaquetada como .exe, buscar junto al ejecutable
    EXE_DIR = os.path.dirname(sys.executable)
else:
    EXE_DIR = os.path.dirname(os.path.abspath(__file__))

LOGOS_DIR = os.path.join(EXE_DIR, "uploads", "logos")

ABREV_ROL = {"Directivo": "Dir.", "Coordinador": "Coord.", "Profesor": "Prof."}


async def main(page: ft.Page):
    log("Ventana principal abierta")
    page.title = "Sistema de Brigadas Escolares"
    page.window.icon = "SBE.ico"
    # Iniciar con paleta neutra para la intro y login
    aplicar_paleta_neutra(page)
    page.theme_mode = ft.ThemeMode.LIGHT

    page.bgcolor = COLOR_FONDO_GRADIENTE_INICIO
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 0
    page.window.maximized = True
    # Registrar fuente elegante para la selección de brigadas
    page.fonts = {"Outfit": "https://raw.githubusercontent.com/nicholasmireles/fonts/main/ofl/outfit/Outfit%5Bwght%5D.ttf"}
    page.update()

    # ----- Animación de entrada: bloques SBE (tonos neutros) -----
    size_bloque = 14
    gap_bloque = 4
    duracion_anim = 1200
    # Tres tonos neutros para S, B, E
    c_s = HEX_NEUTRA_PRIMARIO_OSCURO
    c_b = HEX_NEUTRA_PRIMARIO
    c_e = HEX_NEUTRA_PRIMARIO_CLARO
    partes_sbe = [
        # S (cols 0-2)
        (0, 0, c_s), (1, 0, c_s), (2, 0, c_s), (0, 1, c_s), (0, 2, c_s), (1, 2, c_s), (2, 2, c_s), (2, 3, c_s), (0, 4, c_s), (1, 4, c_s), (2, 4, c_s),
        # B (cols 4-6)
        (4, 0, c_b), (5, 0, c_b), (6, 0, c_b), (4, 1, c_b), (6, 1, c_b), (4, 2, c_b), (5, 2, c_b), (6, 2, c_b), (4, 3, c_b), (6, 3, c_b), (4, 4, c_b), (5, 4, c_b), (6, 4, c_b),
        # E (cols 8-10)
        (8, 0, c_e), (9, 0, c_e), (10, 0, c_e), (8, 1, c_e), (8, 2, c_e), (9, 2, c_e), (10, 2, c_e), (8, 3, c_e), (8, 4, c_e), (9, 4, c_e), (10, 4, c_e),
    ]
    ancho_canvas = 11 * (size_bloque + gap_bloque)
    alto_canvas = 5 * (size_bloque + gap_bloque)
    bloques_containers = [
        ft.Container(animate=duracion_anim, animate_position=duracion_anim, animate_rotation=duracion_anim)
        for _ in partes_sbe
    ]
    canvas_sbe = ft.Stack(
        controls=bloques_containers,
        width=ancho_canvas,
        height=alto_canvas,
        animate_scale=duracion_anim,
        animate_opacity=duracion_anim,
    )

    def dispersar_bloques():
        random.seed()
        for i in range(len(partes_sbe)):
            c = canvas_sbe.controls[i]
            tam = random.randrange(size_bloque - 2, size_bloque + 10)
            c.left = random.randrange(0, max(1, ancho_canvas - tam))
            c.top = random.randrange(0, max(1, alto_canvas - tam))
            c.bgcolor = partes_sbe[i][2]
            c.width, c.height = tam, tam
            c.border_radius = random.randrange(2, 8)
            c.rotate = random.randrange(-30, 30) * 3.14159 / 180
        canvas_sbe.scale = 0.85
        canvas_sbe.opacity = 0.9

    def ensamblar_bloques():
        for i, (col, fila, color) in enumerate(partes_sbe):
            c = canvas_sbe.controls[i]
            c.left = col * (size_bloque + gap_bloque)
            c.top = fila * (size_bloque + gap_bloque)
            c.bgcolor = color
            c.width = c.height = size_bloque
            c.border_radius = 4
            c.rotate = 0
        canvas_sbe.scale = 1
        canvas_sbe.opacity = 1

    texto_subtitulo_intro = ft.Text(
        "Sistema de Brigadas Escolares",
        size=15,
        color="#64748b",
        text_align=ft.TextAlign.CENTER,
    )
    texto_subtitulo_intro_container = ft.Container(
        content=texto_subtitulo_intro,
        opacity=0,
        animate_opacity=ft.Animation(duration=ft.Duration(milliseconds=500), curve=ft.AnimationCurve.EASE_OUT),
    )

    # ----- Estado de la app -----
    content_area = ft.Container(expand=True, bgcolor=COLOR_FONDO_VERDE)
    vista_actual = ["Panel Principal"]
    content_area.content = ft.Container()

    sidebar_container = ft.Container()
    vista_principal = ft.Container(expand=True)

    def build_login_view():
        return screen_login.build(
            page,
            on_login_success=ir_a_seleccion_brigada,
            on_go_register=ir_a_registro,
            on_go_recovery=ir_a_recuperar,
        )

    contenedor_principal = ft.Container(expand=True, alignment=ft.Alignment.CENTER)

    # ----- Cortina de transición Login -> Dashboard -----
    icon_success = ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, size=100, color=TRANSITION_TEXT)
    icon_success_container = ft.Container(
        content=icon_success,
        scale=0,
        animate_scale=ft.Animation(400, ft.AnimationCurve.EASE_OUT_BACK),
    )
    text_welcome = ft.Text(
        "¡Bienvenido!",
        size=18,
        weight="bold",
        color=TRANSITION_TEXT,
        opacity=0,
        animate_opacity=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
        text_align=ft.TextAlign.CENTER,
    )
    transition_overlay = ft.Container(
        expand=True,
        bgcolor=HEX_NEUTRA_PRIMARIO,  # Se cambiará al color de la brigada
        opacity=0,
        visible=False,
        animate_opacity=ft.Animation(500, ft.AnimationCurve.EASE_IN_OUT),
        alignment=ft.Alignment.CENTER,
        content=ft.Column(
            [
                icon_success_container,
                ft.Container(height=20),
                text_welcome,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )

    async def animar_entrada_dashboard():
        """Secuencia: cortina color brigada -> logo o icono (pop) -> texto bienvenida -> cambio a app -> desvanecer."""
        try:
            prefs = ft.SharedPreferences()
            data_str = await prefs.get("usuario_actual")
            data = json.loads(data_str) if data_str else {}
        except Exception:
            data = {}
        nombre = f"{data.get('nombre', '')} {data.get('apellido', '')}".strip() or "Usuario"
        rol = data.get("rol", "")
        abrev = ABREV_ROL.get(rol, rol)
        inst_nombre = data.get("institucion_nombre", "Institución")

        # Nombre de la brigada activa
        brigada_key = (page.data or {}).get("brigada_activa", "ecologica")
        brigada_info = BRIGADAS.get(brigada_key, {})
        brigada_nombre = brigada_info.get("nombre", "Brigada")

        text_welcome.value = f"Bienvenido {abrev} {nombre}\n{brigada_nombre}\n{inst_nombre}"

        # Color de transición = color primario de la brigada seleccionada
        transition_overlay.bgcolor = brigada_info.get("hex_primario", HEX_NEUTRA_PRIMARIO)

        logo_ruta = data.get("institucion_logo_ruta")
        logo_path = os.path.join(LOGOS_DIR, logo_ruta) if logo_ruta else None
        if logo_path and os.path.isfile(logo_path):
            icon_success_container.content = ft.Container(
                content=ft.Image(src=logo_path, width=100, height=100, fit=ft.BoxFit.COVER),
                width=100, height=100, border_radius=50,
                clip_behavior=ft.ClipBehavior.HARD_EDGE,
                border=ft.Border.all(3, "white"),
            )
        else:
            icon_success_container.content = ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, size=100, color=TRANSITION_TEXT)

        transition_overlay.visible = True
        transition_overlay.opacity = 1
        page.update()
        await asyncio.sleep(0.5)

        icon_success_container.scale = 1
        text_welcome.opacity = 1
        page.update()
        await asyncio.sleep(1.2)

        contenedor_principal.content = vista_principal
        page.update()

        icon_success_container.scale = 0
        text_welcome.opacity = 0
        page.update()
        await asyncio.sleep(0.2)

        transition_overlay.opacity = 0
        page.update()
        await asyncio.sleep(0.5)
        transition_overlay.visible = False
        page.update()

    async def cerrar_sesion():
        prefs = ft.SharedPreferences()
        await prefs.remove("usuario_actual")
        if getattr(page, "data", None) and isinstance(page.data, dict):
            page.data.pop("usuario_actual", None)
            page.data.pop("brigada_activa", None)
            # Limpiar caché del dashboard para que no herede el próximo inicio de sesión
            claves_a_eliminar = [k for k in page.data.keys() if k.startswith("_cache_") or k.startswith("_dashboard_")]
            for k in claves_a_eliminar:
                page.data.pop(k, None)
        aplicar_paleta_neutra(page)
        contenedor_principal.content = build_login_view()
        page.update()

    def ir_a_seleccion_brigada():
        """Tras login exitoso: mostrar pantalla de selección de brigada."""
        contenedor_principal.content = screen_brigade_select.build(
            page,
            on_select=on_brigada_seleccionada,
        )
        page.update()

    def on_brigada_seleccionada(brigada_key: str):
        """Usuario seleccionó una brigada → aplicar paleta → transición → dashboard."""
        if not isinstance(page.data, dict):
            page.data = {}
        page.data["brigada_activa"] = brigada_key
        aplicar_paleta(page, brigada_key)
        # Reconstruir content area con el nuevo tema
        content_area.bgcolor = COLOR_FONDO_VERDE
        content_area.content = screen_dashboard.build(page)
        vista_principal.content = ft.Row([sidebar_container, content_area], expand=True)
        page.run_task(refresh_sidebar)
        page.run_task(animar_entrada_dashboard)

    def ir_a_registro():
        contenedor_principal.content = screen_register.build(page, on_back_to_login=volver_a_login)
        page.update()

    def ir_a_recuperar():
        contenedor_principal.content = screen_recovery.build(page, on_back_to_login=volver_a_login)
        page.update()

    def volver_a_login():
        contenedor_principal.content = build_login_view()
        page.update()

    contenedor_principal.content = build_login_view()
    vista_principal.content = ft.Row([sidebar_container, content_area], expand=True)

    async def refresh_sidebar():
        log("refresh_sidebar: construyendo sidebar...")
        try:
            sidebar_container.content = await build_sidebar(
                page, content_area, vista_actual,
                on_logout=lambda: page.run_task(cerrar_sesion),
                on_nav_change=lambda: page.run_task(refresh_sidebar),
            )
            page.update()
            log("refresh_sidebar: listo")
        except Exception as e:
            log(f"refresh_sidebar ERROR: {e}")
            page.update()

    log("Añadiendo contenido a la página...")
    intro_overlay = ft.Container(
        content=ft.Column(
            [
                ft.Container(content=canvas_sbe, scale=2.2),
                ft.Container(height=56),
                texto_subtitulo_intro_container,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=0,
        ),
        expand=True,
        bgcolor=COLOR_FONDO_GRADIENTE_INICIO,
        alignment=ft.Alignment.CENTER,
        animate_opacity=ft.Animation(duration=ft.Duration(milliseconds=500), curve=ft.AnimationCurve.EASE_OUT),
    )

    async def animacion_inicio_automatica():
        await asyncio.sleep(0.5)
        ensamblar_bloques()
        page.update()
        await asyncio.sleep(1.3)
        texto_subtitulo_intro_container.opacity = 1
        page.update()
        await asyncio.sleep(1.2)
        intro_overlay.opacity = 0
        page.update()
        await asyncio.sleep(0.55)
        intro_overlay.visible = False
        page.update()

    stack_principal = ft.Stack(
        controls=[
            contenedor_principal,
            intro_overlay,
            transition_overlay,
        ],
        expand=True,
    )
    page.add(stack_principal)
    dispersar_bloques()
    page.update()
    log("Ventana mostrada; animación en progreso...")
    page.run_task(animacion_inicio_automatica)


if __name__ == "__main__":
    ft.run(main, assets_dir="assets")
