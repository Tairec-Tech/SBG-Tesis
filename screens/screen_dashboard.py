"""Panel Principal — dashboard estilo Figma, tonos verdes."""

import flet as ft
from theme import (
    COLOR_PRIMARIO,
    COLOR_TEXTO,
    COLOR_TEXTO_SEC,
    COLOR_CARD,
    COLOR_BORDE,
    COLOR_FONDO_VERDE,
    get_sombra_card,
)
from components import card_principal, titulo_pagina


def build(page: ft.Page, **kwargs) -> ft.Control:
    contenido = ft.Column(
        [
            titulo_pagina(
                "Panel Principal",
                "Sistema de coordinación de brigadas escolares",
            ),
            ft.Container(height=32),
            _build_kpis(page),
            ft.Container(height=32),
            _build_resumen(page),
        ],
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


def _build_kpis(page):
    """Tarjetas de KPIs (Total Brigadas, Brigadistas, etc.) en tonos verdes. Sin datos de ejemplo."""
    items = [
        ("0", "Total Brigadas", ft.Icons.SHIELD_OUTLINED, "-"),
        ("0", "Total Brigadistas", ft.Icons.PEOPLE_OUTLINED, "-"),
        ("0", "Turnos Este Mes", ft.Icons.CALENDAR_MONTH_OUTLINED, "-"),
        ("0", "Incidentes Resueltos", ft.Icons.CHECK_CIRCLE_OUTLINED, "-"),
    ]
    cards = []
    for valor, etiqueta, icono, tendencia in items:
        cards.append(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Container(
                                    content=ft.Icon(icono, color=COLOR_PRIMARIO, size=28),
                                    width=48,
                                    height=48,
                                    border_radius=12,
                                    bgcolor=ft.Colors.with_opacity(0.12, COLOR_PRIMARIO),
                                    alignment=ft.Alignment.CENTER,
                                ),
                                ft.Container(expand=True),
                                ft.Row(
                                    [
                                        ft.Text(tendencia, size=12, color=COLOR_TEXTO_SEC, weight="w500"),
                                    ],
                                    spacing=4,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        ft.Container(height=12),
                        ft.Text(valor, size=28, weight="bold", color=COLOR_TEXTO),
                        ft.Text(etiqueta, size=13, color=COLOR_TEXTO_SEC),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                    spacing=0,
                ),
                bgcolor=COLOR_CARD,
                padding=20,
                border_radius=12,
                border=ft.Border.all(1, COLOR_BORDE),
                shadow=get_sombra_card(),
            )
        )
    # Altura fija para la fila de KPIs: evita que expanda y se vea el bloque gris gigante
    altura_kpis = 160
    return ft.Container(
        content=ft.Row(
            [ft.Container(content=c, expand=True, height=altura_kpis) for c in cards],
            spacing=20,
            vertical_alignment=ft.CrossAxisAlignment.START,
        ),
        height=altura_kpis,
        bgcolor=COLOR_FONDO_VERDE,
    )


def _build_resumen(page):
    """Sección de resumen o bienvenida."""
    return card_principal(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Icon(ft.Icons.ECO, color=COLOR_PRIMARIO, size=40),
                        ft.Container(width=16),
                        ft.Column(
                            [
                                ft.Text("Bienvenido al Panel de Brigadas Ambientales", size=18, weight="bold", color=COLOR_TEXTO),
                                ft.Text("Municipio Maracaibo — Gestión y coordinación en tonos verdes.", size=14, color=COLOR_TEXTO_SEC),
                            ],
                            spacing=4,
                            horizontal_alignment=ft.CrossAxisAlignment.START,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
            ],
            spacing=0,
        ),
    )
