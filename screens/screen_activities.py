"""Pantalla de gestión de Actividades — estilo Figma, tema brigadas ambientales."""
import flet as ft
from datetime import date
from theme import (
    COLOR_FONDO_VERDE,
    COLOR_TEXTO,
    COLOR_TEXTO_SEC,
    COLOR_PRIMARIO,
    COLOR_CARD,
    COLOR_BORDE,
    RADIO,
    get_sombra_suave,
)
from components import (
    card_principal,
    titulo_pagina,
    boton_primario,
)
from forms import (
    _campo_texto,
    _campo_con_titulo,
    _cerrar_dialogo,
    _abrir_dialogo,
)
import database.crud_actividad as crud_act
import database.crud_brigada as crud_brigada
from database.crud_usuario import es_admin, es_profesor
import json


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


def _abrir_modal_crear_actividad(page: ft.Page, on_success=None, usuario_actual=None):
    """Abre un diálogo para crear nueva actividad — mismo patrón que forms.py.
    Si el usuario es profesor, auto-asigna su brigada (sin dropdown).
    Si es admin, muestra dropdown con todas las brigadas.
    """
    usuario_actual = usuario_actual or {}
    rol = usuario_actual.get("rol", "")
    user_id = usuario_actual.get("id")

    _CAMPO = dict(
        border_color=COLOR_BORDE,
        focused_border_color=COLOR_PRIMARIO,
        border_radius=RADIO,
        text_size=14,
        color=COLOR_TEXTO,
        cursor_color=COLOR_PRIMARIO,
    )
    titulo_campo = ft.TextField(
        hint_text="Nombre de la actividad",
        content_padding=ft.Padding(14, 20),
        **_CAMPO,
    )
    descripcion_campo = ft.TextField(
        hint_text="Descripción de la actividad",
        multiline=True,
        min_lines=4,
        max_lines=6,
        content_padding=ft.Padding(14, 20),
        **_CAMPO,
    )
    fecha_inicio_campo = ft.TextField(
        hint_text="YYYY-MM-DD",
        value=str(date.today()),
        content_padding=ft.Padding(14, 20),
        **_CAMPO,
    )
    fecha_fin_campo = ft.TextField(
        hint_text="YYYY-MM-DD",
        value=str(date.today()),
        content_padding=ft.Padding(14, 20),
        **_CAMPO,
    )

    # --- Lógica de Brigadas según rol ---
    brigada_id_fija = None   # Para profesores con una sola brigada
    dd_brigada = None        # Dropdown (solo se muestra si hay varias opciones)
    brigada_info_text = None # Texto informativo cuando se auto-asigna

    try:
        if es_profesor(rol) and user_id:
            # Profesor: solo sus brigadas
            institucion_id = usuario_actual.get("institucion_id") or 1
            todas = crud_brigada.listar_brigadas_para_profesor(user_id, institucion_id)
            mis_brigadas = [b for b in todas if b.get("es_propia", False) or b.get("profesor_id") == user_id]

            if len(mis_brigadas) == 1:
                # Solo tiene una brigada → auto-asignar, sin dropdown
                brigada_id_fija = mis_brigadas[0]["idBrigada"]
                brigada_info_text = ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.SHIELD_OUTLINED, size=16, color=COLOR_PRIMARIO),
                            ft.Text(
                                f"Brigada: {mis_brigadas[0]['nombre_brigada']}",
                                size=14, weight="w600", color=COLOR_PRIMARIO,
                            ),
                            ft.Text("(asignada automáticamente)", size=12, color=COLOR_TEXTO_SEC),
                        ],
                        spacing=8,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=ft.Padding(14, 16, 14, 16),
                    bgcolor="#e8f5e9",
                    border_radius=RADIO,
                    border=ft.Border.all(1, COLOR_PRIMARIO),
                )
            elif len(mis_brigadas) > 1:
                # Varias brigadas propias → mostrar dropdown solo con las suyas
                opciones = [ft.dropdown.Option(str(b["idBrigada"]), b["nombre_brigada"]) for b in mis_brigadas]
                dd_brigada = ft.Dropdown(
                    label="Seleccionar Brigada",
                    hint_text="Elige una de tus brigadas",
                    options=opciones,
                    value=opciones[0].key,
                    border_color=COLOR_BORDE, focused_border_color=COLOR_PRIMARIO,
                    text_size=14, color=COLOR_TEXTO,
                    content_padding=ft.Padding(12, 14), border_radius=RADIO, dense=True,
                )
            else:
                # Sin brigadas
                brigada_info_text = ft.Text("No tienes brigadas asignadas.", size=13, color="#ef4444", italic=True)
        else:
            # Admin u otro rol → todas las brigadas
            brigadas_disponibles = crud_brigada.listar_brigadas()
            opciones = [ft.dropdown.Option(str(b["idBrigada"]), b["nombre_brigada"]) for b in brigadas_disponibles]
            dd_brigada = ft.Dropdown(
                label="Asignar a Brigada",
                hint_text="Seleccione una brigada",
                options=opciones,
                border_color=COLOR_BORDE, focused_border_color=COLOR_PRIMARIO,
                text_size=14, color=COLOR_TEXTO,
                content_padding=ft.Padding(12, 14), border_radius=RADIO, dense=True,
            )
            if opciones:
                dd_brigada.value = opciones[0].key
    except Exception:
        brigadas_disponibles = []

    dd_estado = ft.Dropdown(
        label="Estado Inicial",
        options=[
            ft.dropdown.Option("Pendiente"),
            ft.dropdown.Option("En Progreso"),
            ft.dropdown.Option("Completada"),
        ],
        value="Pendiente",
        border_color=COLOR_BORDE, focused_border_color=COLOR_PRIMARIO,
        text_size=14, color=COLOR_TEXTO,
        content_padding=ft.Padding(12, 14), border_radius=RADIO, dense=True,
    )

    def _get_brigada_id():
        """Obtiene el ID de brigada seleccionado (fija o del dropdown)."""
        if brigada_id_fija:
            return brigada_id_fija
        if dd_brigada and dd_brigada.value:
            return int(dd_brigada.value)
        return None

    def on_guardar(_):
        if not titulo_campo.value or not titulo_campo.value.strip():
            page.snack_bar = ft.SnackBar(ft.Text("El título es obligatorio."), bgcolor="#ef4444")
            page.snack_bar.open = True
            page.update()
            return

        id_brigada = _get_brigada_id()
        if not id_brigada:
            page.snack_bar = ft.SnackBar(ft.Text("No hay brigada asignada."), bgcolor="#ef4444")
            page.snack_bar.open = True
            page.update()
            return

        try:
            res = crud_act.crear_actividad(
                titulo_campo.value.strip(),
                (descripcion_campo.value or "").strip(),
                fecha_inicio_campo.value.strip(),
                fecha_fin_campo.value.strip(),
                dd_estado.value,
                id_brigada,
            )
            created = bool(res)
        except Exception as e:
            created = False
            print(f"Error creando actividad: {e}")

        if created:
            _cerrar_dialogo(page)
            page.snack_bar = ft.SnackBar(ft.Text("¡Actividad creada correctamente!"), bgcolor="#22c55e")
            page.snack_bar.open = True
            if on_success:
                on_success()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Error al crear la actividad."), bgcolor="#ef4444")
            page.snack_bar.open = True
        page.update()

    # --- Construir contenido del formulario ---
    campos = [
        _campo_con_titulo("Título de la Actividad *", titulo_campo),
        _campo_con_titulo("Descripción", descripcion_campo),
        ft.Row(
            [
                ft.Container(content=_campo_con_titulo("Fecha Inicio", fecha_inicio_campo), expand=True),
                ft.Container(width=12),
                ft.Container(content=_campo_con_titulo("Fecha Fin", fecha_fin_campo), expand=True),
            ],
            spacing=0,
        ),
    ]

    # Brigada: info fija o dropdown según rol
    if brigada_info_text:
        campos.append(_campo_con_titulo("Brigada", brigada_info_text))
    elif dd_brigada:
        campos.append(_campo_con_titulo("Brigada", dd_brigada))

    campos.append(_campo_con_titulo("Estado", dd_estado, espaciado_abajo=0))

    contenido = ft.Column(campos, spacing=0)


    dialogo = ft.AlertDialog(
        modal=True,
        bgcolor=COLOR_CARD,
        title=ft.Text("Nueva Actividad", size=18, weight="w600", color=COLOR_TEXTO),
        content=ft.Container(
            content=ft.Column([contenido], scroll=ft.ScrollMode.AUTO, tight=True),
            width=520,
            bgcolor=COLOR_CARD,
        ),
        actions=[
            ft.TextButton(
                content=ft.Text("Cancelar", color=COLOR_TEXTO, weight=ft.FontWeight.W_500),
                style=ft.ButtonStyle(color=COLOR_TEXTO),
                on_click=lambda e: _cerrar_dialogo(e.page),
            ),
            ft.FilledButton(
                "Guardar",
                style=ft.ButtonStyle(bgcolor=COLOR_PRIMARIO, color="white"),
                on_click=on_guardar,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    _abrir_dialogo(page, dialogo)


def card_actividad(act):
    """Tarjeta detallada de actividad."""
    titulo = act.get("titulo", "Sin título")
    descripcion = act.get("descripcion", "")
    fecha_inicio = str(act.get("fecha_inicio", ""))
    estado = act.get("estado", "Pendiente")
    brigada = act.get("nombre_brigada", "General")

    color_estado = {
        "Completada": ft.Colors.GREEN,
        "Pendiente": ft.Colors.ORANGE,
        "En Progreso": ft.Colors.BLUE,
        "Cancelada": ft.Colors.RED,
    }.get(estado, ft.Colors.GREY)

    return ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(titulo, size=16, weight="bold", color=COLOR_TEXTO, expand=True),
                        ft.Container(
                            content=ft.Text(estado, size=10, weight="bold", color="white"),
                            padding=ft.Padding.symmetric(horizontal=8, vertical=4),
                            border_radius=12,
                            bgcolor=color_estado,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Container(height=4),
                ft.Text(descripcion, size=13, color=COLOR_TEXTO_SEC, max_lines=2, overflow=ft.TextOverflow.ELLIPSIS),
                ft.Container(height=8),
                ft.Row(
                    [
                        ft.Icon(ft.Icons.SHIELD_OUTLINED, size=14, color=COLOR_PRIMARIO),
                        ft.Text(brigada, size=12, color=COLOR_PRIMARIO, weight="w600"),
                        ft.Container(width=10),
                        ft.Icon(ft.Icons.CALENDAR_TODAY, size=14, color=COLOR_TEXTO_SEC),
                        ft.Text(fecha_inicio, size=12, color=COLOR_TEXTO_SEC),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],
            spacing=0,
        ),
        padding=16,
        bgcolor=COLOR_CARD,
        border_radius=RADIO,
        border=ft.Border.all(1, COLOR_BORDE),
        shadow=get_sombra_suave(),
        margin=ft.margin.only(bottom=10),
    )


def build(page: ft.Page, content_area=None, **kwargs) -> ft.Control:
    # Obtener usuario actual para permisos
    usuario = _obtener_usuario_actual(page)

    def refresh():
        if content_area:
            content_area.content = build(page, content_area)
            page.update()

    # 1. Obtener datos
    try:
        actividades = crud_act.obtener_actividades_recientes(50)
    except Exception:
        actividades = []

    lista_items = ft.Column(spacing=0, scroll=ft.ScrollMode.AUTO)

    if actividades:
        for act in actividades:
            lista_items.controls.append(card_actividad(act))
    else:
        lista_items.controls.append(
            ft.Text("No hay actividades registradas.", color=COLOR_TEXTO_SEC, italic=True)
        )

    def on_nueva_click(_):
        _abrir_modal_crear_actividad(page, on_success=refresh, usuario_actual=usuario)


    # --- Estructura Principal ---
    contenido = ft.Column(
        [
            titulo_pagina(
                "Actividades",
                "Gestión y seguimiento de actividades de las brigadas",
                accion=boton_primario("Nueva Actividad", ft.Icons.ADD, on_click=on_nueva_click),
            ),
            ft.Container(height=24),
            lista_items,
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
