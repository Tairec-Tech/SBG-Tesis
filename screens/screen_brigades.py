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
from database.crud_brigada import listar_brigadas, listar_brigadas_para_profesor
from database.crud_usuario import es_admin, es_profesor


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
    
    # Admin puede crear brigadas; Profesor también puede
    puede_crear = es_admin(rol) or es_profesor(rol)
    
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
            # Profesor ve sus brigadas y las de otros profesores
            # Necesitamos la institución del profesor (la obtenemos de su brigada actual)
            # Por ahora usamos institucion_id=1 como fallback
            brigadas = listar_brigadas_para_profesor(user_id, 1)
        else:
            # Otros roles no ven brigadas en esta pantalla
            brigadas = []
    except Exception:
        brigadas = []
    
    if not brigadas:
        msg = "No hay brigadas registradas"
        if es_profesor(rol):
            msg = "Aún no tienes brigadas. ¡Crea tu primera brigada!"
        return card_principal(
            ft.Column(
                [
                    ft.Icon(ft.Icons.SHIELD_OUTLINED, color=COLOR_TEXTO_SEC, size=48),
                    ft.Container(height=16),
                    ft.Text(msg, size=16, weight="bold", color=COLOR_TEXTO),
                    ft.Text("Use «Agregar Brigada» para crear una.", size=14, color=COLOR_TEXTO_SEC),
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
        
        # Info del profesor si es de otro
        responsable = b.get("coordinador") or b.get("area_accion") or "—"
        if not es_propia and b.get("profesor_nombre"):
            responsable = f"Prof. {b.get('profesor_nombre', '')} {b.get('profesor_apellido', '')}"
        
        cards.append(
            _tarjeta_brigada(
                page,
                brigada=b,
                nombre=(b["nombre_brigada"] or "Brigada"),
                responsable=responsable,
                desc=(b.get("descripcion") or b.get("area_accion") or "Sin descripción"),
                miembros=b.get("num_miembros", 0),
                pct=0,
                color_identificador=b.get("color_identificador"),
                on_editar=refresh_callback if puede_editar else None,
                on_eliminar=refresh_callback if puede_eliminar else None,
                es_propia=es_propia,
                es_solo_lectura=not puede_editar,
            )
        )
    return ft.Row(cards, spacing=20, wrap=True)


def _tarjeta_brigada(page, brigada, nombre, responsable, desc, miembros, pct, color_identificador=None, on_editar=None, on_eliminar=None, es_propia=True, es_solo_lectura=False):
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
        # Para brigadas de solo lectura, mostrar detalles
        page.snack_bar = ft.SnackBar(ft.Text(f"Brigada: {nombre} - {miembros} miembros"))
        page.snack_bar.open = True
        page.update()

    # Icono en header según si es propia o no
    icono_header = ft.Icons.SHIELD_OUTLINED if es_propia else ft.Icons.VISIBILITY_OUTLINED
    
    # Construir botones según permisos
    botones = []
    if not es_solo_lectura:
        # Puede editar/agregar miembros
        botones.append(
            ft.OutlinedButton(
                content=ft.Row(
                    [ft.Icon(ft.Icons.PERSON_ADD_OUTLINED, size=18), ft.Text("Agregar miembros", size=13)],
                    spacing=6,
                ),
                style=ft.ButtonStyle(
                    side=ft.BorderSide(1, color_primario),
                    shape=ft.RoundedRectangleBorder(radius=8),
                ),
                on_click=_agregar_miembros,
            )
        )
        botones.append(
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
            )
        )
        botones.append(
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
            )
        )
    else:
        # Solo lectura: solo ver
        botones.append(
            ft.OutlinedButton(
                content=ft.Row(
                    [ft.Icon(ft.Icons.VISIBILITY_OUTLINED, size=18), ft.Text("Ver detalles", size=13)],
                    spacing=6,
                ),
                style=ft.ButtonStyle(
                    side=ft.BorderSide(1, COLOR_BORDE),
                    shape=ft.RoundedRectangleBorder(radius=8),
                ),
                on_click=_ver_detalle,
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
                                    ft.Text(f"Miembros Activos: {miembros}", size=14, color=COLOR_TEXTO),
                                    ft.Container(expand=True),
                                    ft.Container(
                                        content=ft.Stack(
                                            [
                                                ft.Container(
                                                    content=ft.Text(f"{pct}%", size=12, weight="bold", color=color_primario),
                                                    alignment=ft.Alignment.CENTER,
                                                    width=48,
                                                    height=48,
                                                ),
                                                ft.ProgressRing(width=48, height=48, value=pct / 100 if pct else 0, color=color_primario, stroke_width=4),
                                            ],
                                        ),
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            ft.Container(height=20),
                            ft.Row(botones, spacing=12),
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
        width=520,
        border_radius=14,
        shadow=get_sombra_card(),
    )
