"""Reportes de Incidentes — diseño premium con cards, estados interactivos y exportación a DOCX."""

import flet as ft
from datetime import datetime
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
import database.crud_reporte as crud_reporte
from database.crud_usuario import es_profesor


def build(page: ft.Page, **kwargs) -> ft.Control:
    
    # Intentar obtener info del usuario actual
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
        
    puede_crear_reporte = es_profesor(usuario.get("rol", ""))

    def on_nuevo_report(_):
        from forms import abrir_form_nuevo_reporte
        abrir_form_nuevo_reporte(page)

    def _refresh(_=None):
        stats = crud_reporte.get_reporte_stats()
        reportes = crud_reporte.listar_reportes()
        kpis_row.controls = _build_kpi_cards(stats)
        reports_col.controls = _build_report_list(page, reportes)
        page.update()

    # Carga inicial de datos
    stats = crud_reporte.get_reporte_stats()
    kpis_row = ft.Row(controls=_build_kpi_cards(stats), spacing=16)

    reportes = crud_reporte.listar_reportes()
    reports_col = ft.Column(controls=_build_report_list(page, reportes), spacing=14)

    contenido = ft.Column(
        [
            titulo_pagina(
                "Reportes de Incidentes",
                "Registra, haz seguimiento y exporta los eventos de las brigadas",
                accion=boton_primario("Nuevo Reporte", ft.Icons.ADD, on_click=on_nuevo_report) if puede_crear_reporte else None,
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
                                ft.Icon(ft.Icons.SUBJECT_ROUNDED, color=COLOR_PRIMARIO, size=24),
                                ft.Container(width=8),
                                ft.Text("Registro Histórico", size=18, weight="bold", color=COLOR_TEXTO),
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
            reports_col,
            ft.Container(height=40),
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        spacing=0,
    )
    
    # Añadimos key al contenedor principal para poder encontrarlo y recargarlo desde los forms
    container = ft.Container(
        content=contenido,
        padding=24,
        bgcolor=COLOR_FONDO_VERDE,
        expand=True,
        data="screen_reports"
    )
    return container


# ═══════════════════════════════════════════════════════════
#  KPI Cards — estilo glassmorphism con gradientes
# ═══════════════════════════════════════════════════════════

_KPI_GRADIENTS = [
    (["#3b82f6", "#2563eb"], ft.Icons.FOLDER_OPEN_ROUNDED),       # Total
    (["#f59e0b", "#d97706"], ft.Icons.SCHEDULE_ROUNDED),           # En Proceso
    (["#10b981", "#059669"], ft.Icons.CHECK_CIRCLE_OUTLINED),      # Resueltos
]

def _build_kpi_cards(stats: dict) -> list:
    data = [
        (str(stats.get("total", 0)), "Total de\nReportes", _KPI_GRADIENTS[0]),
        (str(stats.get("en_proceso", 0)), "Casos\nEn Proceso", _KPI_GRADIENTS[1]),
        (str(stats.get("resueltos", 0)), "Incidentes\nResueltos", _KPI_GRADIENTS[2]),
    ]
    cards = []
    for val, lbl, (colors, ico) in data:
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
#  Report Cards — diseño interactivo y exportación
# ═══════════════════════════════════════════════════════════

def _estado_chip(estado: str) -> ft.Container:
    colores = {
        "En Proceso": (ft.Colors.with_opacity(0.1, "#f59e0b"), "#d97706", ft.Icons.SCHEDULE),
        "Resuelto": (ft.Colors.with_opacity(0.1, "#10b981"), "#059669", ft.Icons.CHECK_CIRCLE),
    }
    bg, fg, ico = colores.get(estado, (ft.Colors.GREY_100, ft.Colors.GREY_700, ft.Icons.HELP_OUTLINE))
    return ft.Container(
        content=ft.Row(
            [
                ft.Icon(ico, size=11, color=fg),
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


def _prioridad_indicator(prioridad: str) -> ft.Container:
    """Retorna un puntito de color según la prioridad."""
    if "Alta" in prioridad:
        color = ft.Colors.RED_500
    elif "Media" in prioridad:
        color = ft.Colors.ORANGE_500
    else:
        color = ft.Colors.GREEN_500
        
    return ft.Container(
        width=8,
        height=8,
        border_radius=4,
        bgcolor=color,
        tooltip=prioridad
    )


def _build_report_list(page: ft.Page, reportes: list) -> list:
    if not reportes:
        return [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Container(
                            content=ft.Icon(ft.Icons.GPP_GOOD_ROUNDED, color=COLOR_PRIMARIO, size=40),
                            width=80,
                            height=80,
                            border_radius=20,
                            bgcolor=ft.Colors.with_opacity(0.08, COLOR_PRIMARIO),
                            alignment=ft.Alignment(0, 0),
                        ),
                        ft.Container(height=20),
                        ft.Text("Todo está en orden", size=17, weight="bold", color=COLOR_TEXTO),
                        ft.Container(height=6),
                        ft.Text(
                            "No hay reportes de incidentes registrados en el sistema.",
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

    cards = []
    
    def on_exportar(e, req):
        from util_docx import generar_reporte_docx
        ruta = generar_reporte_docx(req)
        if ruta:
            page.snack_bar = ft.SnackBar(
                ft.Text(f"DOCX generado en Descargas: {ruta}", color="white"), 
                bgcolor=COLOR_PRIMARIO,
                duration=4000
            )
        else:
            page.snack_bar = ft.SnackBar(
                ft.Text("Error generando DOCX. Verifique consola.", color="white"), 
                bgcolor="red"
            )
        page.snack_bar.open = True
        page.update()
    
    def on_cambiar_estado(e, req, es_resolver):
        nuevo_estado = "Resuelto" if es_resolver else "En Proceso"
        exito = crud_reporte.actualizar_estado(req["id"], nuevo_estado)
        
        if exito:
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Estado actualizado a {nuevo_estado}", color="white"), 
                bgcolor=COLOR_PRIMARIO
            )
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Error actualizando", color="white"), bgcolor="red")
            
        page.snack_bar.open = True
        # Pequeño truco para forzar actualización de la pantalla (ya que no tenemos Redux o Provider global aquí)
        # La solución limpia es un simple mensaje de éxito y pedir que refresquen o recargar todos
        page.update()

    for r in reportes:
        fecha_str = r["fecha"].strftime("%d %b %Y, %H:%M") if hasattr(r["fecha"], "strftime") else str(r["fecha"])
        es_resuelto = r["estado"] == "Resuelto"
        
        card = ft.Container(
            content=ft.Row(
                [
                    # Barra de color brigada
                    ft.Container(
                        width=4,
                        height=110,
                        border_radius=4,
                        bgcolor=r["color_brigada"],
                    ),
                    ft.Container(width=16),
                    # Contenido principal
                    ft.Column(
                        [
                            ft.Row(
                                [
                                    _prioridad_indicator(r["prioridad"]),
                                    ft.Container(width=6),
                                    ft.Text(f"#{r['id']} — {r['brigada']}", size=12, weight="w600", color=COLOR_PRIMARIO),
                                    ft.Container(expand=True),
                                    ft.Text(fecha_str, size=11, color=COLOR_TEXTO_SEC),
                                ],
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=0,
                            ),
                            ft.Container(height=4),
                            ft.Text(r["titulo"], size=16, weight="bold", color=COLOR_TEXTO),
                            ft.Container(height=4),
                            ft.Text(
                                r["descripcion"], 
                                size=13, 
                                color=COLOR_TEXTO_SEC, 
                                max_lines=2, 
                                overflow=ft.TextOverflow.ELLIPSIS
                            ),
                            ft.Container(height=10),
                            ft.Row(
                                [
                                    ft.Icon(ft.Icons.LOCATION_ON_OUTLINED, size=13, color=COLOR_TEXTO_SEC),
                                    ft.Container(width=4),
                                    ft.Text(r["ubicacion"], size=12, color=COLOR_TEXTO_SEC),
                                    ft.Container(width=16),
                                    _estado_chip(r["estado"]),
                                ],
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=0,
                            ),
                        ],
                        expand=True,
                        spacing=0,
                    ),
                    ft.Container(width=16),
                    # Botones de Acción
                    ft.Column(
                        [
                            ft.IconButton(
                                icon=ft.Icons.DOWNLOAD_ROUNDED,
                                icon_color=COLOR_PRIMARIO,
                                on_click=lambda e, rep=r: on_exportar(e, rep),
                            ),
                            ft.IconButton(
                                icon=ft.Icons.CHECK_CIRCLE_OUTLINED if not es_resuelto else ft.Icons.RESTORE_ROUNDED,
                                icon_color=ft.Colors.GREEN if not es_resuelto else ft.Colors.ORANGE,
                                tooltip=("Marcar como Resuelto" if not es_resuelto else "Reabrir Reporte"),
                                on_click=lambda e, rep=r, res=not es_resuelto: on_cambiar_estado(e, rep, res),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=0,
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),
            padding=ft.Padding(16, 20, 16, 20),
            border_radius=14,
            bgcolor=COLOR_CARD,
            border=ft.Border.all(1, COLOR_BORDE),
            shadow=get_sombra_card(),
        )
        cards.append(card)

    return cards
