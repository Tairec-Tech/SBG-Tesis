"""Pantalla — Utilidades (hub con acceso a Acerca de, Manual, Legal, Importar/Exportar BD)."""

import flet as ft
from theme import (
    COLOR_TEXTO,
    COLOR_TEXTO_SEC,
    COLOR_FONDO_VERDE,
    COLOR_PRIMARIO,
    COLOR_PRIMARIO_CLARO,
    COLOR_CARD,
    COLOR_BORDE,
)
from components import titulo_pagina, card_principal


def build(page: ft.Page, **kwargs) -> ft.Control:
    content_area = kwargs.get("content_area", None)

    def _ir_a(screen_module):
        """Navega a una sub-pantalla con botón de volver."""
        def handler(_):
            if content_area:
                content_area.content = screen_module.build(page, content_area=content_area, on_back=_volver)
                page.update()
        return handler

    def _volver():
        """Vuelve al hub de Utilidades."""
        if content_area:
            content_area.content = build(page, content_area=content_area)
            page.update()

    # Obtener rol del usuario para mostrar/ocultar Importar/Exportar BD
    try:
        _udata = (page.data or {}).get("usuario_actual", {}) if isinstance(page.data, dict) else {}
        es_admin = _udata.get("rol", "") in ("Directivo", "Coordinador")
    except Exception:
        es_admin = False

    from screens import screen_about, screen_manual, screen_legal, screen_backup

    opciones = [
        ("Acerca de", "Información del sistema y créditos", ft.Icons.INFO_OUTLINED, "#10b981", screen_about),
        ("Manual de Usuario", "Guía rápida para el uso del sistema", ft.Icons.HELP_OUTLINE, "#3b82f6", screen_manual),
        ("Información Legal", "Términos, políticas y avisos legales", ft.Icons.GAVEL_OUTLINED, "#8b5cf6", screen_legal),
    ]
    if es_admin:
        opciones.append(("Importar/Exportar BD", "Gestión de respaldos de la base de datos", ft.Icons.STORAGE_OUTLINED, "#f59e0b", screen_backup))

    cards = []
    for titulo, descripcion, icono, color, modulo in opciones:
        cards.append(
            ft.Container(
                content=ft.Row(
                    [
                        ft.Container(
                            content=ft.Icon(icono, color=color, size=32),
                            padding=14,
                            border_radius=14,
                            bgcolor=ft.Colors.with_opacity(0.1, color),
                        ),
                        ft.Container(width=16),
                        ft.Column(
                            [
                                ft.Text(titulo, size=16, weight="bold", color=COLOR_TEXTO),
                                ft.Container(height=4),
                                ft.Text(descripcion, size=13, color=COLOR_TEXTO_SEC),
                            ],
                            spacing=0,
                            expand=True,
                        ),
                        ft.Icon(ft.Icons.CHEVRON_RIGHT, color=COLOR_TEXTO_SEC, size=24),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=20,
                bgcolor=COLOR_CARD,
                border_radius=14,
                border=ft.Border.all(1, COLOR_BORDE),
                shadow=ft.BoxShadow(
                    blur_radius=8, spread_radius=0,
                    color=ft.Colors.with_opacity(0.06, "black"),
                    offset=ft.Offset(0, 2),
                ),
                on_click=_ir_a(modulo),
                ink=True,
            )
        )

    contenido = ft.Column(
        [
            titulo_pagina("Utilidades", "Herramientas y recursos del sistema"),
            ft.Container(height=24),
        ]
        + [ft.Container(content=c, padding=ft.Padding.only(bottom=12)) for c in cards],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        spacing=0,
    )

    return ft.Container(
        content=contenido,
        padding=24,
        bgcolor=COLOR_FONDO_VERDE,
        expand=True,
    )
