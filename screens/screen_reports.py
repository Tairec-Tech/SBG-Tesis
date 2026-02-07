"""Reportes de Incidentes — estilo Figma, tonos verdes."""

import flet as ft
from theme import (
    COLOR_PRIMARIO,
    COLOR_TEXTO,
    COLOR_TEXTO_SEC,
    COLOR_CARD,
    COLOR_BORDE,
    COLOR_FONDO_VERDE,
    COLOR_EXITO,
    COLOR_ALERTA,
    COLOR_PELIGRO,
    get_sombra_card,
)
from components import titulo_pagina, boton_primario, card_principal


def build(page: ft.Page, **kwargs) -> ft.Control:
    def on_nuevo_report(_):
        from forms import abrir_form_nuevo_reporte
        abrir_form_nuevo_reporte(page)

    contenido = ft.Column(
        [
            titulo_pagina(
                "Reportes de Incidentes",
                "Registra y da seguimiento a los eventos y situaciones",
                accion=boton_primario("Nuevo Reporte", ft.Icons.ADD, on_click=on_nuevo_report),
            ),
            ft.Container(height=32),
            _build_summary_cards(),
            ft.Container(height=32),
            _build_incident_list(page),
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


def _build_summary_cards():
    items = [
        ("0", "Total Reportes", ft.Icons.WARNING_AMBER_OUTLINED, COLOR_PELIGRO),
        ("0", "En Proceso", ft.Icons.SCHEDULE_OUTLINED, COLOR_ALERTA),
        ("0", "Resueltos", ft.Icons.CHECK_CIRCLE_OUTLINED, COLOR_EXITO),
    ]
    return ft.Row(
        [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ico, color=color, size=32),
                        ft.Container(height=8),
                        ft.Text(val, size=28, weight="bold", color=COLOR_TEXTO),
                        ft.Text(lbl, size=14, color=COLOR_TEXTO_SEC),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                    spacing=0,
                ),
                bgcolor=COLOR_CARD,
                padding=24,
                border_radius=12,
                border=ft.Border.all(1, COLOR_BORDE),
                shadow=get_sombra_card(),
                expand=True,
            )
            for val, lbl, ico, color in items
        ],
        spacing=20,
    )


def _build_incident_list(page):
    return card_principal(
        ft.Column(
            [
                ft.Text("No hay reportes de incidentes. Use «Nuevo Reporte» para registrar.", size=14, color=COLOR_TEXTO_SEC),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.START,
        ),
    )
