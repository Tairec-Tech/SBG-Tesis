import asyncio
import flet as ft
from auth_theme_toggle import create_auth_theme_toggle
from theme import (
    COLOR_PRIMARIO,
    COLOR_PRIMARIO_CLARO,
    COLOR_TEXTO,
    COLOR_TEXTO_SEC,
    COLOR_CARD,
    COLOR_BORDE,
    COLOR_FONDO_VERDE,
    COLOR_VERDE_SUAVE,
)

# Colores de las esferas de fondo
GLOW_AZUL = "#60a5fa"
GLOW_MORADO = "#c084fc"
GLOW_VERDE = "#4ade80"


def _crear_blob(color: str, top: float, left: float, size: float) -> ft.Container:
    """Esfera grande de fondo (misma técnica)."""
    escala = max(size / 50, 1)
    foco = ft.Container(
        width=12,
        height=12,
        border_radius=6,
        bgcolor=ft.Colors.TRANSPARENT,
        shadow=[
            ft.BoxShadow(blur_radius=int(15 * escala), spread_radius=int(5 * escala), color=ft.Colors.with_opacity(0.9, color), offset=ft.Offset(0, 0)),
            ft.BoxShadow(blur_radius=int(30 * escala), spread_radius=int(10 * escala), color=ft.Colors.with_opacity(0.6, color), offset=ft.Offset(0, 0)),
            ft.BoxShadow(blur_radius=int(42 * escala), spread_radius=int(8 * escala), color=ft.Colors.with_opacity(0.3, color), offset=ft.Offset(0, 0)),
        ],
    )
    return ft.Container(
        content=foco,
        width=size,
        height=size,
        top=top,
        left=left,
        alignment=ft.Alignment(0.5, 0.5),
        clip_behavior=ft.ClipBehavior.NONE,
    )


def _crear_particula_visual(color: str, size: float, blur: float = 0) -> ft.Container:
    """Solo el círculo, para content de FloatingElement."""
    c = ft.Container(
        width=size,
        height=size,
        border_radius=size / 2,
        bgcolor=ft.Colors.with_opacity(0.9, color),
    )
    if blur > 0:
        c.blur = ft.Blur(blur, blur)
    return c


class FloatingElement(ft.Container):
    """Elemento que flota suavemente. step_top/step_left definen la dirección."""

    def __init__(self, content, top, left, step_top=15, step_left=0, **kwargs):
        super().__init__(
            content=content,
            top=top,
            left=left,
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


def build(page: ft.Page, on_back_to_login) -> ft.Control:
    campo_email = ft.TextField(
        label="Correo Electrónico",
        hint_text="Ingrese su correo electrónico",
        hint_style=ft.TextStyle(size=14, color=COLOR_TEXTO_SEC),
        text_style=ft.TextStyle(size=14, color=COLOR_TEXTO),
        border_color=COLOR_BORDE,
        focused_border_color=COLOR_PRIMARIO,
        cursor_color=COLOR_PRIMARIO,
        width=320,
        border_radius=12,
    )

    def on_recuperar(_):
        page.snack_bar = ft.SnackBar(ft.Text("Si el correo existe, recibirá instrucciones (pendiente conectar BD)."))
        page.snack_bar.open = True
        page.update()

    header = ft.Column(
        [
            ft.Container(
                content=ft.Icon(ft.Icons.SHIELD_ROUNDED, size=56, color=COLOR_PRIMARIO),
                width=88,
                height=88,
                border_radius=44,
                bgcolor=COLOR_CARD,
                border=ft.Border.all(2, COLOR_BORDE),
                alignment=ft.Alignment.CENTER,
            ),
            ft.Container(height=16),
            ft.Text("Sistema de Brigadas Escolares", size=26, weight="bold", color=COLOR_TEXTO, text_align=ft.TextAlign.CENTER),
            ft.Container(height=6),
            ft.Text("Plataforma Digital para Coordinación de Brigadas", size=14, color=COLOR_TEXTO_SEC, text_align=ft.TextAlign.CENTER),
            ft.Container(height=4),
            ft.Text("Municipio Maracaibo", size=12, color=COLOR_TEXTO_SEC, text_align=ft.TextAlign.CENTER),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0,
    )

    card = ft.Container(
        content=ft.Column(
            [
                ft.Text("Correo Electrónico", size=14, weight="w500", color=COLOR_TEXTO),
                ft.Container(height=8),
                campo_email,
                ft.Container(height=24),
                ft.FilledButton(
                    content=ft.Text("Recuperar Contraseña", size=16, weight="w600"),
                    style=ft.ButtonStyle(color="white", bgcolor=COLOR_PRIMARIO, shape=ft.RoundedRectangleBorder(radius=12), padding=ft.Padding.symmetric(vertical=16, horizontal=24)),
                    width=320,
                    on_click=on_recuperar,
                ),
                ft.Container(height=20),
                ft.TextButton(
                    content=ft.Row(
                        [ft.Icon(ft.Icons.ARROW_BACK, size=18, color=COLOR_PRIMARIO), ft.Text("← Volver al Login", size=14, color=COLOR_PRIMARIO)],
                        spacing=8,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    on_click=lambda e: on_back_to_login(),
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
        ),
        bgcolor=ft.Colors.with_opacity(0.85, COLOR_CARD),
        blur=ft.Blur(15, 15),
        padding=ft.Padding.all(40),
        border_radius=35,
        border=ft.Border.all(1.5, ft.Colors.with_opacity(0.3, COLOR_BORDE)),
        shadow=[
            ft.BoxShadow(blur_radius=60, spread_radius=-8, color=ft.Colors.with_opacity(0.2, COLOR_TEXTO), offset=ft.Offset(0, 28)),
            ft.BoxShadow(blur_radius=16, spread_radius=0, color=ft.Colors.with_opacity(0.08, COLOR_TEXTO), offset=ft.Offset(0, 12)),
        ],
        width=420,
    )

    # --- Fondo animado (Blobs + Partículas, distribución distinta al Login/Registro) ---
    background_blobs = [
        _crear_blob(GLOW_AZUL, 150, 800, 280),
        _crear_blob(GLOW_VERDE, 50, -100, 320),
        _crear_blob(GLOW_MORADO, 400, 150, 260),
        _crear_blob("#FCD34D", 600, 1000, 240),
        _crear_blob(GLOW_VERDE, 200, 1200, 220),
    ]

    VERDES_PARTICULAS = [
        "#065f46", "#047857", COLOR_PRIMARIO, COLOR_PRIMARIO_CLARO,
        "#34d399", "#6ee7b7", "#86efac", "#a7f3d0", COLOR_VERDE_SUAVE,
    ]
    TAMANO_PARTICULA = 14

    # Distribución diferente para la pantalla de recuperación
    config_particulas = [
        (100, 600, 15, -10),
        (300, 100, -15, 10),
        (450, 1100, 8, 12),
        (50, 300, 10, -5),
        (650, 400, -12, 8),
        (250, 850, 14, 14),
        (550, 200, -8, -12),
        (750, 700, 10, -10),
        (400, 50, -10, 10),
    ]
    
    particulas_animadas = []
    for i, (top, left, st, sl) in enumerate(config_particulas):
        color = VERDES_PARTICULAS[i % len(VERDES_PARTICULAS)]
        particulas_animadas.append(
            FloatingElement(
                content=_crear_particula_visual(color, TAMANO_PARTICULA, blur=0),
                top=top,
                left=left,
                step_top=st,
                step_left=sl,
            )
        )

    icon_key = FloatingElement(
        content=ft.Icon(
            ft.Icons.KEY_ROUNDED,
            size=180,
            color=ft.Colors.with_opacity(0.2, GLOW_AZUL),
        ),
        top=100,
        left=150,
    )

    async def animate_background():
        while True:
            icon_key.animate_float()
            for p in particulas_animadas:
                p.animate_float()
            if page.controls:
                page.update()
            await asyncio.sleep(2.1)

    page.run_task(animate_background)

    footer = ft.Text("© 2026 Sistema de Brigadas Escolares - Municipio Maracaibo", size=12, color=COLOR_TEXTO_SEC, text_align=ft.TextAlign.CENTER)

    btn_theme_toggle = create_auth_theme_toggle(page)

    return ft.Stack(
        [
            ft.Container(expand=True, bgcolor=COLOR_FONDO_VERDE),
            *background_blobs,
            icon_key,
            *particulas_animadas,
            ft.Container(
                content=ft.Column(
                    [
                        ft.Container(height=60),
                        header,
                        ft.Container(height=32),
                        card,
                        ft.Container(height=40),
                        footer,
                        ft.Container(height=20),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.AUTO,
                ),
                alignment=ft.Alignment.CENTER,
                expand=True,
            ),
            btn_theme_toggle,
        ],
        expand=True,
    )
