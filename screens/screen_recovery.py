"""Recuperar Contraseña — estilo Figma: correo, botón Recuperar, Volver al Login."""

import flet as ft
from theme import (
    COLOR_PRIMARIO,
    COLOR_TEXTO,
    COLOR_TEXTO_SEC,
    COLOR_CARD,
    COLOR_BORDE,
    COLOR_FONDO_GRADIENTE_INICIO,
    COLOR_FONDO_GRADIENTE_FIN,
)


def build(page: ft.Page, on_back_to_login) -> ft.Control:
    campo_email = ft.TextField(
        label="Correo Electrónico",
        hint_text="Ingrese su correo electrónico",
        border_color=COLOR_BORDE,
        focused_border_color=COLOR_PRIMARIO,
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
                    ),
                    on_click=lambda e: on_back_to_login(),
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
        ),
        bgcolor=COLOR_CARD,
        width=400,
        padding=40,
        border_radius=24,
        shadow=ft.BoxShadow(blur_radius=32, spread_radius=-4, color=ft.Colors.with_opacity(0.18, "black"), offset=ft.Offset(0, 12)),
        border=ft.Border.all(1, COLOR_BORDE),
    )

    footer = ft.Text("© 2026 Sistema de Brigadas Escolares - Municipio Maracaibo", size=12, color=COLOR_TEXTO_SEC, text_align=ft.TextAlign.CENTER)

    return ft.Container(
        content=ft.Column(
            [header, ft.Container(height=32), card, ft.Container(height=40), footer],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
        ),
        gradient=ft.LinearGradient(
            begin=ft.Alignment.TOP_LEFT,
            end=ft.Alignment.BOTTOM_RIGHT,
            colors=[COLOR_FONDO_GRADIENTE_INICIO, COLOR_FONDO_GRADIENTE_FIN],
        ),
        expand=True,
        alignment=ft.Alignment.CENTER,
    )
