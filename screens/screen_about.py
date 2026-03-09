"""Pantalla — Acerca de la Aplicación."""

import flet as ft
from theme import (
    COLOR_TEXTO,
    COLOR_TEXTO_SEC,
    COLOR_FONDO_VERDE,
    COLOR_PRIMARIO,
    COLOR_PRIMARIO_CLARO,
)
from components import titulo_pagina, card_principal


def build(page: ft.Page, **kwargs) -> ft.Control:
    on_back = kwargs.get("on_back", None)

    back_btn = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.ARROW_BACK, color=COLOR_PRIMARIO, size=20),
                ft.Container(width=4),
                ft.Text("Volver a Utilidades", size=14, color=COLOR_PRIMARIO),
            ],
            spacing=0,
        ),
        on_click=lambda _: on_back() if on_back else None,
        padding=ft.Padding.only(bottom=16),
    ) if on_back else ft.Container()

    contenido = ft.Column(
        [
            back_btn,
            titulo_pagina("Acerca de", "Información del sistema"),
            ft.Container(height=24),
            card_principal(
                ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Icon(ft.Icons.SHIELD_ROUNDED, color=COLOR_PRIMARIO, size=48),
                                ft.Container(width=16),
                                ft.Column(
                                    [
                                        ft.Text("Sistema de Gestión de Brigadas", size=22, weight="bold", color=COLOR_TEXTO),
                                        ft.Text("Brigadas Ambientales Escolares", size=14, color=COLOR_TEXTO_SEC),
                                    ],
                                    spacing=4,
                                ),
                            ],
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        ft.Container(height=20),
                        ft.Divider(height=1),
                        ft.Container(height=20),
                        _info_row("Versión", "1.0.0"),
                        _info_row("Plataforma", "Desktop (Flet Framework)"),
                        _info_row("Base de Datos", "MySQL — db_brigadas_maracaibo"),
                        _info_row("Lenguaje", "Python 3.14"),
                        ft.Container(height=20),
                        ft.Divider(height=1),
                        ft.Container(height=20),
                        ft.Text("Desarrollado para la coordinación y gestión de brigadas ambientales en instituciones educativas del municipio Maracaibo.", 
                                size=14, color=COLOR_TEXTO_SEC),
                        ft.Container(height=12),
                        ft.Text("© 2025-2026 — Brigadas Ambientales Escolares. Todos los derechos reservados.", 
                                size=12, color=COLOR_TEXTO_SEC, italic=True),
                    ],
                    spacing=0,
                ),
            ),
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


def _info_row(label: str, value: str) -> ft.Container:
    return ft.Container(
        content=ft.Row(
            [
                ft.Text(label, size=14, weight="w600", color=COLOR_TEXTO, width=180),
                ft.Text(value, size=14, color=COLOR_TEXTO_SEC),
            ],
            alignment=ft.MainAxisAlignment.START,
        ),
        padding=ft.padding.symmetric(vertical=6),
    )
