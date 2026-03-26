"""
Demo Definitivo — Hover + Flip
Eventos directos en cada cara. Compatible con Flet 0.80.5.
"""
import flet as ft

BRIGADAS = [
    {"nombre": "Gestión de Riesgo", "sub": "y Primeros Auxilios", "icono": ft.Icons.HEALTH_AND_SAFETY,
     "color": "#dc2626", "grad": ["#b91c1c", "#dc2626"],
     "desc": "Gestión de emergencias, evacuación, simulacros y primeros auxilios ante desastres naturales y situaciones de riesgo."},
    {"nombre": "Patrulla Escolar", "sub": "Seguridad Vial", "icono": ft.Icons.TRAFFIC,
     "color": "#ea580c", "grad": ["#c2410c", "#ea580c"],
     "desc": "Seguridad vial, control de tránsito peatonal, protección de la comunidad escolar en zonas de alto riesgo."},
    {"nombre": "Convivencia y Paz", "sub": "Prevención Integral", "icono": ft.Icons.HANDSHAKE,
     "color": "#64748b", "grad": ["#475569", "#64748b"],
     "desc": "Mediación de conflictos, cultura de paz, prevención de violencia escolar y promoción de valores de convivencia."},
    {"nombre": "Brigada Ecológica", "sub": "Medio Ambiente", "icono": ft.Icons.ECO,
     "color": "#059669", "grad": ["#047857", "#059669"],
     "desc": "Conservación ambiental, reciclaje, reforestación, cuidado del agua y educación ecológica en la comunidad."},
]

CARD_W = 340
CARD_H = 320


def crear_tarjeta_interactiva(page: ft.Page, cfg: dict):
    color = cfg["color"]
    grad = cfg["grad"]

    # ── Panel deslizante (flotante, oculto con offset) ──
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
        animate_offset=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
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
                ft.Text("Haz clic para expandir", size=12, color="#94a3b8", weight="w600"),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=6),
            ft.Container(height=20),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
        width=CARD_W, height=CARD_H,
    )

    cara_frontal = ft.Container(
        content=ft.Stack([contenido_base, panel_deslizante]),
        key="frontal",
        animate_scale=ft.Animation(250, ft.AnimationCurve.EASE_OUT),
        scale=1.0,
        bgcolor="white",
        border_radius=20,
        width=CARD_W, height=CARD_H,
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        shadow=[ft.BoxShadow(blur_radius=30, spread_radius=-4,
            color=ft.Colors.with_opacity(0.12, "#1e293b"), offset=ft.Offset(0, 12))],
        ink=False,
    )

    # ── Cara trasera ──
    cara_trasera = ft.Container(
        content=ft.Column([
            ft.Container(height=12),
            ft.Icon(cfg["icono"], size=40, color=ft.Colors.with_opacity(0.3, "white")),
            ft.Container(height=8),
            ft.Text(cfg["nombre"], size=20, weight="w700", color="white", text_align=ft.TextAlign.CENTER),
            ft.Container(height=12),
            ft.Divider(height=1, color=ft.Colors.with_opacity(0.3, "white")),
            ft.Container(height=12),
            ft.Text(cfg["desc"], size=14, color=ft.Colors.with_opacity(0.95, "white"),
                    text_align=ft.TextAlign.CENTER),
            ft.Container(expand=True),
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.ARROW_BACK_ROUNDED, size=18, color=color),
                    ft.Text("Regresar", size=14, weight="w700", color=color),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=6),
                bgcolor="white", border_radius=12,
                padding=ft.Padding(28, 10, 28, 10),
            ),
            ft.Container(height=10),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
        key="trasera",
        gradient=ft.LinearGradient(colors=[grad[0], color],
            begin=ft.Alignment.TOP_LEFT, end=ft.Alignment.BOTTOM_RIGHT),
        border_radius=20,
        padding=ft.Padding(24, 16, 24, 16),
        width=CARD_W, height=CARD_H,
        shadow=[ft.BoxShadow(blur_radius=40, spread_radius=0,
            color=ft.Colors.with_opacity(0.3, color), offset=ft.Offset(0, 16))],
    )

    # ── AnimatedSwitcher (requiere content en Flet 0.80.5) ──
    switcher = ft.AnimatedSwitcher(
        content=cara_frontal,
        transition=ft.AnimatedSwitcherTransition.SCALE,
        duration=400,
        switch_in_curve=ft.AnimationCurve.EASE_OUT_BACK,
        switch_out_curve=ft.AnimationCurve.EASE_IN_BACK,
    )

    # ── Eventos directos en cada cara ──
    def hover_frontal(e):
        hov = e.data == "true"
        panel_deslizante.offset = ft.Offset(0, 0) if hov else ft.Offset(0, 1.0)
        cara_frontal.scale = 1.03 if hov else 1.0
        cara_frontal.update()

    def voltear_a_trasera(e):
        panel_deslizante.offset = ft.Offset(0, 1.0)
        cara_frontal.scale = 1.0
        switcher.content = cara_trasera
        switcher.update()

    def voltear_a_frontal(e):
        switcher.content = cara_frontal
        switcher.update()

    cara_frontal.on_hover = hover_frontal
    cara_frontal.on_click = voltear_a_trasera
    cara_trasera.on_click = voltear_a_frontal

    return switcher


def main(page: ft.Page):
    page.title = "Tarjetas Definitivas"
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
            ft.Text("Tarjetas Definitivas", size=32, weight="w800", color="#1e293b", text_align=ft.TextAlign.CENTER),
            ft.Text("Hover → panel desliza  •  Clic → voltea la tarjeta", size=15, color="#64748b", text_align=ft.TextAlign.CENTER),
            ft.Container(height=40),
            grid,
            ft.Container(height=40),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO),
        expand=True, bgcolor="#f0fdf4",
    ))

ft.run(main)
