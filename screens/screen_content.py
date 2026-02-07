"""Contenido Educativo — guías y recursos, estilo Figma, verde."""

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
from components import titulo_pagina, card_principal


def build(page: ft.Page, **kwargs) -> ft.Control:
    contenido = ft.Column(
        [
            titulo_pagina(
                "Contenido Educativo",
                "Sistema de coordinación de brigadas escolares",
            ),
            ft.Container(height=32),
            _build_hero_card(),
            ft.Container(height=24),
            _build_brigade_guide_card(page),
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


def _build_hero_card():
    return card_principal(
        ft.Row(
            [
                ft.Icon(ft.Icons.MENU_BOOK_OUTLINED, color=COLOR_PRIMARIO, size=48),
                ft.Container(width=24),
                ft.Column(
                    [
                        ft.Text("Centro Educativo", size=18, weight="bold", color=COLOR_TEXTO),
                        ft.Text("Recursos, guías y contenido educativo para brigadas ambientales.", size=14, color=COLOR_TEXTO_SEC),
                    ],
                    spacing=4,
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
        ),
    )


def _build_brigade_guide_card(page):
    return ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Container(
                                content=ft.Icon(ft.Icons.ECO, color="white", size=32),
                                width=56,
                                height=56,
                                border_radius=12,
                                bgcolor=ft.Colors.with_opacity(0.3, "white"),
                                alignment=ft.Alignment.CENTER,
                            ),
                            ft.Container(width=16),
                            ft.Column(
                                [
                                    ft.Text("Guías y recursos", size=18, weight="bold", color="white"),
                                    ft.Text("Recursos y contenido educativo para las brigadas ambientales.", size=13, color=ft.Colors.with_opacity(0.9, "white")),
                                ],
                                spacing=4,
                                horizontal_alignment=ft.CrossAxisAlignment.START,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    padding=20,
                    border_radius=ft.BorderRadius.only(top_left=12, top_right=12),
                    gradient=ft.LinearGradient(
                        begin=ft.Alignment.TOP_LEFT,
                        end=ft.Alignment.BOTTOM_RIGHT,
                        colors=[COLOR_PRIMARIO, "#047857"],
                    ),
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINED, color=COLOR_PRIMARIO, size=20), ft.Text("Responsabilidades", size=14, weight="w600", color=COLOR_TEXTO)],
                                spacing=8,
                            ),
                            ft.Container(height=12),
                            ft.Text("• Conocer prácticas de reciclaje y reducción de residuos.", size=13, color=COLOR_TEXTO_SEC),
                            ft.Text("• Mantener áreas verdes y huertos escolares.", size=13, color=COLOR_TEXTO_SEC),
                            ft.Text("• Promover campañas de conciencia ambiental.", size=13, color=COLOR_TEXTO_SEC),
                            ft.Container(height=16),
                            ft.Row(
                                [ft.Text("Habilidades:", size=14, weight="w600", color=COLOR_TEXTO)],
                                spacing=8,
                            ),
                            ft.Container(height=8),
                            ft.Row(
                                [
                                    ft.Container(content=ft.Text("Reciclaje", size=12), bgcolor=COLOR_BORDE, padding=ft.Padding(10, 6), border_radius=8),
                                    ft.Container(content=ft.Text("Compostaje", size=12), bgcolor=COLOR_BORDE, padding=ft.Padding(10, 6), border_radius=8),
                                    ft.Container(content=ft.Text("Educación ambiental", size=12), bgcolor=COLOR_BORDE, padding=ft.Padding(10, 6), border_radius=8),
                                ],
                                spacing=8,
                                wrap=True,
                            ),
                            ft.Container(height=20),
                            ft.OutlinedButton(
                                content=ft.Row(
                                    [ft.Icon(ft.Icons.DOWNLOAD_OUTLINED, size=20), ft.Text("Descargar Guía", size=14)],
                                    spacing=8,
                                ),
                                style=ft.ButtonStyle(
                                    side=ft.BorderSide(2, COLOR_PRIMARIO),
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                ),
                            ),
                        ],
                        spacing=0,
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                    ),
                    padding=20,
                    bgcolor=COLOR_CARD,
                    border_radius=ft.BorderRadius.only(bottom_left=12, bottom_right=12),
                    border=ft.Border(left=ft.BorderSide(1, COLOR_BORDE), bottom=ft.BorderSide(1, COLOR_BORDE), right=ft.BorderSide(1, COLOR_BORDE)),
                ),
            ],
            spacing=0,
        ),
        border_radius=12,
        shadow=get_sombra_card(),
    )
