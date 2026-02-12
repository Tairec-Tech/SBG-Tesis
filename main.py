"""
Sistema de Brigadas Escolares — Brigadas Ambientales (Municipio Maracaibo).
Flujo: intro (bloques SGB en verde) → Login / Registrar / Recuperar → App (sidebar + contenido).
Tema: tonos verdes (brigadas ambientales).
"""

import asyncio
import json
import os
import random
import sys
import flet as ft

from util_log import log

# Para ver mensajes aunque la terminal no muestre nada: abre sbg_log.txt en esta carpeta
log("--- App SBG iniciando ---")
sys.stdout.flush()
sys.stderr.flush()

from theme import (
    COLOR_FONDO_VERDE,
    COLOR_FONDO_GRADIENTE_INICIO,
    COLOR_FONDO_GRADIENTE_FIN,
    COLOR_PRIMARIO_OSCURO,
    COLOR_PRIMARIO,
    COLOR_PRIMARIO_CLARO,
)
from screens import screen_login, screen_register, screen_recovery
from screens import screen_dashboard
from components import build_sidebar

# Cortina de transición (paleta verde)
TRANSITION_VERDE = COLOR_PRIMARIO
TRANSITION_TEXT = "#FFFFFF"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGOS_DIR = os.path.join(BASE_DIR, "uploads", "logos")

# Abreviaturas para bienvenida
ABREV_ROL = {"Directivo": "Dir.", "Coordinador": "Coord.", "Profesor": "Prof."}


async def main(page: ft.Page):
    log("Ventana principal abierta")
    page.title = "Sistema de Brigadas Escolares"
    page.bgcolor = COLOR_FONDO_GRADIENTE_INICIO
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 0
    page.window.maximized = True
    page.update()

    # ----- Animación de entrada: bloques SGB (tonos verdes) -----
    size_bloque = 14
    gap_bloque = 4
    duracion_anim = 1200
    # Tres tonos verdes para S, G, B (brigadas ambientales)
    c_s, c_g, c_b = COLOR_PRIMARIO_OSCURO, COLOR_PRIMARIO, COLOR_PRIMARIO_CLARO
    partes_sgb = [
        (0, 0, c_s), (1, 0, c_s), (2, 0, c_s), (0, 1, c_s), (0, 2, c_s), (1, 2, c_s), (2, 2, c_s), (2, 3, c_s), (0, 4, c_s), (1, 4, c_s), (2, 4, c_s),
        (4, 0, c_g), (5, 0, c_g), (6, 0, c_g), (4, 1, c_g), (4, 2, c_g), (5, 2, c_g), (6, 2, c_g), (4, 3, c_g), (6, 3, c_g), (4, 4, c_g), (5, 4, c_g), (6, 4, c_g),
        (8, 0, c_b), (9, 0, c_b), (10, 0, c_b), (8, 1, c_b), (10, 1, c_b), (8, 2, c_b), (9, 2, c_b), (10, 2, c_b), (8, 3, c_b), (10, 3, c_b), (8, 4, c_b), (9, 4, c_b), (10, 4, c_b),
    ]
    ancho_canvas = 11 * (size_bloque + gap_bloque)
    alto_canvas = 5 * (size_bloque + gap_bloque)
    animacion_entrada = ft.Animation(
        duration=ft.Duration(milliseconds=600),
        curve=ft.AnimationCurve.EASE_OUT_BACK,
    )
    bloques_containers = [
        ft.Container(animate=duracion_anim, animate_position=duracion_anim, animate_rotation=duracion_anim)
        for _ in partes_sgb
    ]
    canvas_sgb = ft.Stack(
        controls=bloques_containers,
        width=ancho_canvas,
        height=alto_canvas,
        animate_scale=duracion_anim,
        animate_opacity=duracion_anim,
    )

    def dispersar_bloques():
        random.seed()
        for i in range(len(partes_sgb)):
            c = canvas_sgb.controls[i]
            tam = random.randrange(size_bloque - 2, size_bloque + 10)
            c.left = random.randrange(0, max(1, ancho_canvas - tam))
            c.top = random.randrange(0, max(1, alto_canvas - tam))
            c.bgcolor = partes_sgb[i][2]
            c.width, c.height = tam, tam
            c.border_radius = random.randrange(2, 8)
            c.rotate = random.randrange(-30, 30) * 3.14159 / 180
        canvas_sgb.scale = 0.85
        canvas_sgb.opacity = 0.9

    def ensamblar_bloques():
        for i, (col, fila, color) in enumerate(partes_sgb):
            c = canvas_sgb.controls[i]
            c.left = col * (size_bloque + gap_bloque)
            c.top = fila * (size_bloque + gap_bloque)
            c.bgcolor = color
            c.width = c.height = size_bloque
            c.border_radius = 4
            c.rotate = 0
        canvas_sgb.scale = 1
        canvas_sgb.opacity = 1

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
    # Contenedor del área de contenido (sidebar cambia su .content)
    content_area = ft.Container(expand=True, bgcolor=COLOR_FONDO_VERDE)
    vista_actual = ["Panel Principal"]
    content_area.content = screen_dashboard.build(page)

    # Contenedor del sidebar para poder reconstruirlo al cambiar de vista
    sidebar_container = ft.Container()


    # Vista principal: sidebar + contenido (solo se muestra tras login)
    vista_principal = ft.Container(expand=True)  # .content se asigna tras refresh_sidebar

    def build_login_view():
        return screen_login.build(
            page,
            on_login_success=ir_a_app,
            on_go_register=ir_a_registro,
            on_go_recovery=ir_a_recuperar,
        )

    # Un solo contenedor que cambia de contenido: login/registro/recuperar O app (sidebar+contenido)
    contenedor_principal = ft.Container(expand=True, alignment=ft.Alignment.CENTER)

    # ----- Cortina de transición Login -> Dashboard (verde) -----
    icon_success = ft.Icon(
        ft.Icons.CHECK_CIRCLE_ROUNDED,
        size=100,
        color=TRANSITION_TEXT,
    )
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
        bgcolor=TRANSITION_VERDE,
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
        """Secuencia: cortina verde -> logo o icono (pop) -> texto bienvenida con abreviatura e institución -> cambio a app -> desvanecer."""
        # Obtener datos del usuario para personalizar bienvenida
        try:
            data_str = await page.shared_preferences.get("usuario_actual")
            data = json.loads(data_str) if data_str else {}
        except Exception:
            data = {}
        nombre = f"{data.get('nombre', '')} {data.get('apellido', '')}".strip() or "Usuario"
        rol = data.get("rol", "")
        abrev = ABREV_ROL.get(rol, rol)
        inst_nombre = data.get("institucion_nombre", "Institución")
        text_welcome.value = f"Bienvenido {abrev} {nombre} a la coordinación de brigadas de la institución {inst_nombre}"

        # Mostrar logo de la institución (circular) si existe, si no el icono de check
        logo_ruta = data.get("institucion_logo_ruta")
        logo_path = os.path.join(LOGOS_DIR, logo_ruta) if logo_ruta else None
        if logo_path and os.path.isfile(logo_path):
            icon_success_container.content = ft.Container(
                content=ft.Image(src=logo_path, width=100, height=100, fit=ft.ImageFit.COVER),
                width=100,
                height=100,
                border_radius=50,
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
        await page.shared_preferences.remove("usuario_actual")
        if getattr(page, "data", None) and "usuario_actual" in page.data:
            del page.data["usuario_actual"]
        contenedor_principal.content = build_login_view()
        page.update()

    def ir_a_app():
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

    # Primero mostrar la ventana (evita quedarse en "working"); el sidebar se rellena después
    log("Añadiendo contenido a la página...")
    # Overlay de intro: bloques SGB que se ensamblan + subtítulo (encima de todo al inicio)
    intro_overlay = ft.Container(
        content=ft.Column(
            [
                ft.Container(content=canvas_sgb, scale=2.2),
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

    # Stack: contenedor principal, intro, cortina de transición (encima de todo al hacer login)
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
    log("Ventana mostrada; cargando sidebar en segundo plano...")
    # Sidebar se construye en segundo plano (shared_preferences puede bloquear si se hace antes de mostrar la ventana)
    page.run_task(refresh_sidebar)
    page.run_task(animacion_inicio_automatica)


if __name__ == "__main__":
    ft.run(main)
