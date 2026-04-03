"""
Pantalla — Selección de Brigada.
Fondo animado (reutiliza estilo del login) + tarjetas overlay glassmorphism.
Las 4 brigadas son fijas (predefinidas por el Ministerio de Educación).
"""

import asyncio
import flet as ft
from theme import (
    BRIGADAS,
    COLOR_FONDO_VERDE,
    COLOR_TEXTO,
    COLOR_TEXTO_SEC,
    COLOR_PRIMARIO,
    COLOR_PRIMARIO_CLARO,
    COLOR_VERDE_SUAVE,
    COLOR_CARD,
)

# ─── Colores de blobs decorativos ───
_GLOW_AZUL = "#60a5fa"
_GLOW_MORADO = "#c084fc"
_GLOW_VERDE = "#4ade80"
_GLOW_AMBAR = "#FCD34D"

# ─── Partículas verdes ───
_VERDES = [
    "#065f46", "#047857", COLOR_PRIMARIO, COLOR_PRIMARIO_CLARO,
    "#34d399", "#6ee7b7", "#86efac", "#a7f3d0", COLOR_VERDE_SUAVE,
]


def _crear_blob(color: str, top: float, left: float, size: float) -> ft.Container:
    """Esfera grande difuminada de fondo (misma técnica que el login)."""
    escala = max(size / 50, 1)
    foco = ft.Container(
        width=12, height=12, border_radius=6,
        bgcolor=ft.Colors.TRANSPARENT,
        shadow=[
            ft.BoxShadow(blur_radius=int(15 * escala), spread_radius=int(5 * escala),
                         color=ft.Colors.with_opacity(0.9, color), offset=ft.Offset(0, 0)),
            ft.BoxShadow(blur_radius=int(30 * escala), spread_radius=int(10 * escala),
                         color=ft.Colors.with_opacity(0.6, color), offset=ft.Offset(0, 0)),
            ft.BoxShadow(blur_radius=int(42 * escala), spread_radius=int(8 * escala),
                         color=ft.Colors.with_opacity(0.3, color), offset=ft.Offset(0, 0)),
        ],
    )
    return ft.Container(
        content=foco, width=size, height=size, top=top, left=left,
        alignment=ft.Alignment(0.5, 0.5), clip_behavior=ft.ClipBehavior.NONE,
    )


class _FloatingElement(ft.Container):
    """Elemento que flota suavemente en el fondo."""

    def __init__(self, content, top, left, step_top=15, step_left=0, **kwargs):
        super().__init__(
            content=content, top=top, left=left,
            animate_position=ft.Animation(2000, ft.AnimationCurve.EASE_IN_OUT),
            **kwargs,
        )
        self.base_top = top
        self.base_left = left
        self.step_top = step_top
        self.step_left = step_left
        self.floating_phase = True

    def animate_float(self):
        if self.floating_phase:
            self.top = self.base_top + self.step_top
            self.left = self.base_left + self.step_left
        else:
            self.top = self.base_top - self.step_top
            self.left = self.base_left - self.step_left
        self.floating_phase = not self.floating_phase


def _crear_particula(color: str, size: float) -> ft.Container:
    return ft.Container(
        width=size, height=size, border_radius=size / 2,
        bgcolor=ft.Colors.with_opacity(0.9, color),
    )


# ─── Config de las 4 brigadas (fijas) ───
_CARD_W = 340
_CARD_H = 360

_SHADOW_NORMAL = [ft.BoxShadow(blur_radius=30, spread_radius=-4,
    color=ft.Colors.with_opacity(0.12, "#1e293b"), offset=ft.Offset(0, 12))]
_SHADOW_HOVER = [ft.BoxShadow(blur_radius=40, spread_radius=-6,
    color=ft.Colors.with_opacity(0.2, "#1e293b"), offset=ft.Offset(0, 18))]

_BRIGADAS_CONFIG = [
    {
        "key": "riesgo",
        "icono": ft.Icons.HEALTH_AND_SAFETY,
        "color": "#dc2626",
        "grad": ["#b91c1c", "#dc2626"],
        "nombre": "Gestión de Riesgo",
        "sub": "y Primeros Auxilios",
        "desc": "Gestión de emergencias, evacuación, simulacros y primeros auxilios ante desastres naturales.",
        "desc_larga": "Formación en prevención y respuesta ante emergencias y desastres naturales. Incluye planificación de rutas de evacuación, ejecución de simulacros, técnicas de primeros auxilios, manejo de extintores y coordinación con organismos de protección civil.",
    },
    {
        "key": "patrulla",
        "icono": ft.Icons.TRAFFIC,
        "color": "#ea580c",
        "grad": ["#c2410c", "#ea580c"],
        "nombre": "Patrulla Escolar",
        "sub": "Seguridad Vial",
        "desc": "Seguridad vial, control de tránsito peatonal y protección de la comunidad escolar.",
        "desc_larga": "Educación en normas de tránsito y seguridad vial. Los estudiantes aprenden señalización, control de cruces peatonales, organización del flujo vehicular en horas de entrada y salida, y campañas de concientización sobre el uso del cinturón y el respeto a las señales.",
    },
    {
        "key": "convivencia",
        "icono": ft.Icons.HANDSHAKE,
        "color": "#64748b",
        "grad": ["#475569", "#64748b"],
        "nombre": "Convivencia y Paz",
        "sub": "Prevención Integral",
        "desc": "Mediación de conflictos, cultura de paz y prevención de violencia escolar.",
        "desc_larga": "Promoción de la convivencia pacífica y prevención de la violencia. Incluye mediación de conflictos entre estudiantes, talleres de comunicación asertiva, campañas contra el bullying, fortalecimiento de valores como el respeto, la tolerancia y la solidaridad.",
    },
    {
        "key": "ecologica",
        "icono": ft.Icons.ECO,
        "color": "#059669",
        "grad": ["#047857", "#059669"],
        "nombre": "Brigada Ecológica",
        "sub": "Medio Ambiente",
        "desc": "Conservación ambiental, reciclaje, reforestación y educación ecológica.",
        "desc_larga": "Cuidado y preservación del medio ambiente escolar y comunitario. Actividades de reciclaje, huertos escolares, jornadas de reforestación, ahorro de agua y energía, y campañas de sensibilización ambiental para toda la comunidad educativa.",
    },
]


def _crear_tarjeta(page: ft.Page, cfg: dict, on_select):
    """Crea una tarjeta interactiva con hover (panel deslizante) y clic (flip)."""
    color = cfg["color"]
    grad = cfg["grad"]
    is_front = True

    # ── Panel deslizante (hover) ──
    panel_deslizante = ft.Container(
        content=ft.Column([
            ft.Text("Resumen", size=14, weight="w800", color="white", font_family="Outfit"),
            ft.Text(cfg["desc"], size=13, color=ft.Colors.with_opacity(0.9, "white"),
                    max_lines=3, overflow=ft.TextOverflow.ELLIPSIS, font_family="Outfit"),
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
            ft.Text(cfg["nombre"], size=22, weight="w800", color=COLOR_TEXTO,
                    text_align=ft.TextAlign.CENTER, font_family="Outfit"),
            ft.Text(cfg["sub"], size=13, weight="w500",
                    color=ft.Colors.with_opacity(0.7, color),
                    text_align=ft.TextAlign.CENTER, font_family="Outfit"),
            ft.Container(expand=True),
            ft.Row([
                ft.Icon(ft.Icons.TOUCH_APP_ROUNDED, size=16, color=COLOR_TEXTO_SEC),
                ft.Text("Clic para más info", size=12, color=COLOR_TEXTO_SEC,
                        weight="w600", font_family="Outfit"),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=6),
            ft.Container(height=20),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
        width=_CARD_W, height=_CARD_H,
    )

    card_front = ft.Container(
        content=ft.Stack([contenido_base, panel_deslizante]),
        animate_scale=ft.Animation(250, ft.AnimationCurve.EASE_OUT_CUBIC),
        scale=1.0,
        bgcolor=ft.Colors.with_opacity(0.85, COLOR_CARD),
        blur=ft.Blur(12, 12),
        border_radius=20,
        width=_CARD_W, height=_CARD_H,
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        shadow=_SHADOW_NORMAL,
    )

    # ── Botón ← regresar (arriba izquierda) ──
    btn_back = ft.Container(
        content=ft.Icon(ft.Icons.ARROW_BACK_ROUNDED, size=20, color="white"),
        width=36, height=36, border_radius=18,
        bgcolor=ft.Colors.with_opacity(0.25, "white"),
        alignment=ft.Alignment(0, 0),
    )

    # ── Botón Ingresar (cara trasera) ──
    btn_ingresar = ft.Container(
        content=ft.Row([
            ft.Text("Ingresar", size=15, weight="w700", color=color, font_family="Outfit"),
            ft.Icon(ft.Icons.ARROW_FORWARD_ROUNDED, size=20, color=color),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=6),
        bgcolor="white", border_radius=12,
        padding=ft.Padding(36, 12, 36, 12),
        shadow=[ft.BoxShadow(blur_radius=12,
            color=ft.Colors.with_opacity(0.2, "black"), offset=ft.Offset(0, 4))],
        on_click=lambda _: on_select(cfg["key"]),
    )

    # ── Cara trasera ──
    cara_trasera_container = ft.Container(
        content=ft.Stack([
            ft.Container(
                content=ft.Column([
                    ft.Container(height=44),
                    ft.Icon(cfg["icono"], size=36, color=ft.Colors.with_opacity(0.3, "white")),
                    ft.Container(height=6),
                    ft.Text(cfg["nombre"], size=18, weight="w700", color="white",
                            text_align=ft.TextAlign.CENTER, font_family="Outfit"),
                    ft.Container(height=10),
                    ft.Divider(height=1, color=ft.Colors.with_opacity(0.3, "white")),
                    ft.Container(height=10),
                    ft.Text(cfg["desc_larga"], size=13, color=ft.Colors.with_opacity(0.95, "white"),
                            text_align=ft.TextAlign.CENTER, font_family="Outfit"),
                    ft.Container(expand=True),
                    btn_ingresar,
                    ft.Container(height=10),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
                padding=ft.Padding(24, 0, 24, 16),
            ),
            ft.Container(content=btn_back, top=12, left=12),
        ]),
        gradient=ft.LinearGradient(colors=[grad[0], color],
            begin=ft.Alignment.TOP_LEFT, end=ft.Alignment.BOTTOM_RIGHT),
        border_radius=20,
        width=_CARD_W, height=_CARD_H,
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        shadow=[ft.BoxShadow(blur_radius=40, spread_radius=0,
            color=ft.Colors.with_opacity(0.3, color), offset=ft.Offset(0, 16))],
    )

    # ── Keys + AnimatedSwitcher ──
    cara_frontal = ft.Container(content=card_front, key="frontal")
    cara_trasera = ft.Container(content=cara_trasera_container, key="trasera")

    switcher = ft.AnimatedSwitcher(
        content=cara_frontal,
        transition=ft.AnimatedSwitcherTransition.SCALE,
        duration=400,
        switch_in_curve=ft.AnimationCurve.EASE_OUT_CUBIC,
        switch_out_curve=ft.AnimationCurve.EASE_IN_CUBIC,
    )

    # ── Eventos ──
    def on_enter(e):
        nonlocal is_front
        if is_front:
            panel_deslizante.offset = ft.Offset(0, 0)
            card_front.scale = 1.05
            card_front.shadow = _SHADOW_HOVER
            card_front.update()
            panel_deslizante.update()

    def on_exit(e):
        nonlocal is_front
        if is_front:
            panel_deslizante.offset = ft.Offset(0, 1.0)
            card_front.scale = 1.0
            card_front.shadow = _SHADOW_NORMAL
            card_front.update()
            panel_deslizante.update()

    def flip_to_back(e):
        nonlocal is_front
        if is_front:
            panel_deslizante.offset = ft.Offset(0, 1.0)
            card_front.scale = 1.0
            card_front.shadow = _SHADOW_NORMAL
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

    return ft.GestureDetector(
        content=switcher,
        on_enter=on_enter,
        on_exit=on_exit,
        on_tap=flip_to_back,
        mouse_cursor=ft.MouseCursor.CLICK,
    )


def build(page: ft.Page, on_select) -> ft.Control:
    """Pantalla de selección con fondo animado y tarjetas overlay."""

    # ── Nombre de la institución ──
    try:
        _data = (page.data or {}).get("usuario_actual", {}) if isinstance(page.data, dict) else {}
        inst_nombre = _data.get("institucion_nombre", "")
    except Exception:
        inst_nombre = ""

    # ═══════════════════════════════════════════
    #  FONDO ANIMADO (igual que el login)
    # ═══════════════════════════════════════════
    background_blobs = [
        _crear_blob(_GLOW_AZUL, 30, -60, 320),
        _crear_blob(_GLOW_AMBAR, 80, 1100, 260),
        _crear_blob(_GLOW_VERDE, 550, 80, 300),
        _crear_blob(_GLOW_MORADO, 450, 1150, 260),
        _crear_blob("#dc2626", 300, 600, 200),
    ]

    # Partículas flotantes
    config_particulas = [
        (180, 200, 12, 0), (100, 130, 0, 14), (60, 1050, -10, 8),
        (130, 1200, 8, -10), (330, 320, -8, -8), (480, 950, 10, 12),
        (620, 180, -12, 6), (680, 850, 6, -12), (580, 1250, -6, 10),
        (400, 500, -8, 10), (250, 700, 10, -6),
    ]
    particulas_animadas = []
    for i, (top, left, st, sl) in enumerate(config_particulas):
        color = _VERDES[i % len(_VERDES)]
        particulas_animadas.append(
            _FloatingElement(
                content=_crear_particula(color, 14),
                top=top, left=left, step_top=st, step_left=sl,
            )
        )

    # Iconos flotantes decorativos
    icon_shield = _FloatingElement(
        content=ft.Icon(ft.Icons.SHIELD_ROUNDED, size=200,
                        color=ft.Colors.with_opacity(0.08, COLOR_PRIMARIO)),
        top=60, left=1100, step_top=10, step_left=-5,
    )
    icon_school = _FloatingElement(
        content=ft.Icon(ft.Icons.SCHOOL_ROUNDED, size=160,
                        color=ft.Colors.with_opacity(0.08, _GLOW_MORADO)),
        top=500, left=50, step_top=-8, step_left=6,
    )

    # Animación de fondo
    async def animate_background():
        while True:
            try:
                icon_shield.animate_float()
                icon_school.animate_float()
                for p in particulas_animadas:
                    p.animate_float()
                if page.controls:
                    page.update()
            except Exception:
                break
            await asyncio.sleep(2.1)

    page.run_task(animate_background)

    # ═══════════════════════════════════════════
    #  HEADER
    # ═══════════════════════════════════════════
    header_items = [
        ft.Text(
            "Sistema de Brigadas Escolares",
            size=36, weight="w800", color=COLOR_TEXTO,
            font_family="Outfit",
            text_align=ft.TextAlign.CENTER,
        ),
    ]
    if inst_nombre:
        header_items.append(ft.Container(height=4))
        header_items.append(
            ft.Text(inst_nombre, size=20, weight="w600", color=COLOR_TEXTO,
                    text_align=ft.TextAlign.CENTER, italic=True, font_family="Outfit")
        )
    header_items.append(ft.Container(height=8))
    header_items.append(
        ft.Text(
            "Seleccione el tipo de brigada",
            size=18, color=COLOR_TEXTO_SEC,
            text_align=ft.TextAlign.CENTER, font_family="Outfit",
        )
    )

    header = ft.Column(
        header_items,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0,
    )

    # ═══════════════════════════════════════════
    #  TARJETAS INTERACTIVAS — HOVER + FLIP
    # ═══════════════════════════════════════════
    tarjetas = [_crear_tarjeta(page, cfg, on_select) for cfg in _BRIGADAS_CONFIG]

    grid = ft.Column([
        ft.Row(tarjetas[:2], alignment=ft.MainAxisAlignment.CENTER, spacing=28),
        ft.Row(tarjetas[2:], alignment=ft.MainAxisAlignment.CENTER, spacing=28),
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=28)

    # ═══════════════════════════════════════════
    #  COMPOSICIÓN FINAL
    # ═══════════════════════════════════════════
    from auth_theme_toggle import create_auth_theme_toggle
    btn_theme = create_auth_theme_toggle(page)

    content_layer = ft.Container(
        content=ft.Column(
            [
                ft.Container(height=32),
                header,
                ft.Container(height=32),
                grid,
                ft.Container(height=24),
                ft.Text("© 2026 Sistema de Brigadas Escolares", size=11,
                         color=COLOR_TEXTO_SEC, font_family="Outfit"),
                ft.Container(height=16),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
        ),
        alignment=ft.Alignment(0, 0),
        expand=True,
    )

    return ft.Stack(
        [
            ft.Container(expand=True, bgcolor=COLOR_FONDO_VERDE),
            *background_blobs,
            icon_shield,
            icon_school,
            *particulas_animadas,
            content_layer,
            btn_theme,
        ],
        expand=True,
    )
