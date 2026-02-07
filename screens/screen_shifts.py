"""Turnos y Horarios — estilo Figma, cards por fecha."""

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
from components import titulo_pagina, boton_primario, card_principal


def build(page: ft.Page, **kwargs) -> ft.Control:
    def on_nuevo_turno(_):
        from forms import abrir_form_turno
        abrir_form_turno(page)

    contenido = ft.Column(
        [
            titulo_pagina(
                "Turnos y Horarios",
                "Organiza y asigna los turnos de las brigadas ambientales",
                accion=boton_primario("Nuevo Turno", ft.Icons.ADD, on_click=on_nuevo_turno),
            ),
            ft.Container(height=32),
            _build_kpis(),
            ft.Container(height=32),
            _build_schedule(page),
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


def _build_kpis():
    items = [
        ("0", "Turnos Programados", ft.Icons.CALENDAR_MONTH_OUTLINED),
        ("0", "Brigadistas Asignados", ft.Icons.PEOPLE_OUTLINED),
        ("0", "Días con Turnos", ft.Icons.SCHEDULE_OUTLINED),
    ]
    row = ft.Row(
        [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ico, color=COLOR_PRIMARIO, size=28),
                        ft.Container(height=8),
                        ft.Text(val, size=24, weight="bold", color=COLOR_TEXTO),
                        ft.Text(lbl, size=13, color=COLOR_TEXTO_SEC),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                    spacing=0,
                ),
                bgcolor=COLOR_CARD,
                padding=20,
                border_radius=12,
                border=ft.Border.all(1, COLOR_BORDE),
                shadow=get_sombra_card(),
                expand=True,
            )
            for val, lbl, ico in items
        ],
        spacing=20,
    )
    return row


def _build_schedule(page):
    """Cards de turnos por fecha. Sin datos de ejemplo."""
    return card_principal(
        ft.Column(
            [
                ft.Icon(ft.Icons.CALENDAR_MONTH_OUTLINED, color=COLOR_TEXTO_SEC, size=48),
                ft.Container(height=16),
                ft.Text("No hay turnos programados", size=16, weight="bold", color=COLOR_TEXTO),
                ft.Text("Use «Nuevo Turno» para crear el primero.", size=14, color=COLOR_TEXTO_SEC),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
        ),
        padding=48,
    )
