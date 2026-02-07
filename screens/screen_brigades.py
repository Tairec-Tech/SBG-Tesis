"""Gestión de Brigadas — grid de tarjetas estilo Figma, verde (ambientales)."""

import flet as ft
from theme import (
    COLOR_PRIMARIO,
    COLOR_PRIMARIO_OSCURO,
    COLOR_TEXTO,
    COLOR_TEXTO_SEC,
    COLOR_CARD,
    COLOR_BORDE,
    COLOR_FONDO_VERDE,
    get_sombra_card,
)
from components import card_principal, titulo_pagina, boton_primario
from database.crud_brigada import listar_brigadas


def build(page: ft.Page, content_area=None, **kwargs) -> ft.Control:
    def on_nuevo(_):
        from forms import abrir_form_brigada_registrar
        abrir_form_brigada_registrar(page, on_success=refresh)

    def refresh():
        if content_area is not None:
            content_area.content = build(page, content_area=content_area)

    header = titulo_pagina(
        "Gestión de Brigadas",
        "Administra y organiza todas las brigadas ambientales de tu institución",
        accion=boton_primario("Agregar Brigada", ft.Icons.ADD, on_click=on_nuevo),
    )

    contenido = ft.Column(
        [
            header,
            ft.Container(height=32),
            _build_brigade_cards(page, refresh),
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


def _build_brigade_cards(page, refresh_callback=None):
    """Grid de tarjetas con las brigadas de la base de datos."""
    try:
        brigadas = listar_brigadas()
    except Exception:
        brigadas = []
    if not brigadas:
        return card_principal(
            ft.Column(
                [
                    ft.Icon(ft.Icons.SHIELD_OUTLINED, color=COLOR_TEXTO_SEC, size=48),
                    ft.Container(height=16),
                    ft.Text("No hay brigadas registradas", size=16, weight="bold", color=COLOR_TEXTO),
                    ft.Text("Use «Agregar Brigada» para crear la primera.", size=14, color=COLOR_TEXTO_SEC),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
            ),
            padding=48,
        )
    cards = [
        _tarjeta_brigada(
            page,
            brigada=b,
            nombre=(b["nombre_brigada"] or "Brigada"),
            responsable=(b.get("coordinador") or b.get("area_accion") or "—"),
            desc=(b.get("descripcion") or b.get("area_accion") or "Sin descripción"),
            miembros=b.get("num_miembros", 0),
            pct=0,
            on_editar=refresh_callback,
            on_eliminar=refresh_callback,
        )
        for b in brigadas
    ]
    return ft.Row(cards, spacing=20, wrap=True)


def _tarjeta_brigada(page, brigada, nombre, responsable, desc, miembros, pct, on_editar=None, on_eliminar=None):
    from forms import abrir_form_brigada_modificar, abrir_form_brigada_eliminar

    def _editar(_):
        abrir_form_brigada_modificar(page, brigada=brigada, on_success=on_editar)

    def _eliminar(_):
        abrir_form_brigada_eliminar(page, brigada=brigada, on_success=on_eliminar)

    return ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.SHIELD_OUTLINED, color="white", size=24),
                            ft.Container(expand=True),
                            ft.Icon(ft.Icons.STAR_OUTLINE, color="white", size=20),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    padding=ft.Padding(16, 16, 16, 8),
                    border_radius=ft.BorderRadius.only(top_left=12, top_right=12),
                    gradient=ft.LinearGradient(
                        begin=ft.Alignment.TOP_LEFT,
                        end=ft.Alignment.BOTTOM_RIGHT,
                        colors=[COLOR_PRIMARIO, COLOR_PRIMARIO_OSCURO],
                    ),
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(nombre, size=16, weight="bold", color=COLOR_TEXTO),
                            ft.Text(responsable, size=13, color=COLOR_TEXTO_SEC),
                            ft.Container(height=12),
                            ft.Text(desc, size=13, color=COLOR_TEXTO_SEC),
                            ft.Container(height=16),
                            ft.Row(
                                [
                                    ft.Icon(ft.Icons.PEOPLE_OUTLINED, color=COLOR_PRIMARIO, size=20),
                                    ft.Text(f"Miembros Activos: {miembros}", size=13, color=COLOR_TEXTO),
                                    ft.Container(expand=True),
                                    ft.Container(
                                        content=ft.Stack(
                                            [
                                                ft.Container(
                                                    content=ft.Text(f"{pct}%", size=11, weight="bold", color=COLOR_PRIMARIO),
                                                    alignment=ft.Alignment.CENTER,
                                                    width=44,
                                                    height=44,
                                                ),
                                                ft.ProgressRing(width=44, height=44, value=pct / 100, color=COLOR_PRIMARIO, stroke_width=4),
                                            ],
                                        ),
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            ft.Container(height=16),
                            ft.Row(
                                [
                                    ft.OutlinedButton(
                                        content=ft.Row(
                                            [ft.Icon(ft.Icons.EDIT_OUTLINED, size=18), ft.Text("Editar", size=13)],
                                            spacing=6,
                                        ),
                                        style=ft.ButtonStyle(
                                            side=ft.BorderSide(1, COLOR_BORDE),
                                            shape=ft.RoundedRectangleBorder(radius=8),
                                        ),
                                        on_click=_editar,
                                    ),
                                    ft.OutlinedButton(
                                        content=ft.Row(
                                            [ft.Icon(ft.Icons.DELETE_OUTLINED, size=18), ft.Text("Eliminar", size=13)],
                                            spacing=6,
                                        ),
                                        style=ft.ButtonStyle(
                                            side=ft.BorderSide(1, "#f87171"),
                                            shape=ft.RoundedRectangleBorder(radius=8),
                                        ),
                                        on_click=_eliminar,
                                    ),
                                ],
                                spacing=12,
                            ),
                        ],
                        spacing=0,
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                    ),
                    padding=20,
                    bgcolor=COLOR_CARD,
                    border_radius=ft.BorderRadius.only(bottom_left=12, bottom_right=12),
                ),
            ],
            spacing=0,
        ),
        width=320,
        border_radius=12,
        shadow=get_sombra_card(),
    )
