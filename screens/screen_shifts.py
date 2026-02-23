"""Turnos y Horarios — diseño premium con timeline y cards enriquecidas."""

import flet as ft
from datetime import timedelta, date
from theme import (
    COLOR_PRIMARIO,
    COLOR_PRIMARIO_CLARO,
    COLOR_TEXTO,
    COLOR_TEXTO_SEC,
    COLOR_CARD,
    COLOR_BORDE,
    COLOR_FONDO_VERDE,
    get_sombra_card,
)
from components import titulo_pagina, boton_primario
import database.crud_turno as crud_turno


def build(page: ft.Page, **kwargs) -> ft.Control:

    def on_nuevo_turno(_):
        from forms import abrir_form_turno
        abrir_form_turno(page)

    def _refresh(_=None):
        stats = crud_turno.get_turno_stats()
        turnos = crud_turno.listar_turnos()
        kpis_row.controls = _build_kpi_cards(stats)
        schedule_col.controls = _build_turno_section(turnos)
        page.update()

    stats = crud_turno.get_turno_stats()
    kpis_row = ft.Row(controls=_build_kpi_cards(stats), spacing=16)

    turnos = crud_turno.listar_turnos()
    schedule_col = ft.Column(controls=_build_turno_section(turnos), spacing=0)

    contenido = ft.Column(
        [
            titulo_pagina(
                "Turnos y Horarios",
                "Organiza y asigna los turnos de las brigadas",
                accion=boton_primario("Nuevo Turno", ft.Icons.ADD, on_click=on_nuevo_turno),
            ),
            ft.Container(height=28),
            kpis_row,
            ft.Container(height=28),
            # Encabezado de sección
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
                            width=52,
                            height=52,
                            border_radius=14,
                            gradient=ft.LinearGradient(
                                colors=colors,
                                begin=ft.Alignment(-1, -1),
                                end=ft.Alignment(1, 1),
                            ),
                            alignment=ft.Alignment(0, 0),
                            shadow=ft.BoxShadow(
                                blur_radius=12,
                                spread_radius=0,
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
                bgcolor=COLOR_CARD,
                padding=ft.Padding(20, 18, 20, 18),
                border_radius=16,
                border=ft.Border.all(1, COLOR_BORDE),
                shadow=get_sombra_card(),
                expand=True,
            )
        )
    return cards


# ═══════════════════════════════════════════════════════════
#  Turno Cards — timeline con indicador lateral
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
    """Badge circular con el día del mes y nombre del día."""
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
                ft.Text(dia_num, size=22, weight="bold", color="white" if is_today else COLOR_TEXTO,
                        text_align=ft.TextAlign.CENTER),
                ft.Text(dia_nombre, size=9, weight="w600",
                        color=ft.Colors.with_opacity(0.8, "white") if is_today else COLOR_TEXTO_SEC,
                        text_align=ft.TextAlign.CENTER),
            ],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        width=56,
        height=56,
        border_radius=16,
        alignment=ft.Alignment(0, 0),
        gradient=ft.LinearGradient(
            colors=[COLOR_PRIMARIO, COLOR_PRIMARIO_CLARO],
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
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
            spacing=0,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=bg,
        padding=ft.Padding(10, 5, 10, 5),
        border_radius=20,
    )


def _turno_item(t: dict) -> ft.Container:
    """Un turno individual con barra lateral de color de brigada."""
    hi = _format_time(t["hora_inicio"])
    hf = _format_time(t["hora_fin"])
    color_brigada = t.get("color", "#2563eb")

    return ft.Container(
        content=ft.Row(
            [
                # Barra lateral de color
                ft.Container(
                    width=4,
                    height=70,
                    border_radius=4,
                    bgcolor=color_brigada,
                ),
                ft.Container(width=14),
                # Contenido principal
                ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text(t["brigada"], size=14, weight="w600", color=COLOR_TEXTO),
                                ft.Container(expand=True),
                                _estado_chip(t["estado"]),
                            ],
                        ),
                        ft.Container(height=6),
                        ft.Row(
                            [
                                # Hora
                                ft.Container(
                                    content=ft.Row(
                                        [
                                            ft.Icon(ft.Icons.ACCESS_TIME_ROUNDED, size=14, color=COLOR_PRIMARIO),
                                            ft.Container(width=4),
                                            ft.Text(f"{hi} – {hf}", size=12, weight="w500", color=COLOR_TEXTO),
                                        ],
                                        spacing=0,
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                    bgcolor=ft.Colors.with_opacity(0.06, COLOR_PRIMARIO),
                                    padding=ft.Padding(8, 4, 8, 4),
                                    border_radius=6,
                                ),
                                ft.Container(width=8),
                                # Ubicación
                                ft.Icon(ft.Icons.LOCATION_ON_OUTLINED, size=14, color=COLOR_TEXTO_SEC),
                                ft.Container(width=2),
                                ft.Text(
                                    t["ubicacion"] or "Sin ubicación",
                                    size=12,
                                    color=COLOR_TEXTO_SEC,
                                    max_lines=1,
                                    overflow=ft.TextOverflow.ELLIPSIS,
                                    expand=True,
                                ),
                            ],
                            spacing=0,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        # Notas (si hay)
                        ft.Container(height=4) if t.get("notas") else ft.Container(),
                        ft.Text(
                            t["notas"], size=11, color=COLOR_TEXTO_SEC, italic=True, max_lines=1,
                            overflow=ft.TextOverflow.ELLIPSIS,
                        ) if t.get("notas") else ft.Container(),
                    ],
                    spacing=0,
                    expand=True,
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.START,
        ),
        padding=ft.Padding(14, 14, 14, 14),
        border_radius=12,
        bgcolor=COLOR_CARD,
        border=ft.Border.all(1, COLOR_BORDE),
        ink=True,
    )


def _build_turno_section(turnos: list) -> list:
    """Construye la vista completa de turnos con timeline."""
    if not turnos:
        return [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Container(
                            content=ft.Icon(ft.Icons.CALENDAR_MONTH_OUTLINED, color=COLOR_PRIMARIO, size=40),
                            width=80,
                            height=80,
                            border_radius=20,
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
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=0,
                ),
                padding=ft.Padding(40, 48, 40, 48),
                border_radius=16,
                bgcolor=COLOR_CARD,
                border=ft.Border.all(1, COLOR_BORDE),
                shadow=get_sombra_card(),
                alignment=ft.Alignment(0, 0),
            )
        ]

    # Agrupar por fecha
    from collections import OrderedDict
    por_fecha = OrderedDict()
    for t in turnos:
        f = t["fecha"]
        if f not in por_fecha:
            por_fecha[f] = []
        por_fecha[f].append(t)

    sections = []
    for fecha, items in por_fecha.items():
        # Encabezado de fecha
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

        turno_items = [_turno_item(t) for t in items]

        # Card de fecha con badge + turnos
        fecha_section = ft.Container(
            content=ft.Row(
                [
                    # Badge de día
                    ft.Column(
                        [_fecha_badge(fecha)],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Container(width=16),
                    # Columna de turnos
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
                        spacing=8,
                        expand=True,
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.START,
                spacing=0,
            ),
            padding=ft.Padding(20, 18, 20, 18),
            border_radius=16,
            bgcolor=COLOR_CARD,
            border=ft.Border.all(1, COLOR_BORDE),
            shadow=get_sombra_card(),
        )
        sections.append(fecha_section)
        sections.append(ft.Container(height=14))

    return sections
