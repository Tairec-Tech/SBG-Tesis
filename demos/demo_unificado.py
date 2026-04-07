"""
Demo PRO — Hover + Flip con mejoras de rendimiento y UX.
- GestureDetector para hover confiable
- Updates selectivos (.update() por control)
- nonlocal para estado limpio
- Hover con sombra dinámica (tarjeta viva)
- Curvas EASE_OUT_CUBIC para fluidez premium
- Glassmorphism + cursor CLICK
"""
import flet as ft

BRIGADAS = [
    {"nombre": "Gestión de Riesgo", "sub": "y Primeros Auxilios", "icono": ft.Icons.HEALTH_AND_SAFETY,
     "color": "#dc2626", "grad": ["#b91c1c", "#dc2626"],
     "desc": "Gestión de emergencias, evacuación, simulacros y primeros auxilios ante desastres naturales.",
     "desc_larga": "Formación en prevención y respuesta ante emergencias y desastres naturales. Incluye planificación de rutas de evacuación, ejecución de simulacros, técnicas de primeros auxilios, manejo de extintores y coordinación con organismos de protección civil."},
    {"nombre": "Patrulla Escolar", "sub": "Seguridad Vial", "icono": ft.Icons.TRAFFIC,
     "color": "#ea580c", "grad": ["#c2410c", "#ea580c"],
     "desc": "Seguridad vial, control de tránsito peatonal y protección de la comunidad escolar.",
     "desc_larga": "Educación en normas de tránsito y seguridad vial. Los estudiantes aprenden señalización, control de cruces peatonales, organización del flujo vehicular en horas de entrada y salida, y campañas de concientización sobre el uso del cinturón y el respeto a las señales."},
    {"nombre": "Convivencia y Paz", "sub": "Prevención Integral", "icono": ft.Icons.HANDSHAKE,
     "color": "#64748b", "grad": ["#475569", "#64748b"],
     "desc": "Mediación de conflictos, cultura de paz y prevención de violencia escolar.",
     "desc_larga": "Promoción de la convivencia pacífica y prevención de la violencia. Incluye mediación de conflictos entre estudiantes, talleres de comunicación asertiva, campañas contra el bullying, fortalecimiento de valores como el respeto, la tolerancia y la solidaridad."},
    {"nombre": "Brigada Ecológica", "sub": "Medio Ambiente", "icono": ft.Icons.ECO,
     "color": "#059669", "grad": ["#047857", "#059669"],
     "desc": "Conservación ambiental, reciclaje, reforestación y educación ecológica.",
     "desc_larga": "Cuidado y preservación del medio ambiente escolar y comunitario. Actividades de reciclaje, huertos escolares, jornadas de reforestación, ahorro de agua y energía, y campañas de sensibilización ambiental para toda la comunidad educativa."},
]

CARD_W = 340
CARD_H = 360

# Sombras reutilizables
_SHADOW_NORMAL = [ft.BoxShadow(blur_radius=30, spread_radius=-4,
    color=ft.Colors.with_opacity(0.12, "#1e293b"), offset=ft.Offset(0, 12))]
_SHADOW_HOVER = [ft.BoxShadow(blur_radius=40, spread_radius=-6,
    color=ft.Colors.with_opacity(0.2, "#1e293b"), offset=ft.Offset(0, 18))]


def crear_tarjeta_interactiva(page: ft.Page, cfg: dict):
    color = cfg["color"]
    grad = cfg["grad"]
    is_front = True  # nonlocal — estado limpio

    # ── Panel deslizante ──
    panel_deslizante = ft.Container(
        content=ft.Column([
            ft.Text("Resumen", size=14, weight="w800", color="white"),
            ft.Text(cfg["desc"], size=13, color=ft.Colors.with_opacity(0.9, "white"),
                    max_lines=3, overflow=ft.TextOverflow.ELLIPSIS),
        ], spacing=4),
        bgcolor=color,
        padding=ft.Padding(24, 16, 24, 16),
        height=110,
        bottom=0, left=0, right=0,
        offset=ft.Offset(0, 1.0),
        animate_offset=ft.Animation(350, ft.AnimationCurve.EASE_OUT_CUBIC),
    )

    # ── Cara frontal ──
    top_bar = ft.Container(
        height=5, border_radius=ft.BorderRadius(3, 3, 0, 0),
        gradient=ft.LinearGradient(colors=[color, grad[0], color],
            begin=ft.Alignment(-1, 0), end=ft.Alignment(1, 0)),
    )

    icon_circle = ft.Container(
        content=ft.Icon(cfg["icono"], color="white", size=44),
        width=90, height=90, border_radius=45,
        gradient=ft.LinearGradient(colors=grad,
            begin=ft.Alignment.TOP_LEFT, end=ft.Alignment.BOTTOM_RIGHT),
        alignment=ft.Alignment(0, 0),
        shadow=[ft.BoxShadow(blur_radius=20, spread_radius=0,
            color=ft.Colors.with_opacity(0.4, color), offset=ft.Offset(0, 8))],
    )

    contenido_base = ft.Container(
        content=ft.Column([
            top_bar,
            ft.Container(height=24),
            icon_circle,
            ft.Container(height=16),
            ft.Text(cfg["nombre"], size=22, weight="w800", color="#1e293b", text_align=ft.TextAlign.CENTER),
            ft.Text(cfg["sub"], size=13, weight="w500",
                    color=ft.Colors.with_opacity(0.7, color), text_align=ft.TextAlign.CENTER),
            ft.Container(expand=True),
            ft.Row([
                ft.Icon(ft.Icons.TOUCH_APP_ROUNDED, size=16, color="#94a3b8"),
                ft.Text("Clic para más info", size=12, color="#94a3b8", weight="w600"),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=6),
            ft.Container(height=20),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
        width=CARD_W, height=CARD_H,
    )

    card_front_container = ft.Container(
        content=ft.Stack([contenido_base, panel_deslizante]),
        animate_scale=ft.Animation(250, ft.AnimationCurve.EASE_OUT_CUBIC),
        scale=1.0,
        bgcolor=ft.Colors.with_opacity(0.85, "white"),  # Glassmorphism
        blur=ft.Blur(12, 12),
        border_radius=20,
        width=CARD_W, height=CARD_H,
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        shadow=_SHADOW_NORMAL,
    )

    # ── Botón ← regresar (arriba derecha) ──
    btn_back = ft.Container(
        content=ft.Icon(ft.Icons.ARROW_BACK_ROUNDED, size=20, color="white"),
        width=36, height=36, border_radius=18,
        bgcolor=ft.Colors.with_opacity(0.25, "white"),
        alignment=ft.Alignment(0, 0),
    )

    # ── Cara trasera ──
    cara_trasera_container = ft.Container(
        content=ft.Stack([
            # Contenido principal
            ft.Container(
                content=ft.Column([
                    ft.Container(height=44),  # espacio para el botón ←
                    ft.Icon(cfg["icono"], size=36, color=ft.Colors.with_opacity(0.3, "white")),
                    ft.Container(height=6),
                    ft.Text(cfg["nombre"], size=18, weight="w700", color="white", text_align=ft.TextAlign.CENTER),
                    ft.Container(height=10),
                    ft.Divider(height=1, color=ft.Colors.with_opacity(0.3, "white")),
                    ft.Container(height=10),
                    ft.Text(cfg["desc_larga"], size=13, color=ft.Colors.with_opacity(0.95, "white"),
                            text_align=ft.TextAlign.CENTER),
                    ft.Container(expand=True),
                    # Botón INGRESAR (ahora es el botón principal)
                    ft.Container(
                        content=ft.Row([
                            ft.Text("Ingresar", size=15, weight="w700", color=color),
                            ft.Icon(ft.Icons.ARROW_FORWARD_ROUNDED, size=20, color=color),
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=6),
                        bgcolor="white", border_radius=12,
                        padding=ft.Padding(36, 12, 36, 12),
                        shadow=[ft.BoxShadow(blur_radius=12,
                            color=ft.Colors.with_opacity(0.2, "black"), offset=ft.Offset(0, 4))],
                    ),
                    ft.Container(height=10),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
                padding=ft.Padding(24, 0, 24, 16),
            ),
            # Botón ← arriba derecha
            ft.Container(content=btn_back, top=12, left=12),
        ]),
        gradient=ft.LinearGradient(colors=[grad[0], color],
            begin=ft.Alignment.TOP_LEFT, end=ft.Alignment.BOTTOM_RIGHT),
        border_radius=20,
        width=CARD_W, height=CARD_H,
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        shadow=[ft.BoxShadow(blur_radius=40, spread_radius=0,
            color=ft.Colors.with_opacity(0.3, color), offset=ft.Offset(0, 16))],
    )

    # ── Keys para AnimatedSwitcher ──
    cara_frontal = ft.Container(content=card_front_container, key="frontal")
    cara_trasera = ft.Container(content=cara_trasera_container, key="trasera")

    # ── AnimatedSwitcher — SCALE con curvas suaves ──
    switcher = ft.AnimatedSwitcher(
        content=cara_frontal,
        transition=ft.AnimatedSwitcherTransition.SCALE,
        duration=400,
        switch_in_curve=ft.AnimationCurve.EASE_OUT_CUBIC,
        switch_out_curve=ft.AnimationCurve.EASE_IN_CUBIC,
    )

    # ── Eventos — updates selectivos ──
    def on_enter(e):
        nonlocal is_front
        if is_front:
            panel_deslizante.offset = ft.Offset(0, 0)
            card_front_container.scale = 1.05
            card_front_container.shadow = _SHADOW_HOVER
            card_front_container.update()
            panel_deslizante.update()

    def on_exit(e):
        nonlocal is_front
        if is_front:
            panel_deslizante.offset = ft.Offset(0, 1.0)
            card_front_container.scale = 1.0
            card_front_container.shadow = _SHADOW_NORMAL
            card_front_container.update()
            panel_deslizante.update()

    def flip_to_back(e):
        nonlocal is_front
        if is_front:
            panel_deslizante.offset = ft.Offset(0, 1.0)
            card_front_container.scale = 1.0
            card_front_container.shadow = _SHADOW_NORMAL
            switcher.content = cara_trasera
            is_front = False
            switcher.update()

    def flip_to_front(e):
        nonlocal is_front
        if not is_front:
            switcher.content = cara_frontal
            is_front = True
            switcher.update()

    btn_back.on_click = flip_to_front

    # ── GestureDetector — cursor CLICK ──
    return ft.GestureDetector(
        content=switcher,
        on_enter=on_enter,
        on_exit=on_exit,
        on_tap=flip_to_back,
        mouse_cursor=ft.MouseCursor.CLICK,
    )


def main(page: ft.Page):
    page.title = "Tarjetas PRO"
    page.bgcolor = "#f0fdf4"
    page.window.maximized = True
    page.padding = 0

    tarjetas = [crear_tarjeta_interactiva(page, cfg) for cfg in BRIGADAS]

    grid = ft.Column([
        ft.Row(tarjetas[:2], alignment=ft.MainAxisAlignment.CENTER, spacing=28),
        ft.Row(tarjetas[2:], alignment=ft.MainAxisAlignment.CENTER, spacing=28),
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=28)

    page.add(ft.Container(
        content=ft.Column([
            ft.Container(height=40),
            ft.Text("Tarjetas PRO", size=32, weight="w800", color="#1e293b", text_align=ft.TextAlign.CENTER),
            ft.Text("Hover desliza panel  •  Clic voltea  •  Cursor tipo botón", size=15,
                    color="#64748b", text_align=ft.TextAlign.CENTER),
            ft.Container(height=40),
            grid,
            ft.Container(height=40),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO),
        expand=True, bgcolor="#f0fdf4",
    ))

ft.run(main)
