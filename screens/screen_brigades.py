"""Gestión de Brigadas — grid de tarjetas estilo Figma, color por brigada."""

import flet as ft
import re
import json
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
from database.crud_brigada import listar_brigadas, listar_brigadas_para_profesor, obtener_brigada as obtener_brigada_crud
from database.crud_usuario import es_admin, es_profesor, obtener_usuario, listar_brigadistas_brigada


def _abrir_dialogo_detalle_brigada(page: ft.Page, id_brigada: int, nombre_brigada: str, num_miembros: int):
    """Abre un diálogo con detalles de la brigada y jerarquía (líder, sublíder, miembros)."""
    try:
        b = obtener_brigada_crud(id_brigada)
    except Exception:
        b = None
    if not b:
        page.snack_bar = ft.SnackBar(ft.Text("No se pudo cargar la brigada."), bgcolor="#ef4444")
        page.snack_bar.open = True
        page.update()
        return
    nombre = b.get("nombre_brigada") or nombre_brigada
    desc = b.get("descripcion") or b.get("area_accion") or "—"
    profesor_id = b.get("profesor_id")
    subjefe_id = b.get("subjefe_id")
    profesor_nombre = "—"
    if profesor_id:
        try:
            u = obtener_usuario(profesor_id)
            if u:
                profesor_nombre = f"{u.get('nombre', '')} {u.get('apellido', '')}".strip() or u.get("email", "—")
        except Exception:
            pass
    subjefe_nombre = "—"
    if subjefe_id:
        try:
            u = obtener_usuario(subjefe_id)
            if u:
                subjefe_nombre = f"{u.get('nombre', '')} {u.get('apellido', '')}".strip() or u.get("email", "—")
        except Exception:
            pass
    try:
        miembros_lista = listar_brigadistas_brigada(id_brigada)
    except Exception:
        miembros_lista = []
    lineas_jerarquia = [
        ft.Text("Jerarquía", size=14, weight="bold", color=COLOR_TEXTO),
        ft.Container(height=6),
        ft.Row([ft.Text("Líder (profesor): ", size=13, color=COLOR_TEXTO_SEC), ft.Text(profesor_nombre, size=13, color=COLOR_TEXTO)], spacing=8),
        ft.Row([ft.Text("Sublíder: ", size=13, color=COLOR_TEXTO_SEC), ft.Text(subjefe_nombre, size=13, color=COLOR_TEXTO)], spacing=8),
        ft.Container(height=12),
        ft.Text("Miembros", size=14, weight="bold", color=COLOR_TEXTO),
        ft.Container(height=6),
    ]
    for m in miembros_lista:
        lineas_jerarquia.append(
            ft.Container(
                content=ft.Text(f"• {m.get('nombre', '')} {m.get('apellido', '')} ({m.get('rol', '')})", size=13, color=COLOR_TEXTO),
                padding=ft.Padding(0, 2),
            )
        )
    if not miembros_lista:
        lineas_jerarquia.append(ft.Text("Ninguno registrado.", size=13, color=COLOR_TEXTO_SEC))
    contenido = ft.Column(
        [
            ft.Text(nombre, size=18, weight="bold", color=COLOR_TEXTO),
            ft.Text(desc, size=13, color=COLOR_TEXTO_SEC),
            ft.Container(height=16),
            *lineas_jerarquia,
        ],
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.START,
    )
    dialogo = ft.AlertDialog(
        modal=True,
        bgcolor=COLOR_CARD,
        title=ft.Text("Detalles de la brigada", size=18, weight="w600", color=COLOR_TEXTO),
        content=ft.Container(
            content=ft.Column([contenido], scroll=ft.ScrollMode.AUTO, tight=True),
            width=420,
            bgcolor=COLOR_CARD,
        ),
        actions=[
            ft.TextButton(
                content=ft.Text("Cerrar", size=13, color=COLOR_TEXTO),
                style=ft.ButtonStyle(color=COLOR_TEXTO),
                on_click=lambda e: page.pop_dialog(),
            ),
        ],
    )
    page.show_dialog(dialogo)


def _oscurecer_hex(hex_color: str, factor: float = 0.65) -> str:
    """Devuelve una versión más oscura del color hex (#RRGGBB)."""
    if not hex_color or not re.match(r"^#[0-9A-Fa-f]{6}$", hex_color):
        return COLOR_PRIMARIO_OSCURO
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    r = max(0, min(255, int(r * factor)))
    g = max(0, min(255, int(g * factor)))
    b = max(0, min(255, int(b * factor)))
    return f"#{r:02x}{g:02x}{b:02x}"


def _obtener_usuario_actual(page: ft.Page) -> dict:
    """Obtiene el usuario actual desde page.data (login) o client_storage."""
    try:
        if getattr(page, "data", None) and isinstance(page.data.get("usuario_actual"), dict):
            return page.data["usuario_actual"]
        usuario_json = page.client_storage.get("usuario_actual")
        if usuario_json:
            return json.loads(usuario_json) if isinstance(usuario_json, str) else (usuario_json or {})
    except Exception:
        pass
    return {}


def build(page: ft.Page, content_area=None, **kwargs) -> ft.Control:
    # Obtener usuario actual para permisos
    usuario = _obtener_usuario_actual(page)
    rol = usuario.get("rol", "")
    user_id = usuario.get("id")
    
    # Solo el profesor puede crear brigadas; directivo/coordinador solo supervisan
    puede_crear = es_profesor(rol)
    
    def on_nuevo(_):
        from forms import abrir_form_brigada_registrar
        abrir_form_brigada_registrar(page, on_success=refresh, usuario_actual=usuario)

    def refresh():
        if content_area is not None:
            content_area.content = build(page, content_area=content_area)
            page.update()

    # Texto del header según rol
    if es_profesor(rol):
        subtitulo = "Gestiona tus brigadas y visualiza las de otros profesores"
    else:
        subtitulo = "Administra y organiza todas las brigadas ambientales de tu institución"
    
    header = titulo_pagina(
        "Gestión de Brigadas",
        subtitulo,
        accion=boton_primario("Agregar Brigada", ft.Icons.ADD, on_click=on_nuevo) if puede_crear else None,
    )

    contenido = ft.Column(
        [
            header,
            ft.Container(height=32),
            _build_brigade_cards(page, refresh, usuario),
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


def _build_brigade_cards(page, refresh_callback=None, usuario=None):
    """Grid de tarjetas con las brigadas de la base de datos, filtradas por rol."""
    usuario = usuario or {}
    rol = usuario.get("rol", "")
    user_id = usuario.get("id")
    
    try:
        if es_admin(rol):
            # Admin ve todas las brigadas
            brigadas = listar_brigadas()
        elif es_profesor(rol) and user_id:
            # Profesor ve sus brigadas y las de otros profesores (institución desde login)
            institucion_id = usuario.get("institucion_id") or 1
            brigadas = listar_brigadas_para_profesor(user_id, institucion_id)
        else:
            # Otros roles no ven brigadas en esta pantalla
            brigadas = []
    except Exception:
        brigadas = []
    
    if not brigadas:
        msg = "No hay brigadas registradas"
        sub = "Los profesores pueden crear brigadas desde «Agregar Brigada»."
        if es_profesor(rol):
            msg = "Aún no tienes brigadas. ¡Crea tu primera brigada!"
            sub = "Use «Agregar Brigada» para crear una."
        return card_principal(
            ft.Column(
                [
                    ft.Icon(ft.Icons.SHIELD_OUTLINED, color=COLOR_TEXTO_SEC, size=48),
                    ft.Container(height=16),
                    ft.Text(msg, size=16, weight="bold", color=COLOR_TEXTO),
                    ft.Text(sub, size=14, color=COLOR_TEXTO_SEC),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
            ),
            padding=48,
        )
    
    cards = []
    for b in brigadas:
        # Determinar si el usuario puede editar/eliminar esta brigada
        es_propia = b.get("es_propia", False) or b.get("profesor_id") == user_id
        puede_editar = es_admin(rol) or es_propia
        puede_eliminar = es_admin(rol) or es_propia
        
        # Líder: Prof. Nombre Abrev. (ej. Prof. Juan P.)
        pnom = (b.get("profesor_nombre") or "").strip()
        pap = (b.get("profesor_apellido") or "").strip()
        if pnom:
            abrev_ap = f" {pap[0]}." if pap else ""
            responsable = f"Líder: Prof. {pnom}{abrev_ap}"
        else:
            responsable = "Líder: —"
        
        cards.append(
            _tarjeta_brigada(
                page,
                brigada=b,
                nombre=(b["nombre_brigada"] or "Brigada"),
                responsable=responsable,
                desc=(b.get("descripcion") or b.get("area_accion") or "Sin descripción"),
                miembros=b.get("num_miembros", 0),
                color_identificador=b.get("color_identificador"),
                on_editar=refresh_callback if puede_editar else None,
                on_eliminar=refresh_callback if puede_eliminar else None,
                es_propia=es_propia,
                es_solo_lectura=not puede_editar,
            )
        )
    return ft.Row(cards, spacing=20, wrap=True)


def _tarjeta_brigada(page, brigada, nombre, responsable, desc, miembros, color_identificador=None, on_editar=None, on_eliminar=None, es_propia=True, es_solo_lectura=False):
    from forms import abrir_form_brigada_modificar, abrir_form_brigada_eliminar, abrir_form_brigada_agregar_miembros

    color_primario = color_identificador if color_identificador and re.match(r"^#[0-9A-Fa-f]{6}$", color_identificador) else COLOR_PRIMARIO
    color_oscuro = _oscurecer_hex(color_identificador, 0.65) if color_identificador and re.match(r"^#[0-9A-Fa-f]{6}$", color_identificador) else COLOR_PRIMARIO_OSCURO

    def _editar(_):
        if on_editar:
            abrir_form_brigada_modificar(page, brigada=brigada, on_success=on_editar)

    def _eliminar(_):
        if on_eliminar:
            abrir_form_brigada_eliminar(page, brigada=brigada, on_success=on_eliminar)

    def _agregar_miembros(_):
        if on_editar:
            abrir_form_brigada_agregar_miembros(page, brigada=brigada, on_success=on_editar)

    def _ver_detalle(_):
        _abrir_dialogo_detalle_brigada(page, brigada.get("idBrigada"), nombre, miembros)

    # Icono en header según si es propia o no
    icono_header = ft.Icons.SHIELD_OUTLINED if es_propia else ft.Icons.VISIBILITY_OUTLINED

    # Botones más compactos para que quepan todos (Ver detalles, Agregar miembros, Editar, Eliminar)
    botones = [
        ft.OutlinedButton(
            content=ft.Row([ft.Icon(ft.Icons.INFO_OUTLINED, size=16), ft.Text("Ver", size=11)], spacing=4),
            style=ft.ButtonStyle(side=ft.BorderSide(1, COLOR_BORDE), shape=ft.RoundedRectangleBorder(radius=6), color=COLOR_TEXTO, padding=ft.Padding(10, 6)),
            on_click=_ver_detalle,
        ),
    ]
    if not es_solo_lectura:
        botones.append(
            ft.OutlinedButton(
                content=ft.Row([ft.Icon(ft.Icons.PERSON_ADD_OUTLINED, size=16), ft.Text("Miembros", size=11)], spacing=4),
                style=ft.ButtonStyle(side=ft.BorderSide(1, color_primario), shape=ft.RoundedRectangleBorder(radius=6), color=COLOR_TEXTO, padding=ft.Padding(10, 6)),
                on_click=_agregar_miembros,
            )
        )
        botones.append(
            ft.OutlinedButton(
                content=ft.Row([ft.Icon(ft.Icons.EDIT_OUTLINED, size=16), ft.Text("Editar", size=11)], spacing=4),
                style=ft.ButtonStyle(side=ft.BorderSide(1, COLOR_BORDE), shape=ft.RoundedRectangleBorder(radius=6), color=COLOR_TEXTO, padding=ft.Padding(10, 6)),
                on_click=_editar,
            )
        )
        botones.append(
            ft.OutlinedButton(
                content=ft.Row([ft.Icon(ft.Icons.DELETE_OUTLINED, size=16), ft.Text("Eliminar", size=11)], spacing=4),
                style=ft.ButtonStyle(side=ft.BorderSide(1, "#f87171"), shape=ft.RoundedRectangleBorder(radius=6), color="#b91c1c", padding=ft.Padding(10, 6)),
                on_click=_eliminar,
            )
        )

    # Indicador si es brigada de otro profesor
    indicador_otro = None
    if not es_propia:
        indicador_otro = ft.Container(
            content=ft.Text("De otro profesor", size=11, color="white", weight="w500"),
            bgcolor=ft.Colors.with_opacity(0.3, "white"),
            padding=ft.Padding(8, 4, 8, 4),
            border_radius=4,
        )

    return ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(icono_header, color="white", size=28),
                            ft.Container(expand=True),
                            indicador_otro if indicador_otro else ft.Icon(ft.Icons.STAR_OUTLINE, color="white", size=22),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    padding=ft.Padding(20, 20, 20, 12),
                    border_radius=ft.BorderRadius.only(top_left=14, top_right=14),
                    gradient=ft.LinearGradient(
                        begin=ft.Alignment.TOP_LEFT,
                        end=ft.Alignment.BOTTOM_RIGHT,
                        colors=[color_primario, color_oscuro],
                    ),
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(nombre, size=18, weight="bold", color=COLOR_TEXTO),
                            ft.Text(responsable, size=14, color=COLOR_TEXTO_SEC),
                            ft.Container(height=14),
                            ft.Text(desc, size=14, color=COLOR_TEXTO_SEC),
                            ft.Container(height=20),
                            ft.Row(
                                [
                                    ft.Icon(ft.Icons.PEOPLE_OUTLINED, color=color_primario, size=22),
                                    ft.Text(f"Miembros activos: {miembros}", size=14, color=COLOR_TEXTO),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            ft.Container(height=16),
                            ft.Row(botones, spacing=8, wrap=True),
                        ],
                        spacing=0,
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                    ),
                    padding=24,
                    bgcolor=COLOR_CARD,
                    border_radius=ft.BorderRadius.only(bottom_left=14, bottom_right=14),
                ),
            ],
            spacing=0,
        ),
        width=380,
        border_radius=14,
        shadow=get_sombra_card(),
    )
