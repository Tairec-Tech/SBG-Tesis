"""Brigadistas — listado y gestión de miembros desde la BD."""

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
from database.crud_usuario import listar_brigadistas


def build(page: ft.Page, content_area=None, **kwargs) -> ft.Control:
    def on_agregar(_):
        from forms import abrir_form_brigadista_registrar
        abrir_form_brigadista_registrar(page, on_success=refresh)

    def refresh():
        if content_area is not None:
            content_area.content = build(page, content_area=content_area)

    contenido = ft.Column(
        [
            titulo_pagina(
                "Brigadistas",
                "Miembros de las brigadas ambientales",
                accion=boton_primario("Agregar Brigadista", ft.Icons.PERSON_ADD, on_click=on_agregar),
            ),
            ft.Container(height=32),
            _build_list(page, refresh),
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


def _build_list(page, refresh_callback=None):
    """Lista de brigadistas desde la BD; vacía si no hay o hay error."""
    try:
        lista = listar_brigadistas()
    except Exception:
        lista = []
    if not lista:
        return card_principal(
            ft.Column(
                [
                    ft.Icon(ft.Icons.PEOPLE_OUTLINED, color=COLOR_TEXTO_SEC, size=48),
                    ft.Container(height=16),
                    ft.Text("No hay brigadistas registrados", size=16, weight="bold", color=COLOR_TEXTO),
                    ft.Text("Use «Agregar Brigadista» para registrar el primero.", size=14, color=COLOR_TEXTO_SEC),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
            ),
            padding=48,
        )
    cards = [
        _tarjeta_brigadista(page, u, on_editar=refresh_callback, on_eliminar=refresh_callback)
        for u in lista
    ]
    return ft.Row(cards, spacing=20, wrap=True)


def _tarjeta_brigadista(page, brigadista, on_editar=None, on_eliminar=None):
    from forms import abrir_form_brigadista_modificar, abrir_form_brigadista_eliminar

    nombre_completo = f"{brigadista.get('nombre') or ''} {brigadista.get('apellido') or ''}".strip() or "Sin nombre"
    email = brigadista.get("email") or "—"
    rol = brigadista.get("rol") or "—"
    brigada_nombre = brigadista.get("nombre_brigada") or "—"

    def _editar(_):
        abrir_form_brigadista_modificar(page, brigadista=brigadista, on_success=on_editar)

    def _eliminar(_):
        abrir_form_brigadista_eliminar(page, brigadista=brigadista, on_success=on_eliminar)

    return ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.PERSON_OUTLINED, color="white", size=24),
                            ft.Text(nombre_completo, size=16, weight="bold", color="white"),
                            ft.Container(expand=True),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    padding=16,
                    bgcolor=COLOR_PRIMARIO,
                    border_radius=ft.BorderRadius.only(top_left=12, top_right=12),
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [ft.Icon(ft.Icons.EMAIL_OUTLINED, size=18, color=COLOR_TEXTO_SEC), ft.Text(email, size=13, color=COLOR_TEXTO)],
                                spacing=8,
                            ),
                            ft.Row(
                                [ft.Icon(ft.Icons.BADGE_OUTLINED, size=18, color=COLOR_TEXTO_SEC), ft.Text(rol, size=13, color=COLOR_TEXTO)],
                                spacing=8,
                            ),
                            ft.Row(
                                [ft.Icon(ft.Icons.SHIELD_OUTLINED, size=18, color=COLOR_TEXTO_SEC), ft.Text(brigada_nombre, size=13, color=COLOR_TEXTO)],
                                spacing=8,
                            ),
                            ft.Container(height=16),
                            ft.Row(
                                [
                                    ft.OutlinedButton(
                                        content=ft.Row([ft.Icon(ft.Icons.EDIT_OUTLINED, size=18), ft.Text("Editar", size=13)], spacing=6),
                                        style=ft.ButtonStyle(side=ft.BorderSide(1, COLOR_BORDE), shape=ft.RoundedRectangleBorder(radius=8)),
                                        on_click=_editar,
                                    ),
                                    ft.OutlinedButton(
                                        content=ft.Row([ft.Icon(ft.Icons.DELETE_OUTLINED, size=18), ft.Text("Eliminar", size=13)], spacing=6),
                                        style=ft.ButtonStyle(side=ft.BorderSide(1, "#f87171"), shape=ft.RoundedRectangleBorder(radius=8)),
                                        on_click=_eliminar,
                                    ),
                                ],
                                spacing=12,
                            ),
                        ],
                        spacing=8,
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
        width=320,
        border_radius=12,
        shadow=get_sombra_card(),
    )
