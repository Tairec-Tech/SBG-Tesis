"""Pantalla — Configuración General."""

import flet as ft
from theme import (
    COLOR_TEXTO,
    COLOR_TEXTO_SEC,
    COLOR_FONDO_VERDE,
    COLOR_PRIMARIO,
)
from components import titulo_pagina, card_principal


def build(page: ft.Page, **kwargs) -> ft.Control:
    contenido = ft.Column(
        [
            titulo_pagina("Configuración", "Ajustes generales del sistema"),
            ft.Container(height=24),
            card_principal(
                ft.Column(
                    [
                        ft.Icon(ft.Icons.CONSTRUCTION_OUTLINED, color=COLOR_PRIMARIO, size=48),
                        ft.Container(height=16),
                        ft.Text("Módulo en Desarrollo", size=20, weight="bold", color=COLOR_TEXTO),
                        ft.Container(height=8),
                        ft.Text(
                            "Las opciones de configuración avanzada estarán disponibles próximamente. "
                            "Mientras tanto, puedes cambiar el modo de interfaz (claro/oscuro) desde la barra lateral.",
                            size=14, color=COLOR_TEXTO_SEC, text_align=ft.TextAlign.CENTER,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=0,
                ),
                padding=48,
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
