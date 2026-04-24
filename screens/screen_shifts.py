"""Calendario de Brigada — diseño premium con timeline y cards enriquecidas.
Incluye edición/eliminación condicional por permisos de profesor."""

import flet as ft
from datetime import timedelta, date, datetime
import json
from theme import (
    COLOR_PRIMARIO,
    COLOR_PRIMARIO_CLARO,
    COLOR_TEXTO,
    COLOR_TEXTO_SEC,
    COLOR_CARD,
    COLOR_BORDE,
    COLOR_FONDO_VERDE,
    RADIO,
    get_sombra_card,
)
from components import titulo_pagina, boton_primario
from forms import _campo_con_titulo, _cerrar_dialogo, _abrir_dialogo
import database.crud_turno as crud_turno
from database.crud_usuario import es_admin


def _obtener_usuario_actual(page: ft.Page) -> dict:
    try:
        if getattr(page, "data", None) and isinstance(page.data.get("usuario_actual"), dict):
            return page.data["usuario_actual"]
        usuario_json = page.client_storage.get("usuario_actual")
        if usuario_json:
            return json.loads(usuario_json) if isinstance(usuario_json, str) else (usuario_json or {})
    except Exception:
        pass
    return {}


# ═══════════════════════════════════════════════════════════
#  Modal de edición de turno
# ═══════════════════════════════════════════════════════════

def _abrir_modal_editar_turno(page: ft.Page, turno: dict, usuario: dict, on_success=None):
    """Modal para editar un turno existente con DatePicker y TimePicker nativos."""
    brigada_rol_id = usuario.get("Brigada_idBrigada") if not es_admin(usuario.get("rol", "")) else None
    _MESES = {1:"Ene",2:"Feb",3:"Mar",4:"Abr",5:"May",6:"Jun",
              7:"Jul",8:"Ago",9:"Sep",10:"Oct",11:"Nov",12:"Dic"}

    def _format_fecha(d):
        if d:
            return f"{d.day:02d}/{_MESES.get(d.month,'')}/{d.year}"
        return "Seleccionar…"

    def _parse_time(t):
        """Convierte timedelta o time a (hour, minute)."""
        if isinstance(t, timedelta):
            total = int(t.total_seconds())
            h, m = divmod(total, 3600)
            return h, m // 60
        try:
            return t.hour, t.minute
        except Exception:
            return 0, 0

    # Estado inicial desde el turno
    fecha_actual = turno["fecha"] if isinstance(turno["fecha"], date) else date.today()
    hi_h, hi_m = _parse_time(turno["hora_inicio"])
    hf_h, hf_m = _parse_time(turno["hora_fin"])

    from datetime import time as dt_time
    _fecha_sel = {"valor": fecha_actual}
    _hora_ini_sel = {"valor": dt_time(hi_h, hi_m)}
    _hora_fin_sel = {"valor": dt_time(hf_h, hf_m)}

    texto_fecha = ft.Text(_format_fecha(fecha_actual), size=14, color=COLOR_TEXTO, expand=True)
    texto_hora_ini = ft.Text(f"{hi_h:02d}:{hi_m:02d}", size=14, color=COLOR_TEXTO, expand=True)
    texto_hora_fin = ft.Text(f"{hf_h:02d}:{hf_m:02d}", size=14, color=COLOR_TEXTO, expand=True)

    # DatePicker
    def _on_fecha_change(e):
        picked = e.control.value
        if picked:
            if isinstance(picked, datetime):
                picked = picked.date()
            _fecha_sel["valor"] = picked
            texto_fecha.value = _format_fecha(picked)
            page.update()

    date_picker = ft.DatePicker(
        first_date=date(2024, 1, 1), last_date=date(2030, 12, 31),
        value=fecha_actual, on_change=_on_fecha_change,
    )

    # TimePickers
    def _on_hora_ini_change(e):
        picked = e.control.value
        if picked:
            _hora_ini_sel["valor"] = picked
            texto_hora_ini.value = f"{picked.hour:02d}:{picked.minute:02d}"
            page.update()

    def _on_hora_fin_change(e):
        picked = e.control.value
        if picked:
            _hora_fin_sel["valor"] = picked
            texto_hora_fin.value = f"{picked.hour:02d}:{picked.minute:02d}"
            page.update()

    time_picker_ini = ft.TimePicker(on_change=_on_hora_ini_change)
    time_picker_fin = ft.TimePicker(on_change=_on_hora_fin_change)

    page.overlay.extend([date_picker, time_picker_ini, time_picker_fin])

    def _limpiar_overlay():
        for p in (date_picker, time_picker_ini, time_picker_fin):
            if p in page.overlay:
                page.overlay.remove(p)

    # Botones de selección (mismo estilo que el form de crear turno)
    def _mk_boton_selector(icon, texto_ref, on_click_fn, expand=False):
        c = ft.Container(
            content=ft.Row(
                [
                    ft.Icon(icon, size=18, color=COLOR_PRIMARIO),
                    ft.Container(width=6),
                    texto_ref,
                    ft.Icon(ft.Icons.ARROW_DROP_DOWN, size=18, color=COLOR_TEXTO_SEC),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.Padding(14, 12, 14, 12),
            border=ft.Border.all(1, COLOR_BORDE),
            border_radius=RADIO,
            bgcolor=COLOR_CARD,
            on_click=on_click_fn,
            ink=True,
        )
        if expand:
            c.expand = True
        return c

    boton_fecha = _mk_boton_selector(ft.Icons.CALENDAR_MONTH_ROUNDED, texto_fecha,
                                      lambda _: setattr(date_picker, 'open', True) or page.update())
    boton_hora_ini = _mk_boton_selector(ft.Icons.ACCESS_TIME_ROUNDED, texto_hora_ini,
                                         lambda _: setattr(time_picker_ini, 'open', True) or page.update(), expand=True)
    boton_hora_fin = _mk_boton_selector(ft.Icons.ACCESS_TIME_ROUNDED, texto_hora_fin,
                                         lambda _: setattr(time_picker_fin, 'open', True) or page.update(), expand=True)

    ubicacion_campo = ft.TextField(
        value=turno.get("ubicacion", ""), hint_text="Ubicación del turno",
        border_color=COLOR_BORDE, focused_border_color=COLOR_PRIMARIO,
        border_radius=RADIO, text_size=14, color=COLOR_TEXTO,
        cursor_color=COLOR_PRIMARIO, content_padding=ft.Padding(14, 14),
    )
    notas_campo = ft.TextField(
        value=turno.get("notas", ""), hint_text="Notas...",
        multiline=True, min_lines=3, max_lines=5,
        border_color=COLOR_BORDE, focused_border_color=COLOR_PRIMARIO,
        border_radius=RADIO, text_size=14, color=COLOR_TEXTO,
        cursor_color=COLOR_PRIMARIO, content_padding=ft.Padding(14, 14),
    )

    dd_estado = ft.Dropdown(
        label="Estado",
        options=[
            ft.dropdown.Option("Programado"),
            ft.dropdown.Option("En Progreso"),
            ft.dropdown.Option("Completado"),
        ],
        value=turno.get("estado", "Programado"),
        border_color=COLOR_BORDE, focused_border_color=COLOR_PRIMARIO,
        text_size=14, color=COLOR_TEXTO,
        content_padding=ft.Padding(12, 14), border_radius=RADIO, dense=True,
    )

    # Info de brigada (no se puede cambiar)
    brigada_info = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.SHIELD_OUTLINED, size=16, color=COLOR_PRIMARIO),
            ft.Text(f"Brigada: {turno.get('brigada', '')}", size=14, weight="w600", color=COLOR_PRIMARIO),
        ], spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        padding=ft.Padding(14, 16, 14, 16),
        bgcolor="#e8f5e9", border_radius=RADIO, border=ft.Border.all(1, COLOR_PRIMARIO),
    )

    fila_horas = ft.Row([
        ft.Column([ft.Text("Hora Inicio", size=14, weight="w500", color=COLOR_TEXTO),
                   ft.Container(height=8), boton_hora_ini], spacing=0, expand=True),
        ft.Container(width=16),
        ft.Column([ft.Text("Hora Fin", size=14, weight="w500", color=COLOR_TEXTO),
                   ft.Container(height=8), boton_hora_fin], spacing=0, expand=True),
    ], spacing=0)

    contenido = ft.Column([
        _campo_con_titulo("Brigada", brigada_info),
        _campo_con_titulo("Fecha", boton_fecha),
        fila_horas,
        ft.Container(height=16),
        _campo_con_titulo("Estado", dd_estado),
        _campo_con_titulo("Ubicación", ubicacion_campo),
        _campo_con_titulo("Notas", notas_campo, espaciado_abajo=0),
    ], spacing=0)

    def on_guardar(_):
        fi = _fecha_sel["valor"]
        hi = _hora_ini_sel["valor"]
        hf = _hora_fin_sel["valor"]

        if not fi or not hi or not hf:
            page.snack_bar = ft.SnackBar(ft.Text("Complete fecha y horas."), bgcolor="#ef4444")
            page.snack_bar.open = True
            page.update()
            return

        if hf <= hi:
            page.snack_bar = ft.SnackBar(ft.Text("La hora fin debe ser posterior a la hora inicio."), bgcolor="#ef4444")
            page.snack_bar.open = True
            page.update()
            return

        ok = crud_turno.actualizar_turno(
            turno_id=turno["id"],
            fecha=fi.strftime("%Y-%m-%d"),
            hora_inicio=f"{hi.hour:02d}:{hi.minute:02d}:00",
            hora_fin=f"{hf.hour:02d}:{hf.minute:02d}:00",
            ubicacion=(ubicacion_campo.value or "").strip(),
            notas=(notas_campo.value or "").strip(),
            estado=dd_estado.value,
            brigada_rol_id=brigada_rol_id,
        )

        _limpiar_overlay()
        _cerrar_dialogo(page)

        if ok:
            page.snack_bar = ft.SnackBar(ft.Text("Turno actualizado ✓"), bgcolor="#22c55e")
            if on_success:
                on_success()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Error al actualizar el turno."), bgcolor="#ef4444")
        page.snack_bar.open = True
        page.update()

    def _on_cancelar(e):
        _limpiar_overlay()
        _cerrar_dialogo(page)

    dialogo = ft.AlertDialog(
        modal=True,
        bgcolor=COLOR_CARD,
        title=ft.Row([
            ft.Text("Editar Turno", size=18, weight="w600", color=COLOR_TEXTO),
            ft.Container(expand=True),
            ft.IconButton(icon=ft.Icons.CLOSE, on_click=_on_cancelar),
        ]),
        content=ft.Container(
            content=ft.Column([contenido], scroll=ft.ScrollMode.AUTO, tight=True),
            width=520, bgcolor=COLOR_CARD,
        ),
        actions=[
            ft.TextButton(content=ft.Text("Cancelar", color=COLOR_TEXTO), on_click=_on_cancelar),
            ft.FilledButton("Guardar", style=ft.ButtonStyle(bgcolor=COLOR_PRIMARIO, color="white"), on_click=on_guardar),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    _abrir_dialogo(page, dialogo)


# ═══════════════════════════════════════════════════════════
#  Modal de confirmación para eliminar turno
# ═══════════════════════════════════════════════════════════

def _abrir_modal_eliminar_turno(page: ft.Page, turno: dict, usuario: dict, on_success=None):
    brigada_rol_id = usuario.get("Brigada_idBrigada") if not es_admin(usuario.get("rol", "")) else None
    brigada = turno.get("brigada", "")
    fecha_str = str(turno.get("fecha", ""))

    def on_confirmar(_):
        ok = crud_turno.eliminar_turno(turno["id"], brigada_rol_id=brigada_rol_id)
        _cerrar_dialogo(page)
        if ok:
            page.snack_bar = ft.SnackBar(ft.Text("Turno eliminado."), bgcolor="#22c55e")
            if on_success:
                on_success()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Error al eliminar."), bgcolor="#ef4444")
        page.snack_bar.open = True
        page.update()

    dialogo = ft.AlertDialog(
        modal=True, bgcolor=COLOR_CARD,
        title=ft.Text("Eliminar Turno", size=18, weight="w600", color=COLOR_TEXTO),
        content=ft.Container(
            content=ft.Column([
                ft.Text("Esta acción no se puede deshacer.", size=13, color=COLOR_TEXTO_SEC),
                ft.Container(height=12),
                ft.Text(f"¿Eliminar turno de «{brigada}» del {fecha_str}?", size=14, weight="w600", color=COLOR_TEXTO),
            ], spacing=0),
            width=420, bgcolor=COLOR_CARD,
        ),
        actions=[
            ft.TextButton(content=ft.Text("Cancelar", color=COLOR_TEXTO), on_click=lambda e: _cerrar_dialogo(e.page)),
            ft.FilledButton("Eliminar", style=ft.ButtonStyle(bgcolor="#ef4444", color="white"), on_click=on_confirmar),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    _abrir_dialogo(page, dialogo)


# ═══════════════════════════════════════════════════════════
#  Build principal
# ═══════════════════════════════════════════════════════════

def build(page: ft.Page, content_area=None, **kwargs) -> ft.Control:
    usuario = _obtener_usuario_actual(page)
    rol = usuario.get("rol", "")
    user_id = usuario.get("id")
    brigada_rol_id = usuario.get("Brigada_idBrigada") if not es_admin(rol) else None

    def on_nuevo_turno(_):
        from forms import abrir_form_turno
        abrir_form_turno(page)

    _tb = (page.data or {}).get("brigada_activa")

    def _refresh(_=None):
        if content_area:
            content_area.content = build(page, content_area)
            page.update()
        else:
            stats = crud_turno.get_turno_stats(_tb, brigada_rol_id)
            kpis_row.controls = _build_kpi_cards(stats)
            schedule_col.controls = _build_merged_schedule(_tb, brigada_rol_id, user_id, rol, _refresh, _on_editar, _on_eliminar, page)
            page.update()

    stats = crud_turno.get_turno_stats(_tb, brigada_rol_id)
    kpis_row = ft.Row(controls=_build_kpi_cards(stats), spacing=16)

    def _on_editar(turno):
        if turno.get("es_actividad"):
            # Omitiremos editar actividades desde aquí en esta fase puramente de lectura de calendarios
            page.snack_bar = ft.SnackBar(ft.Text("Edita la planificación desde la vista de Actividades."), bgcolor="#3b82f6")
            page.snack_bar.open = True
            page.update()
        else:
            _abrir_modal_editar_turno(page, turno, usuario, on_success=_refresh)

    def _on_eliminar(turno):
        if turno.get("es_actividad"):
            pass
        else:
            _abrir_modal_eliminar_turno(page, turno, usuario, on_success=_refresh)

    def _build_merged_schedule(_tb, b_id, uid, ro, _ref, _oe, _od, p):
        import database.crud_actividad as crud_act
        import util_json_plan
        from datetime import datetime
        turnos = crud_turno.listar_turnos(tipo_brigada=_tb, brigada_rol_id=b_id)
        actividades = crud_act.listar_actividades(tipo_brigada=_tb, brigada_rol_id=b_id)
        
        merged = list(turnos)
        for act in actividades:
            try:
                # Intenta convertir fechas de actividad
                f = act.get("fecha_inicio")
                if isinstance(f, str):
                    f = datetime.strptime(f, "%Y-%m-%d").date()
                
                # Extraer JSON de la actividad
                plan = util_json_plan.deserializar_plan(act.get("descripcion", ""))
                origen = plan.get("origen_actividad", "Actividad")
                efemeride = plan.get("efemeride", "")
                momento = plan.get("momento_escolar", "")

                label_origen = f"{origen}: {efemeride}" if efemeride else origen
                notas_act = f"{momento} - {plan.get('objetivo_plan', '')}"
                
                item_virtual = {
                    "id": act["id"],
                    "es_actividad": True,
                    "fecha": f,
                    "hora_inicio": "00:00:00", # Todo el día
                    "hora_fin": "23:59:59",
                    "brigada": act.get("brigada", "General"),
                    "estado": act.get("estado", "Planificada"),
                    "ubicacion": label_origen,
                    "notas": notas_act,
                    "color": "#8b5cf6", # Morado distintivo para actividades en el calendario
                    "profesor_id": act.get("creador_id")
                }
                merged.append(item_virtual)
            except Exception as e:
                print(f"Error procesando actividad para calendario: {e}")
                
        return _build_turno_section(merged, uid, ro, _ref, _oe, _od, p)

    schedule_col = ft.Column(
        controls=_build_merged_schedule(_tb, brigada_rol_id, user_id, rol, _refresh, _on_editar, _on_eliminar, page),
        spacing=0,
    )

    contenido = ft.Column(
        [
            titulo_pagina(
                "Calendario de Brigada",
                "Organiza y asigna los turnos de las brigadas",
                accion=boton_primario("Nuevo Turno", ft.Icons.ADD, on_click=on_nuevo_turno),
            ),
            ft.Container(height=28),
            kpis_row,
            ft.Container(height=28),
            ft.Container(
                content=ft.Row(
                    [
                        ft.Row(
                            [
                                ft.Icon(ft.Icons.VIEW_TIMELINE_ROUNDED, color=COLOR_PRIMARIO, size=22),
                                ft.Container(width=8),
                                ft.Text("Programación", size=18, weight="bold", color=COLOR_TEXTO),
                            ],
                            spacing=0,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        ft.Container(expand=True),
                        ft.Container(
                            content=ft.Row(
                                [
                                    ft.Icon(ft.Icons.REFRESH_ROUNDED, color=COLOR_PRIMARIO, size=16),
                                    ft.Container(width=4),
                                    ft.Text("Actualizar", size=12, weight="w500", color=COLOR_PRIMARIO),
                                ],
                                spacing=0,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            on_click=_refresh,
                            ink=True,
                            padding=ft.Padding(12, 8, 12, 8),
                            border_radius=8,
                            border=ft.Border.all(1, COLOR_PRIMARIO),
                        ),
                    ],
                ),
                padding=ft.Padding(0, 0, 0, 16),
            ),
            schedule_col,
            ft.Container(height=20),
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        spacing=0,
    )
    return ft.Container(content=contenido, padding=24, bgcolor=COLOR_FONDO_VERDE, expand=True)


# ═══════════════════════════════════════════════════════════
#  KPI Cards — estilo glassmorphism con gradientes
# ═══════════════════════════════════════════════════════════

_KPI_GRADIENTS = [
    ([COLOR_PRIMARIO, "#059669"], ft.Icons.CALENDAR_MONTH_ROUNDED),
    (["#f59e0b", "#d97706"], ft.Icons.PEOPLE_ROUNDED),
    (["#3b82f6", "#2563eb"], ft.Icons.SCHEDULE_ROUNDED),
]


def _build_kpi_cards(stats: dict) -> list:
    data = [
        (str(stats.get("total_turnos", 0)), "Turnos\nProgramados"),
        (str(stats.get("brigadistas_asignados", 0)), "Brigadistas\nAsignados"),
        (str(stats.get("dias_con_turnos", 0)), "Días con\nTurnos"),
    ]
    cards = []
    for i, (val, lbl) in enumerate(data):
        colors, ico = _KPI_GRADIENTS[i]
        cards.append(
            ft.Container(
                content=ft.Row(
                    [
                        ft.Container(
                            content=ft.Icon(ico, color="white", size=26),
                            width=52, height=52, border_radius=14,
                            gradient=ft.LinearGradient(
                                colors=colors,
                                begin=ft.Alignment(-1, -1), end=ft.Alignment(1, 1),
                            ),
                            alignment=ft.Alignment(0, 0),
                            shadow=ft.BoxShadow(
                                blur_radius=12, spread_radius=0,
                                color=ft.Colors.with_opacity(0.3, colors[0]),
                                offset=ft.Offset(0, 4),
                            ),
                        ),
                        ft.Container(width=16),
                        ft.Column(
                            [
                                ft.Text(val, size=28, weight="bold", color=COLOR_TEXTO),
                                ft.Text(lbl, size=11, color=COLOR_TEXTO_SEC, max_lines=2),
                            ],
                            spacing=2,
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                bgcolor=COLOR_CARD, padding=ft.Padding(20, 18, 20, 18),
                border_radius=16, border=ft.Border.all(1, COLOR_BORDE),
                shadow=get_sombra_card(), expand=True,
            )
        )
    return cards


# ═══════════════════════════════════════════════════════════
#  Turno Cards — timeline con indicador lateral + acciones
# ═══════════════════════════════════════════════════════════

_DIAS_ES = {0: "Lunes", 1: "Martes", 2: "Miércoles", 3: "Jueves", 4: "Viernes", 5: "Sábado", 6: "Domingo"}
_MESES_ES = {1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
             7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"}


def _format_time(t) -> str:
    if isinstance(t, timedelta):
        total = int(t.total_seconds())
        h, m = divmod(total, 3600)
        m = m // 60
        return f"{h:02d}:{m:02d}"
    try:
        return t.strftime("%H:%M")
    except Exception:
        return str(t)


def _fecha_badge(fecha) -> ft.Container:
    try:
        dia_num = str(fecha.day)
        dia_nombre = _DIAS_ES.get(fecha.weekday(), "")[:3].upper()
    except Exception:
        dia_num = "?"
        dia_nombre = ""

    hoy = date.today()
    is_today = (fecha == hoy) if isinstance(fecha, date) else False

    return ft.Container(
        content=ft.Column(
            [
                ft.Text(dia_num, size=22, weight="bold",
                        color="white" if is_today else COLOR_TEXTO,
                        text_align=ft.TextAlign.CENTER),
                ft.Text(dia_nombre, size=9, weight="w600",
                        color=ft.Colors.with_opacity(0.8, "white") if is_today else COLOR_TEXTO_SEC,
                        text_align=ft.TextAlign.CENTER),
            ],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        width=56, height=56, border_radius=16,
        alignment=ft.Alignment(0, 0),
        gradient=ft.LinearGradient(
            colors=[COLOR_PRIMARIO, COLOR_PRIMARIO_CLARO],
            begin=ft.Alignment(-1, -1), end=ft.Alignment(1, 1),
        ) if is_today else None,
        bgcolor=None if is_today else ft.Colors.with_opacity(0.06, COLOR_PRIMARIO),
        border=ft.Border.all(1.5, COLOR_PRIMARIO) if is_today else ft.Border.all(1, COLOR_BORDE),
    )


def _estado_chip(estado: str) -> ft.Container:
    colores = {
        "Programado": (ft.Colors.with_opacity(0.1, "#3b82f6"), "#3b82f6", ft.Icons.SCHEDULE),
        "En Progreso": (ft.Colors.with_opacity(0.1, "#f59e0b"), "#d97706", ft.Icons.PLAY_CIRCLE_FILLED),
        "Completado": (ft.Colors.with_opacity(0.1, "#10b981"), "#059669", ft.Icons.CHECK_CIRCLE),
    }
    bg, fg, ico = colores.get(estado, (ft.Colors.GREY_100, ft.Colors.GREY_700, ft.Icons.HELP_OUTLINE))
    return ft.Container(
        content=ft.Row(
            [
                ft.Icon(ico, size=13, color=fg),
                ft.Container(width=4),
                ft.Text(estado, size=11, weight="w600", color=fg),
            ],
            spacing=0, vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=bg, padding=ft.Padding(10, 5, 10, 5), border_radius=20,
    )


def _turno_item(t: dict, puede_editar: bool = False,
                on_edit=None, on_delete=None) -> ft.Container:
    """Un turno individual con barra lateral y acciones condicionales."""
    hi = _format_time(t["hora_inicio"])
    hf = _format_time(t["hora_fin"])
    color_brigada = t.get("color", "#2563eb")

    acciones = []
    if puede_editar:
        acciones.append(
            ft.IconButton(
                icon=ft.Icons.EDIT_OUTLINED, icon_color=COLOR_PRIMARIO, icon_size=18,
                tooltip="Editar turno", style=ft.ButtonStyle(padding=4),
                width=32, height=32,
                on_click=lambda e, turno=t: on_edit(turno) if on_edit else None,
            )
        )
        acciones.append(
            ft.IconButton(
                icon=ft.Icons.DELETE_OUTLINE_ROUNDED, icon_color="#ef4444", icon_size=18,
                tooltip="Eliminar turno", style=ft.ButtonStyle(padding=4),
                width=32, height=32,
                on_click=lambda e, turno=t: on_delete(turno) if on_delete else None,
            )
        )

    return ft.Container(
        content=ft.Row(
            [
                ft.Container(width=4, height=70, border_radius=4, bgcolor=color_brigada),
                ft.Container(width=14),
                ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text(t["brigada"], size=14, weight="w600", color=COLOR_TEXTO),
                                ft.Container(expand=True),
                                *acciones,
                                _estado_chip(t["estado"]),
                            ],
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        ft.Container(height=6),
                        ft.Row(
                            [
                                ft.Container(
                                    content=ft.Row(
                                        [
                                            ft.Icon(ft.Icons.ACCESS_TIME_ROUNDED, size=14, color=COLOR_PRIMARIO),
                                            ft.Container(width=4),
                                            ft.Text(f"{hi} – {hf}", size=12, weight="w500", color=COLOR_TEXTO),
                                        ],
                                        spacing=0, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                    bgcolor=ft.Colors.with_opacity(0.06, COLOR_PRIMARIO),
                                    padding=ft.Padding(8, 4, 8, 4), border_radius=6,
                                ),
                                ft.Container(width=8),
                                ft.Icon(ft.Icons.LOCATION_ON_OUTLINED, size=14, color=COLOR_TEXTO_SEC),
                                ft.Container(width=2),
                                ft.Text(
                                    t["ubicacion"] or "Sin ubicación", size=12, color=COLOR_TEXTO_SEC,
                                    max_lines=1, overflow=ft.TextOverflow.ELLIPSIS, expand=True,
                                ),
                            ],
                            spacing=0, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        ft.Container(height=4) if t.get("notas") else ft.Container(),
                        ft.Text(
                            t["notas"], size=11, color=COLOR_TEXTO_SEC, italic=True,
                            max_lines=1, overflow=ft.TextOverflow.ELLIPSIS,
                        ) if t.get("notas") else ft.Container(),
                    ],
                    spacing=0, expand=True,
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.START,
        ),
        padding=ft.Padding(14, 14, 14, 14),
        border_radius=12, bgcolor=COLOR_CARD,
        border=ft.Border.all(1, COLOR_BORDE), ink=True,
    )


def _build_turno_section(turnos: list, user_id=None, rol="",
                         on_refresh=None, on_edit=None, on_delete=None, page=None) -> list:
    """Construye la vista completa de turnos con timeline."""
    if not turnos:
        return [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Container(
                            content=ft.Icon(ft.Icons.CALENDAR_MONTH_OUTLINED, color=COLOR_PRIMARIO, size=40),
                            width=80, height=80, border_radius=20,
                            bgcolor=ft.Colors.with_opacity(0.08, COLOR_PRIMARIO),
                            alignment=ft.Alignment(0, 0),
                        ),
                        ft.Container(height=20),
                        ft.Text("No hay turnos programados", size=17, weight="bold", color=COLOR_TEXTO),
                        ft.Container(height=6),
                        ft.Text(
                            "Usa el botón «Nuevo Turno» para crear\nel primer turno de tu brigada.",
                            size=13, color=COLOR_TEXTO_SEC, text_align=ft.TextAlign.CENTER,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0,
                ),
                padding=ft.Padding(40, 48, 40, 48), border_radius=16,
                bgcolor=COLOR_CARD, border=ft.Border.all(1, COLOR_BORDE),
                shadow=get_sombra_card(), alignment=ft.Alignment(0, 0),
            )
        ]

    from collections import OrderedDict
    por_fecha = OrderedDict()
    for t in turnos:
        f = t["fecha"]
        if f not in por_fecha:
            por_fecha[f] = []
        por_fecha[f].append(t)

    sections = []
    for fecha, items in por_fecha.items():
        try:
            dia_semana = _DIAS_ES.get(fecha.weekday(), "")
            mes = _MESES_ES.get(fecha.month, "")
            fecha_str = f"{dia_semana}, {fecha.day} de {mes}"
            hoy = date.today()
            if fecha == hoy:
                fecha_str += "  •  Hoy"
            elif fecha == hoy + timedelta(days=1):
                fecha_str += "  •  Mañana"
        except Exception:
            fecha_str = str(fecha)

        turno_items = []
        for t in items:
            # Determinar si el usuario puede editar este turno
            # Un admin puede editar todos; un profesor solo los de su brigada
            puede = es_admin(rol) or (user_id is not None and t.get("profesor_id") == user_id)
            turno_items.append(_turno_item(t, puede_editar=puede, on_edit=on_edit, on_delete=on_delete))

        fecha_section = ft.Container(
            content=ft.Row(
                [
                    ft.Column(
                        [_fecha_badge(fecha)],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Container(width=16),
                    ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text(fecha_str, size=14, weight="w600", color=COLOR_TEXTO),
                                    ft.Container(expand=True),
                                    ft.Text(
                                        f"{len(items)} turno{'s' if len(items) > 1 else ''}",
                                        size=11, color=COLOR_TEXTO_SEC,
                                    ),
                                ],
                            ),
                            ft.Container(height=10),
                            *turno_items,
                        ],
                        spacing=8, expand=True,
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.START, spacing=0,
            ),
            padding=ft.Padding(20, 18, 20, 18), border_radius=16,
            bgcolor=COLOR_CARD, border=ft.Border.all(1, COLOR_BORDE),
            shadow=get_sombra_card(),
        )
        sections.append(fecha_section)
        sections.append(ft.Container(height=14))

    return sections
