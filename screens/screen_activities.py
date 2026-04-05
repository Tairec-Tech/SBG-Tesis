"""Pantalla de gestión de Actividades — SBE.
Funcionalidad:
- Por defecto muestra solo las actividades del profesor actual.
- Toggle para ver las actividades de otros (solo lectura).
- Acciones sobre las propias: completar, editar, eliminar.
- Admin puede operar sobre todas.
"""
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


# ─── Modal: Crear / Editar actividad ─────────────────────────────────

def _abrir_modal_actividad(page: ft.Page, on_success=None, usuario_actual=None, actividad=None):
    """
    Abre un diálogo para crear o editar una actividad.
    Si 'actividad' es un dict, precarga datos y al guardar actualiza.
    """
    usuario_actual = usuario_actual or {}
    rol = usuario_actual.get("rol", "")
    user_id = usuario_actual.get("id")
    editando = actividad is not None
    from datetime import datetime

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
        value=actividad.get("titulo", "") if editando else "",
        content_padding=ft.Padding(14, 20),
        **_CAMPO,
    )
    descripcion_campo = ft.TextField(
        hint_text="Descripción de la actividad",
        value=actividad.get("descripcion", "") if editando else "",
        multiline=True,
        min_lines=4,
        max_lines=6,
        content_padding=ft.Padding(14, 20),
        **_CAMPO,
    )

    # ── DatePicker nativo para fechas (mismo patrón que turnos) ──
    _MESES = {1:"Ene",2:"Feb",3:"Mar",4:"Abr",5:"May",6:"Jun",
              7:"Jul",8:"Ago",9:"Sep",10:"Oct",11:"Nov",12:"Dic"}

    def _format_fecha(d):
        if d:
            return f"{d.day:02d}/{_MESES.get(d.month,'')}/{d.year}"
        return "Seleccionar fecha…"

    # Estado de fechas seleccionadas
    _fecha_ini_default = None
    _fecha_fin_default = None
    if editando:
        fi = actividad.get("fecha_inicio")
        ff = actividad.get("fecha_fin")
        _fecha_ini_default = fi if isinstance(fi, date) else date.today()
        _fecha_fin_default = ff if isinstance(ff, date) else date.today()
    else:
        _fecha_ini_default = date.today()
        _fecha_fin_default = date.today()

    _fecha_ini_sel = {"valor": _fecha_ini_default}
    _fecha_fin_sel = {"valor": _fecha_fin_default}

    texto_fecha_ini = ft.Text(
        _format_fecha(_fecha_ini_default), size=14,
        color=COLOR_TEXTO if _fecha_ini_default else COLOR_TEXTO_SEC, expand=True,
    )
    texto_fecha_fin = ft.Text(
        _format_fecha(_fecha_fin_default), size=14,
        color=COLOR_TEXTO if _fecha_fin_default else COLOR_TEXTO_SEC, expand=True,
    )

    def _on_fecha_ini_change(e):
        picked = e.control.value
        if picked:
            if isinstance(picked, datetime):
                picked = picked.date()
            _fecha_ini_sel["valor"] = picked
            texto_fecha_ini.value = _format_fecha(picked)
            texto_fecha_ini.color = COLOR_TEXTO
            page.update()

    def _on_fecha_fin_change(e):
        picked = e.control.value
        if picked:
            if isinstance(picked, datetime):
                picked = picked.date()
            _fecha_fin_sel["valor"] = picked
            texto_fecha_fin.value = _format_fecha(picked)
            texto_fecha_fin.color = COLOR_TEXTO
            page.update()

    date_picker_ini = ft.DatePicker(
        first_date=date(2024, 1, 1),
        last_date=date(2030, 12, 31),
        value=_fecha_ini_default,
        on_change=_on_fecha_ini_change,
    )
    date_picker_fin = ft.DatePicker(
        first_date=date(2024, 1, 1),
        last_date=date(2030, 12, 31),
        value=_fecha_fin_default,
        on_change=_on_fecha_fin_change,
    )

    page.overlay.append(date_picker_ini)
    page.overlay.append(date_picker_fin)

    def _abrir_fecha_ini(_):
        date_picker_ini.open = True
        page.update()

    def _abrir_fecha_fin(_):
        date_picker_fin.open = True
        page.update()

    def _limpiar_overlay():
        for p in (date_picker_ini, date_picker_fin):
            if p in page.overlay:
                page.overlay.remove(p)

    boton_fecha_ini = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.CALENDAR_MONTH_ROUNDED, size=20, color=COLOR_PRIMARIO),
                ft.Container(width=8),
                texto_fecha_ini,
                ft.Icon(ft.Icons.ARROW_DROP_DOWN, size=20, color=COLOR_TEXTO_SEC),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.Padding(14, 12, 14, 12),
        border=ft.Border.all(1, COLOR_BORDE),
        border_radius=RADIO,
        bgcolor=COLOR_CARD,
        on_click=_abrir_fecha_ini,
        ink=True,
    )

    boton_fecha_fin = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.CALENDAR_MONTH_ROUNDED, size=20, color=COLOR_PRIMARIO),
                ft.Container(width=8),
                texto_fecha_fin,
                ft.Icon(ft.Icons.ARROW_DROP_DOWN, size=20, color=COLOR_TEXTO_SEC),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.Padding(14, 12, 14, 12),
        border=ft.Border.all(1, COLOR_BORDE),
        border_radius=RADIO,
        bgcolor=COLOR_CARD,
        on_click=_abrir_fecha_fin,
        ink=True,
    )

    brigada_id_fija = None
    dd_brigada = None
    brigada_info_text = None

    if editando:
        brigada_id_fija = actividad.get("Brigada_idBrigada")
        nombre_brigada = actividad.get("nombre_brigada", "Brigada")
        brigada_info_text = ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.SHIELD_OUTLINED, size=16, color=COLOR_PRIMARIO),
                    ft.Text(
                        f"Brigada: {nombre_brigada}",
                        size=14, weight="w600", color=COLOR_PRIMARIO,
                    ),
                ],
                spacing=8,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.Padding(14, 16, 14, 16),
            bgcolor="#e8f5e9",
            border_radius=RADIO,
            border=ft.Border.all(1, COLOR_PRIMARIO),
        )
    else:
        try:
            _tb = (page.data or {}).get("brigada_activa")
            if es_profesor(rol) and user_id:
                institucion_id = usuario_actual.get("institucion_id")
                if not institucion_id:
                    raise ValueError("Sesión sin institución válida para crear actividades.")
                todas = crud_brigada.listar_brigadas_para_profesor(user_id, institucion_id, _tb)
                mis_brigadas = [b for b in todas if b.get("es_propia", False) or b.get("profesor_id") == user_id]

                if len(mis_brigadas) == 1:
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
                    brigada_info_text = ft.Text("No tienes brigadas asignadas.", size=13, color="#ef4444", italic=True)
            else:
                brigadas_disponibles = crud_brigada.listar_brigadas(_tb)
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
        except Exception as e:
            brigada_info_text = ft.Text(str(e), size=13, color="#ef4444", italic=True)

    estado_actual = actividad.get("estado", "Pendiente") if editando else "Pendiente"
    dd_estado = ft.Dropdown(
        label="Estado",
        options=[
            ft.dropdown.Option("Pendiente"),
            ft.dropdown.Option("En Progreso"),
            ft.dropdown.Option("Completada"),
        ],
        value=estado_actual,
        border_color=COLOR_BORDE, focused_border_color=COLOR_PRIMARIO,
        text_size=14, color=COLOR_TEXTO,
        content_padding=ft.Padding(12, 14), border_radius=RADIO, dense=True,
    )

    def _get_brigada_id():
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

        fi = _fecha_ini_sel["valor"]
        ff = _fecha_fin_sel["valor"]
        if not fi or not ff:
            page.snack_bar = ft.SnackBar(ft.Text("Seleccione ambas fechas."), bgcolor="#ef4444")
            page.snack_bar.open = True
            page.update()
            return

        fecha_inicio_str = str(fi)
        fecha_fin_str = str(ff)

        try:
            if editando:
                ok = crud_act.actualizar_actividad(
                    id_actividad=actividad["idActividad"],
                    titulo=titulo_campo.value.strip(),
                    descripcion=(descripcion_campo.value or "").strip(),
                    fecha_inicio=fecha_inicio_str,
                    fecha_fin=fecha_fin_str,
                    estado=dd_estado.value,
                    usuario_id=user_id,
                    es_admin_usuario=es_admin(rol),
                )
                success = ok
            else:
                res = crud_act.crear_actividad(
                    titulo_campo.value.strip(),
                    (descripcion_campo.value or "").strip(),
                    fecha_inicio_str,
                    fecha_fin_str,
                    dd_estado.value,
                    id_brigada,
                    usuario_creador_id=user_id,
                )
                success = bool(res)
        except Exception as e:
            success = False
            print(f"Error {'editando' if editando else 'creando'} actividad: {e}")

        if success:
            _limpiar_overlay()
            _cerrar_dialogo(page)
            msg = "¡Actividad actualizada!" if editando else "¡Actividad creada correctamente!"
            page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor="#22c55e")
            page.snack_bar.open = True
            if on_success:
                on_success()
        else:
            msg = "Error al actualizar la actividad." if editando else "Error al crear la actividad."
            page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor="#ef4444")
            page.snack_bar.open = True
        page.update()

    campos = [
        _campo_con_titulo("Título de la Actividad *", titulo_campo),
        _campo_con_titulo("Descripción", descripcion_campo),
        ft.Row(
            [
                ft.Container(content=_campo_con_titulo("Fecha Inicio", boton_fecha_ini), expand=True),
                ft.Container(width=12),
                ft.Container(content=_campo_con_titulo("Fecha Fin", boton_fecha_fin), expand=True),
            ],
            spacing=0,
        ),
    ]

    if brigada_info_text:
        campos.append(_campo_con_titulo("Brigada", brigada_info_text))
    elif dd_brigada:
        campos.append(_campo_con_titulo("Brigada", dd_brigada))

    campos.append(_campo_con_titulo("Estado", dd_estado, espaciado_abajo=0))
    contenido = ft.Column(campos, spacing=0)

    titulo_modal = "Editar Actividad" if editando else "Nueva Actividad"
    boton_texto = "Guardar" if editando else "Crear"

    def _on_cancelar(e):
        _limpiar_overlay()
        _cerrar_dialogo(e.page)

    dialogo = ft.AlertDialog(
        modal=True,
        bgcolor=COLOR_CARD,
        title=ft.Text(titulo_modal, size=18, weight="w600", color=COLOR_TEXTO),
        content=ft.Container(
            content=ft.Column([contenido], scroll=ft.ScrollMode.AUTO, tight=True),
            width=520,
            bgcolor=COLOR_CARD,
        ),
        actions=[
            ft.TextButton(
                content=ft.Text("Cancelar", color=COLOR_TEXTO, weight=ft.FontWeight.W_500),
                style=ft.ButtonStyle(color=COLOR_TEXTO),
                on_click=_on_cancelar,
            ),
            ft.FilledButton(
                boton_texto,
                style=ft.ButtonStyle(bgcolor=COLOR_PRIMARIO, color="white"),
                on_click=on_guardar,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    _abrir_dialogo(page, dialogo)


# ─── Modal: Confirmar eliminación ─────────────────────────────────────

def _abrir_modal_eliminar(page: ft.Page, actividad: dict, on_success=None, usuario_actual=None):
    """Diálogo de confirmación para eliminar una actividad."""
    usuario_actual = usuario_actual or {}
    rol = usuario_actual.get("rol", "")
    user_id = usuario_actual.get("id")
    titulo = actividad.get("titulo", "esta actividad")

    def on_confirmar(_):
        err = crud_act.eliminar_actividad(
            id_actividad=actividad["idActividad"],
            usuario_id=user_id,
            es_admin_usuario=es_admin(rol),
        )
        _cerrar_dialogo(page)
        if err:
            page.snack_bar = ft.SnackBar(ft.Text(err), bgcolor="#ef4444")
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Actividad eliminada."), bgcolor="#22c55e")
            if on_success:
                on_success()
        page.snack_bar.open = True
        page.update()

    dialogo = ft.AlertDialog(
        modal=True,
        bgcolor=COLOR_CARD,
        title=ft.Text("Eliminar Actividad", size=18, weight="w600", color=COLOR_TEXTO),
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Esta acción no se puede deshacer. Se eliminará la actividad y sus datos asociados.",
                        size=13, color=COLOR_TEXTO_SEC,
                    ),
                    ft.Container(height=12),
                    ft.Text(f'¿Eliminar «{titulo}»?', size=14, weight="w600", color=COLOR_TEXTO),
                ],
                spacing=0,
            ),
            width=420,
            bgcolor=COLOR_CARD,
        ),
        actions=[
            ft.TextButton(
                content=ft.Text("Cancelar", color=COLOR_TEXTO, weight=ft.FontWeight.W_500),
                style=ft.ButtonStyle(color=COLOR_TEXTO),
                on_click=lambda e: _cerrar_dialogo(e.page),
            ),
            ft.FilledButton(
                "Eliminar",
                style=ft.ButtonStyle(bgcolor="#ef4444", color="white"),
                on_click=on_confirmar,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    _abrir_dialogo(page, dialogo)


# ─── Tarjeta de actividad ────────────────────────────────────────────

def card_actividad(act, usuario_actual, on_complete=None, on_edit=None, on_delete=None, solo_lectura=False):
    """Tarjeta detallada de actividad con acciones condicionales."""
    titulo = act.get("titulo", "Sin título")
    descripcion = act.get("descripcion", "")
    fecha_inicio = str(act.get("fecha_inicio", ""))
    fecha_fin = str(act.get("fecha_fin", ""))
    estado = act.get("estado", "Pendiente")
    brigada = act.get("nombre_brigada", "General")
    creador_id = act.get("creador_id")

    rol = usuario_actual.get("rol", "") if usuario_actual else ""
    usuario_id = usuario_actual.get("id") if usuario_actual else None

    es_propietario = usuario_id is not None and (es_admin(rol) or creador_id == usuario_id)
    puede_actuar = es_propietario and not solo_lectura

    puede_completar = puede_actuar and estado != "Completada"
    puede_editar = puede_actuar
    puede_eliminar = puede_actuar

    color_estado = {
        "Completada": ft.Colors.GREEN,
        "Pendiente": ft.Colors.ORANGE,
        "En Progreso": ft.Colors.BLUE,
        "Cancelada": ft.Colors.RED,
    }.get(estado, ft.Colors.GREY)

    acciones = []
    if puede_completar:
        acciones.append(
            ft.IconButton(
                icon=ft.Icons.CHECK_CIRCLE_OUTLINE_ROUNDED,
                icon_color="#22c55e",
                icon_size=20,
                tooltip="Marcar como completada",
                style=ft.ButtonStyle(padding=4),
                width=34, height=34,
                on_click=lambda e, aid=act["idActividad"]: on_complete(aid) if on_complete else None,
            )
        )
    if puede_editar:
        acciones.append(
            ft.IconButton(
                icon=ft.Icons.EDIT_OUTLINED,
                icon_color=COLOR_PRIMARIO,
                icon_size=20,
                tooltip="Editar actividad",
                style=ft.ButtonStyle(padding=4),
                width=34, height=34,
                on_click=lambda e, a=act: on_edit(a) if on_edit else None,
            )
        )
    if puede_eliminar:
        acciones.append(
            ft.IconButton(
                icon=ft.Icons.DELETE_OUTLINE_ROUNDED,
                icon_color="#ef4444",
                icon_size=20,
                tooltip="Eliminar actividad",
                style=ft.ButtonStyle(padding=4),
                width=34, height=34,
                on_click=lambda e, a=act: on_delete(a) if on_delete else None,
            )
        )

    # Badge de solo lectura si la actividad es de otro profesor
    badge_ajeno = []
    if solo_lectura and not es_admin(rol):
        badge_ajeno.append(
            ft.Container(
                content=ft.Text("Solo lectura", size=9, color=COLOR_TEXTO_SEC, italic=True),
                padding=ft.Padding(6, 2, 6, 2),
                border_radius=8,
                border=ft.Border.all(1, COLOR_BORDE),
            )
        )

    return ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(titulo, size=16, weight="bold", color=COLOR_TEXTO, expand=True),
                        *acciones,
                        *badge_ajeno,
                        ft.Container(
                            content=ft.Text(estado, size=10, weight="bold", color="white"),
                            padding=ft.Padding.symmetric(horizontal=8, vertical=4),
                            border_radius=12,
                            bgcolor=color_estado,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
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
                        ft.Text(f"{fecha_inicio}  →  {fecha_fin}", size=12, color=COLOR_TEXTO_SEC),
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


# ─── Pantalla principal ──────────────────────────────────────────────

def build(page: ft.Page, content_area=None, **kwargs) -> ft.Control:
    usuario = _obtener_usuario_actual(page)
    rol = usuario.get("rol", "")
    user_id = usuario.get("id")
    es_prof = es_profesor(rol)

    # Estado: ¿ver solo mis actividades? — persistido en page.data para sobrevivir rebuilds
    _key = "_act_ver_solo_mias"
    if _key not in (page.data or {}):
        if page.data is None:
            page.data = {}
        page.data[_key] = es_prof
    ver_solo_mias = {"value": page.data.get(_key, es_prof)}

    def refresh():
        if content_area:
            content_area.content = build(page, content_area)
            page.update()

    _tb = (page.data or {}).get("brigada_activa")

    # ─── Callbacks de acciones ────────────────────────────────────
    def on_completar(id_actividad: int):
        exito = crud_act.marcar_actividad_completada(
            id_actividad=id_actividad,
            usuario_id=user_id,
            es_admin_usuario=es_admin(rol),
        )
        if exito:
            page.snack_bar = ft.SnackBar(ft.Text("Actividad marcada como completada."), bgcolor="#22c55e")
            page.snack_bar.open = True
            refresh()
        else:
            page.snack_bar = ft.SnackBar(
                ft.Text("No se pudo cambiar el estado. Verifique permisos."),
                bgcolor="#ef4444",
            )
            page.snack_bar.open = True
            page.update()

    def on_editar(act: dict):
        _abrir_modal_actividad(page, on_success=refresh, usuario_actual=usuario, actividad=act)

    def on_eliminar(act: dict):
        _abrir_modal_eliminar(page, actividad=act, on_success=refresh, usuario_actual=usuario)

    def on_nueva_click(_):
        _abrir_modal_actividad(page, on_success=refresh, usuario_actual=usuario)

    # ─── Construir lista de actividades ───────────────────────────
    def _construir_lista():
        lista_items = ft.Column(spacing=0, scroll=ft.ScrollMode.AUTO)

        filtro_usuario = user_id if (ver_solo_mias["value"] and es_prof) else None

        try:
            actividades = crud_act.obtener_actividades_recientes(
                50, tipo_brigada=_tb, solo_usuario_id=filtro_usuario,
            )
        except Exception:
            actividades = []

        if actividades:
            for act in actividades:
                es_ajena = (user_id is not None and act.get("creador_id") != user_id and not es_admin(rol))
                lista_items.controls.append(
                    card_actividad(
                        act, usuario,
                        on_complete=on_completar,
                        on_edit=on_editar,
                        on_delete=on_eliminar,
                        solo_lectura=es_ajena,
                    )
                )
        else:
            msg = "No tienes actividades registradas." if ver_solo_mias["value"] else "No hay actividades registradas."
            lista_items.controls.append(
                ft.Text(msg, color=COLOR_TEXTO_SEC, italic=True)
            )
        return lista_items

    lista_ref = ft.Ref[ft.Column]()

    # ─── Toggle de filtro ─────────────────────────────────────────
    toggle_filtro = None
    if es_prof:
        def on_toggle_cambio(e):
            page.data[_key] = e.control.value
            refresh()

        toggle_filtro = ft.Row(
            [
                ft.Switch(
                    value=ver_solo_mias["value"],
                    active_color=COLOR_PRIMARIO,
                    on_change=on_toggle_cambio,
                ),
                ft.Text(
                    "Solo mis actividades",
                    size=13, color=COLOR_TEXTO_SEC, weight="w500",
                ),
            ],
            spacing=8,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    # ─── Estructura Principal ─────────────────────────────────────
    header_items = [
        titulo_pagina(
            "Actividades",
            "Gestión y seguimiento de actividades de las brigadas",
            accion=boton_primario("Nueva Actividad", ft.Icons.ADD, on_click=on_nueva_click),
        ),
    ]

    if toggle_filtro:
        header_items.append(ft.Container(height=8))
        header_items.append(
            ft.Container(
                content=toggle_filtro,
                padding=ft.Padding(12, 8, 12, 8),
                border_radius=RADIO,
                bgcolor=COLOR_CARD,
                border=ft.Border.all(1, COLOR_BORDE),
            )
        )

    header_items.append(ft.Container(height=16))
    header_items.append(_construir_lista())

    contenido = ft.Column(
        header_items,
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
