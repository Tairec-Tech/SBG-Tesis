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
    COLOR_BORDE,
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
_BRIGADAS_CONFIG = [
    {
        "key": "riesgo",
        "icono": ft.Icons.HEALTH_AND_SAFETY,
        "color_primario": "#dc2626",
        "color_oscuro": "#991b1b",
        "gradient": ["#b91c1c", "#dc2626"],
        "nombre": "Gestión de Riesgo",
        "sub": "y Primeros Auxilios",
        "descripcion": "Gestión de emergencias, evacuación, simulacros y primeros auxilios ante desastres naturales y situaciones de riesgo.",
    },
    {
        "key": "patrulla",
        "icono": ft.Icons.TRAFFIC,
        "color_primario": "#ea580c",
        "color_oscuro": "#9a3412",
        "gradient": ["#c2410c", "#ea580c"],
        "nombre": "Patrulla Escolar",
        "sub": "Seguridad Vial",
        "descripcion": "Seguridad vial, control de tránsito peatonal, protección de la comunidad escolar en zonas de alto riesgo.",
    },
    {
        "key": "convivencia",
        "icono": ft.Icons.HANDSHAKE,
        "color_primario": "#64748b",
        "color_oscuro": "#334155",
        "gradient": ["#475569", "#64748b"],
        "nombre": "Convivencia y Paz",
        "sub": "Prevención Integral",
        "descripcion": "Mediación de conflictos, cultura de paz, prevención de violencia escolar y promoción de valores de convivencia.",
    },
    {
        "key": "ecologica",
        "icono": ft.Icons.ECO,
        "color_primario": "#059669",
        "color_oscuro": "#065f46",
        "gradient": ["#047857", "#059669"],
        "nombre": "Brigada Ecológica",
        "sub": "Medio Ambiente",
        "descripcion": "Conservación ambiental, reciclaje, reforestación, cuidado del agua y educación ecológica en la comunidad.",
    },
]


def build(page: ft.Page, on_select) -> ft.Control:
    """Pantalla de selección con fondo animado y tarjetas overlay."""

    # ── Nombre de la institución ──
    try:
        _data = (page.data or {}).get("usuario_actual", {}) if isinstance(page.data, dict) else {}
        inst_nombre = _data.get("institucion_nombre", "")
    except Exception:
        inst_nombre = ""

    def _on_click(key):
        def handler(_):
            on_select(key)
        return handler

    # ═══════════════════════════════════════════
    #  FONDO ANIMADO (igual que el login)
    # ═══════════════════════════════════════════
    background_blobs = [
        _crear_blob(_GLOW_AZUL, 30, -60, 320),
        _crear_blob(_GLOW_AMBAR, 80, 1100, 260),
        _crear_blob(_GLOW_VERDE, 550, 80, 300),
        _crear_blob(_GLOW_MORADO, 450, 1150, 260),
        _crear_blob("#dc2626", 300, 600, 200),  # toque rojo para brigada Riesgo
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

    # Animación de fondo + glow pulsante de iconos
    icon_glow_refs = []

    async def animate_background():
        glow_phase = True
        while True:
            try:
                icon_shield.animate_float()
                icon_school.animate_float()
                for p in particulas_animadas:
                    p.animate_float()
                # Pulso de glow en los íconos de las tarjetas
                for g in icon_glow_refs:
                    if glow_phase:
                        g.shadow = [ft.BoxShadow(blur_radius=45, spread_radius=10,
                            color=g.data, offset=ft.Offset(0, 0))]
                    else:
                        g.shadow = [ft.BoxShadow(blur_radius=25, spread_radius=3,
                            color=g.data, offset=ft.Offset(0, 0))]
                glow_phase = not glow_phase
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
            ft.Text(inst_nombre, size=16, color=COLOR_TEXTO_SEC,
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
    #  TARJETAS OVERLAY GLASSMORPHISM — PREMIUM
    # ═══════════════════════════════════════════
    cards = []
    card_refs = []

    for idx, cfg in enumerate(_BRIGADAS_CONFIG):
        desc_text = ft.Text(
            cfg["descripcion"], size=13, color=COLOR_TEXTO_SEC,
            text_align=ft.TextAlign.CENTER, font_family="Outfit",
            max_lines=2, overflow=ft.TextOverflow.ELLIPSIS,
        )

        # Glow pulsante detrás del ícono (el 'data' guarda el color para la animación)
        glow_color = ft.Colors.with_opacity(0.5, cfg["color_primario"])
        icon_glow = ft.Container(
            width=90, height=90, border_radius=45,
            bgcolor=ft.Colors.TRANSPARENT,
            shadow=[ft.BoxShadow(blur_radius=20, spread_radius=3,
                color=glow_color, offset=ft.Offset(0, 0))],
            animate=ft.Animation(1800, ft.AnimationCurve.EASE_IN_OUT),
            data=glow_color,  # almacenar color para la animación
        )
        icon_glow_refs.append(icon_glow)

        icon_circle = ft.Container(
            content=ft.Icon(cfg["icono"], color="white", size=44),
            width=90, height=90, border_radius=45,
            gradient=ft.LinearGradient(
                colors=cfg["gradient"],
                begin=ft.Alignment.TOP_LEFT,
                end=ft.Alignment.BOTTOM_RIGHT,
            ),
            alignment=ft.Alignment(0, 0),
            shadow=[ft.BoxShadow(blur_radius=20, spread_radius=0,
                color=ft.Colors.with_opacity(0.45, cfg["color_primario"]),
                offset=ft.Offset(0, 10))],
        )

        icon_stack = ft.Container(
            content=ft.Stack([icon_glow, icon_circle], alignment=ft.Alignment(0, 0)),
            width=95, height=95,
        )

        card_content = ft.Column([
            icon_stack,
            ft.Container(height=14),
            ft.Text(cfg["nombre"], size=24, weight="w800", color=COLOR_TEXTO,
                    text_align=ft.TextAlign.CENTER, font_family="Outfit"),
            ft.Container(height=4),
            ft.Text(cfg["sub"], size=14, weight="w500",
                    color=ft.Colors.with_opacity(0.7, cfg["color_primario"]),
                    text_align=ft.TextAlign.CENTER, font_family="Outfit"),
            ft.Container(height=8),
            desc_text,
            ft.Container(height=14),
            # Botón "Ingresar"
            ft.Container(
                content=ft.Row([
                    ft.Text("Ingresar", size=14, weight="w700", color="white", font_family="Outfit"),
                    ft.Icon(ft.Icons.ARROW_FORWARD_ROUNDED, size=18, color="white"),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=6),
                bgcolor=cfg["color_primario"],
                border_radius=10,
                padding=ft.Padding(32, 10, 32, 10),
                shadow=[ft.BoxShadow(blur_radius=16, spread_radius=0,
                    color=ft.Colors.with_opacity(0.35, cfg["color_primario"]),
                    offset=ft.Offset(0, 6))],
            ),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)

        # Banda decorativa superior con gradiente triple
        top_bar = ft.Container(
            height=6, border_radius=ft.BorderRadius(3, 3, 0, 0),
            gradient=ft.LinearGradient(
                colors=[cfg["color_primario"], cfg["color_oscuro"], cfg["color_primario"]],
                begin=ft.Alignment(-1, 0), end=ft.Alignment(1, 0)),
        )

        # Tarjeta glassmorphism — grande y premium
        card = ft.Container(
            content=ft.Column([
                top_bar,
                ft.Container(content=card_content, padding=ft.Padding(24, 20, 24, 24)),
            ], spacing=0),
            bgcolor=ft.Colors.with_opacity(0.88, COLOR_CARD),
            blur=ft.Blur(18, 18),
            border_radius=24,
            border=ft.Border.all(1.5, ft.Colors.with_opacity(0.25, COLOR_BORDE)),
            shadow=[
                ft.BoxShadow(blur_radius=48, spread_radius=-6,
                    color=ft.Colors.with_opacity(0.18, COLOR_TEXTO), offset=ft.Offset(0, 20)),
                ft.BoxShadow(blur_radius=16, spread_radius=0,
                    color=ft.Colors.with_opacity(0.06, COLOR_TEXTO), offset=ft.Offset(0, 8)),
            ],
            width=340,
            on_click=_on_click(cfg["key"]),
            ink=True,
            # Animación de entrada
            opacity=0,
            offset=ft.Offset(0, 0.15),
            animate_opacity=ft.Animation(600 + idx * 150, ft.AnimationCurve.EASE_OUT),
            animate_offset=ft.Animation(600 + idx * 150, ft.AnimationCurve.EASE_OUT),
            scale=1.0,
            animate_scale=ft.Animation(250, ft.AnimationCurve.EASE_OUT),
        )

        # Hover dramático
        def _make_hover(card_ref, color):
            def handler(e):
                is_hover = e.data == "true"
                card_ref.scale = 1.06 if is_hover else 1.0
                card_ref.shadow = [
                    ft.BoxShadow(blur_radius=60 if is_hover else 48,
                        spread_radius=4 if is_hover else -6,
                        color=ft.Colors.with_opacity(0.4 if is_hover else 0.18, color),
                        offset=ft.Offset(0, 24 if is_hover else 20)),
                    ft.BoxShadow(blur_radius=20 if is_hover else 16,
                        spread_radius=0,
                        color=ft.Colors.with_opacity(0.1, COLOR_TEXTO),
                        offset=ft.Offset(0, 8)),
                ]
                card_ref.border = ft.Border.all(
                    2.5 if is_hover else 1.5,
                    ft.Colors.with_opacity(0.6 if is_hover else 0.25,
                        color if is_hover else COLOR_BORDE))
                try:
                    if page.controls:
                        page.update()
                except Exception:
                    pass
            return handler

        card.on_hover = _make_hover(card, cfg["color_primario"])
        cards.append(card)
        card_refs.append(card)

    # Grid 2x2
    grid = ft.Column([
        ft.Row(cards[:2], alignment=ft.MainAxisAlignment.CENTER, spacing=32),
        ft.Row(cards[2:], alignment=ft.MainAxisAlignment.CENTER, spacing=32),
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=32)

    # ═══════════════════════════════════════════
    #  ANIMACIÓN DE ENTRADA ESCALONADA
    # ═══════════════════════════════════════════
    async def _animar_entrada():
        await asyncio.sleep(0.3)
        for i, card in enumerate(card_refs):
            card.opacity = 1.0
            card.offset = ft.Offset(0, 0)
            page.update()
            await asyncio.sleep(0.15)

    page.run_task(_animar_entrada)

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
