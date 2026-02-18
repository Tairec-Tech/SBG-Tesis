"""Brigadistas — listado por secciones (Profesores / Alumnos) con filtros. Solo Profesor y alumnos; excluye Directivo/Coordinador."""

import flet as ft
from theme import (
    COLOR_PRIMARIO,
    COLOR_TEXTO,
    COLOR_TEXTO_SEC,
    COLOR_CARD,
    COLOR_BORDE,
    COLOR_FONDO_VERDE,
    RADIO,
    get_sombra_card,
)
from components import titulo_pagina, boton_primario, card_principal
from database.crud_usuario import listar_brigadistas_visibles_only, es_profesor


def _filtrar_brigadistas(lista, nombre=None, apellido=None, cedula=None, rol=None):
    """Filtra por nombre, apellido, cédula, rol. Valores vacíos no filtran."""
    if not lista:
        return []
    out = lista
    if nombre and (nombre := str(nombre).strip().lower()):
        out = [u for u in out if nombre in ((u.get("nombre") or "") + " " + (u.get("apellido") or "")).lower()]
    if apellido and (apellido := str(apellido).strip().lower()):
        out = [u for u in out if apellido in (u.get("apellido") or "").lower()]
    if cedula and (cedula := str(cedula).strip()):
        out = [u for u in out if cedula in (u.get("cedula") or "")]
    if rol and (rol := str(rol).strip()):
        if rol.lower() == "profesor":
            out = [u for u in out if u.get("rol") == "Profesor"]
        elif rol.lower() in ("estudiante", "alumno"):
            out = [u for u in out if u.get("rol") in ("Brigadista Jefe", "Subjefe", "Brigadista")]
        else:
            out = [u for u in out if (u.get("rol") or "").lower() == rol.lower()]
    return out


def build(page: ft.Page, content_area=None, **kwargs) -> ft.Control:
    usuario = {}
    try:
        if getattr(page, "data", None) and isinstance(page.data.get("usuario_actual"), dict):
            usuario = page.data["usuario_actual"]
        elif page.client_storage.get("usuario_actual"):
            import json
            raw = page.client_storage.get("usuario_actual")
            usuario = json.loads(raw) if isinstance(raw, str) else (raw or {})
    except Exception:
        pass
    puede_agregar = es_profesor(usuario.get("rol", ""))

    def on_agregar(_):
        from forms import abrir_form_brigadista_registrar
        abrir_form_brigadista_registrar(page, on_success=refresh)

    def refresh():
        if content_area is not None:
            content_area.content = build(page, content_area=content_area)
            page.update()

    contenido = ft.Column(
        [
            titulo_pagina(
                "Brigadistas",
                "Profesores y alumnos de las brigadas (directivos y coordinadores no aparecen aquí)",
                accion=boton_primario("Agregar Brigadista", ft.Icons.PERSON_ADD, on_click=on_agregar) if puede_agregar else None,
            ),
            ft.Container(height=24),
            _build_filtros_y_lista(page, refresh),
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


def _build_filtros_y_lista(page, refresh_callback=None):
    """Barra de filtros + lista en 2 secciones (Profesores / Alumnos) o una sola si hay filtro activo."""
    try:
        lista = listar_brigadistas_visibles_only()
    except Exception:
        lista = []

    # Controles de filtro (se actualizan al cambiar)
    filtro_nombre = ft.TextField(
        hint_text="Nombre",
        width=160,
        height=42,
        border_radius=8,
        border_color=COLOR_BORDE,
        focused_border_color=COLOR_PRIMARIO,
        text_size=13,
        content_padding=ft.Padding(12, 10),
        dense=True,
        on_change=lambda e: _aplicar_filtro(),
    )
    filtro_apellido = ft.TextField(
        hint_text="Apellido",
        width=160,
        height=42,
        border_radius=8,
        border_color=COLOR_BORDE,
        focused_border_color=COLOR_PRIMARIO,
        text_size=13,
        content_padding=ft.Padding(12, 10),
        dense=True,
        on_change=lambda e: _aplicar_filtro(),
    )
    filtro_cedula = ft.TextField(
        hint_text="Cédula",
        width=140,
        height=42,
        border_radius=8,
        border_color=COLOR_BORDE,
        focused_border_color=COLOR_PRIMARIO,
        text_size=13,
        content_padding=ft.Padding(12, 10),
        dense=True,
        on_change=lambda e: _aplicar_filtro(),
    )
    filtro_rol = ft.Dropdown(
        hint_text="Rol",
        width=140,
        height=42,
        options=[
            ft.dropdown.Option("", "Todos"),
            ft.dropdown.Option("Profesor", "Profesor"),
            ft.dropdown.Option("Estudiante", "Estudiante"),
        ],
        border_color=COLOR_BORDE,
        focused_border_color=COLOR_PRIMARIO,
        text_size=13,
        content_padding=ft.Padding(12, 10),
        dense=True,
        on_select=lambda e: _aplicar_filtro(),
    )

    contenedor_lista = ft.Container()

    def _aplicar_filtro():
        nom = filtro_nombre.value or ""
        ape = filtro_apellido.value or ""
        ced = filtro_cedula.value or ""
        rol = filtro_rol.value or ""
        tiene_filtro = bool(nom.strip() or ape.strip() or ced.strip() or rol.strip())
        filtrados = _filtrar_brigadistas(lista, nombre=nom or None, apellido=ape or None, cedula=ced or None, rol=rol or None)
        contenedor_lista.content = _build_lista_interna(
            page, filtrados, tiene_filtro, refresh_callback
        )
        page.update()

    def _limpiar_filtros():
        filtro_nombre.value = ""
        filtro_apellido.value = ""
        filtro_cedula.value = ""
        filtro_rol.value = ""
        _aplicar_filtro()

    # Lista inicial: dos secciones
    profesores = [u for u in lista if u.get("rol") == "Profesor"]
    alumnos = [u for u in lista if u.get("rol") in ("Brigadista Jefe", "Subjefe", "Brigadista")]
    contenedor_lista.content = _build_lista_interna(
        page, lista, False, refresh_callback, profesores=profesores, alumnos=alumnos
    )

    # Bloque de filtros: compacto, sin expandir (evita cuadro gris gigante)
    fila_filtros = ft.Row(
        [
            filtro_nombre,
            filtro_apellido,
            filtro_cedula,
            filtro_rol,
            ft.OutlinedButton(
                "Limpiar filtros",
                icon=ft.Icons.CLEAR_ALL_ROUNDED,
                on_click=lambda e: _limpiar_filtros(),
                style=ft.ButtonStyle(
                    padding=ft.Padding(16, 10),
                    shape=ft.RoundedRectangleBorder(radius=8),
                ),
            ),
        ],
        wrap=True,
        spacing=12,
        alignment=ft.MainAxisAlignment.START,
    )

    card_filtros = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Icon(ft.Icons.FILTER_LIST_ROUNDED, color=COLOR_PRIMARIO, size=20),
                        ft.Text("Filtros de búsqueda", size=15, weight=ft.FontWeight.W_600, color=COLOR_TEXTO),
                    ],
                    spacing=8,
                ),
                ft.Container(height=12),
                ft.Text(
                    "Busque por nombre, apellido, cédula o rol. Por defecto se muestran Profesores y Alumnos por separado.",
                    size=12,
                    color=COLOR_TEXTO_SEC,
                ),
                ft.Container(height=12),
                fila_filtros,
            ],
            spacing=0,
            tight=True,
        ),
        padding=ft.Padding(20, 20),
        border_radius=RADIO,
        bgcolor=COLOR_CARD,
        border=ft.border.all(1, COLOR_BORDE),
        shadow=get_sombra_card(),
        expand=False,
    )

    return ft.Column(
        [
            card_filtros,
            ft.Container(height=24),
            contenedor_lista,
        ],
        spacing=0,
        expand=True,
    )


def _build_lista_interna(page, lista_completa, filtro_activo, refresh_callback, profesores=None, alumnos=None):
    if filtro_activo or profesores is None:
        profesores = [u for u in lista_completa if u.get("rol") == "Profesor"]
        alumnos = [u for u in lista_completa if u.get("rol") in ("Brigadista Jefe", "Subjefe", "Brigadista")]
    if not profesores and not alumnos:
        return card_principal(
            ft.Column(
                [
                    ft.Icon(ft.Icons.PEOPLE_OUTLINED, color=COLOR_TEXTO_SEC, size=48),
                    ft.Container(height=16),
                    ft.Text("No hay brigadistas que coincidan", size=16, weight="bold", color=COLOR_TEXTO),
                    ft.Text("Use «Agregar Brigadista» o quite filtros.", size=14, color=COLOR_TEXTO_SEC),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
            ),
            padding=48,
        )
    from forms import abrir_form_brigadista_modificar, abrir_form_brigadista_eliminar

    def _tarjeta(u):
        return _tarjeta_brigadista(page, u, on_editar=refresh_callback, on_eliminar=refresh_callback)

    if filtro_activo:
        # Una sola lista combinada
        cards = [_tarjeta(u) for u in profesores + alumnos]
        return ft.Row(cards, spacing=20, wrap=True)

    # Dos secciones: Profesores y Alumnos
    sec_prof = ft.Column(
        [
            ft.Text("Profesores", size=16, weight="bold", color=COLOR_TEXTO),
            ft.Container(height=12),
            ft.Row([_tarjeta(u) for u in profesores], spacing=20, wrap=True) if profesores else ft.Text("Ninguno.", size=13, color=COLOR_TEXTO_SEC),
        ],
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.START,
    )
    sec_alumnos = ft.Column(
        [
            ft.Container(height=24),
            ft.Text("Alumnos", size=16, weight="bold", color=COLOR_TEXTO),
            ft.Container(height=12),
            ft.Row([_tarjeta(u) for u in alumnos], spacing=20, wrap=True) if alumnos else ft.Text("Ninguno.", size=13, color=COLOR_TEXTO_SEC),
        ],
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.START,
    )
    return ft.Column([sec_prof, sec_alumnos], spacing=0)


def _tarjeta_brigadista(page, brigadista, on_editar=None, on_eliminar=None):
    from forms import abrir_form_brigadista_modificar, abrir_form_brigadista_eliminar

    nombre_completo = f"{brigadista.get('nombre') or ''} {brigadista.get('apellido') or ''}".strip() or "Sin nombre"
    cedula = brigadista.get("cedula") or "—"
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
                                [ft.Icon(ft.Icons.BADGE_OUTLINED, size=18, color=COLOR_TEXTO_SEC), ft.Text(f"Cédula: {cedula}", size=13, color=COLOR_TEXTO)],
                                spacing=8,
                            ),
                            ft.Row(
                                [ft.Icon(ft.Icons.EMAIL_OUTLINED, size=18, color=COLOR_TEXTO_SEC), ft.Text(email, size=13, color=COLOR_TEXTO)],
                                spacing=8,
                            ),
                            ft.Row(
                                [ft.Icon(ft.Icons.PERSON_OUTLINED, size=18, color=COLOR_TEXTO_SEC), ft.Text(rol, size=13, color=COLOR_TEXTO)],
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
                                        style=ft.ButtonStyle(side=ft.BorderSide(1, COLOR_BORDE), shape=ft.RoundedRectangleBorder(radius=8), color=COLOR_TEXTO),
                                        on_click=_editar,
                                    ),
                                    ft.OutlinedButton(
                                        content=ft.Row([ft.Icon(ft.Icons.DELETE_OUTLINED, size=18), ft.Text("Eliminar", size=13)], spacing=6),
                                        style=ft.ButtonStyle(side=ft.BorderSide(1, "#f87171"), shape=ft.RoundedRectangleBorder(radius=8), color="#b91c1c"),
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
