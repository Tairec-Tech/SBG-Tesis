import flet as ft
from datetime import datetime
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
from components import titulo_pagina, boton_primario
from util_docx import generar_reporte_actividad_docx
from forms import modal_nuevo_reporte_actividad
from database.crud_usuario import es_admin, es_profesor


def _mostrar_snack(page: ft.Page, mensaje: str, color: str):
    page.snack_bar = ft.SnackBar(ft.Text(mensaje), bgcolor=color)
    page.snack_bar.open = True
    page.update()


def _puede_crear_reportes(rol: str) -> bool:
    return es_admin(rol) or es_profesor(rol)


def _obtener_usuario_actual(page: ft.Page) -> dict:
    import json

    usuario = {}
    try:
        if getattr(page, "data", None) and isinstance(page.data.get("usuario_actual"), dict):
            usuario = page.data.get("usuario_actual") or {}
        else:
            raw = page.client_storage.get("usuario_actual")
            if raw:
                usuario = json.loads(raw) if isinstance(raw, str) else (raw or {})
    except Exception:
        usuario = {}
    return usuario or {}


def build(page: ft.Page, **kwargs) -> ft.Control:
    from database import crud_reporte

    usuario = _obtener_usuario_actual(page)
    usuario_id = usuario.get("id") or usuario.get("idUsuario") or 0
    puede_crear_reporte = _puede_crear_reportes(usuario.get("rol", ""))
    brigada_rol_id = usuario.get("Brigada_idBrigada") if not es_admin(usuario.get("rol", "")) else None

    _tb = (page.data or {}).get("brigada_activa")
    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)

    async def descargar_doc(reporte_data):
        default_name = f"Reporte_Actividad_ACT-{reporte_data.get('id', 'X')}.docx"
        path = await file_picker.save_file(
            dialog_title="Guardar reporte de actividad",
            file_name=default_name,
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["docx"],
        )
        if not path:
            _mostrar_snack(page, "Exportación cancelada por el usuario.", ft.Colors.ORANGE)
            return
        save_path = generar_reporte_actividad_docx(reporte_data, save_path=path)
        if save_path:
            _mostrar_snack(page, f"Documento guardado en: {save_path}", ft.Colors.GREEN)
        else:
            _mostrar_snack(page, "Error al generar el documento DOCX.", ft.Colors.RED)

    reports_col = ft.Column(spacing=14)

    def _build_report_list():
        if not reportes:
            return [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(ft.Icons.EVENT_BUSY_ROUNDED, size=48, color=COLOR_BORDE),
                            ft.Text("No hay reportes de actividades registrados", size=16, color=COLOR_TEXTO_SEC),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=12,
                    ),
                    padding=40,
                    alignment=ft.Alignment(0, 0),
                )
            ]

        cards = []
        for r in reportes:
            fecha_dt = r.get("fecha_reporte")
            fecha_str = fecha_dt.strftime("%d/%m/%Y %H:%M") if isinstance(fecha_dt, datetime) else str(fecha_dt)

            resultado = str(r.get("resultado", ""))
            color_res = ft.Colors.BLUE
            if "éxito" in resultado.lower() or "completado" in resultado.lower():
                color_res = ft.Colors.GREEN
            elif "observaciones" in resultado.lower() or "parcial" in resultado.lower():
                color_res = ft.Colors.ORANGE
            elif "fallo" in resultado.lower() or "cancelad" in resultado.lower():
                color_res = ft.Colors.RED

            badge_resultado = ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.FLAG_CIRCLE_ROUNDED, color=color_res, size=16),
                        ft.Text(resultado, size=12, weight="bold", color=color_res),
                    ],
                    spacing=4,
                ),
                padding=ft.Padding(8, 4, 8, 4),
                bgcolor=ft.Colors.with_opacity(0.1, color_res),
                border_radius=8,
            )

            card = ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Row(
                                    [
                                        ft.Icon(ft.Icons.EVENT_NOTE_ROUNDED, color=COLOR_PRIMARIO, size=24),
                                        ft.Column(
                                            [
                                                ft.Text(r.get("actividad_titulo"), size=16, weight="bold", color=COLOR_TEXTO),
                                                ft.Text(f"Reportado por: {r.get('usuario_nombre')} — {fecha_str}", size=12, color=COLOR_TEXTO_SEC),
                                            ],
                                            spacing=2,
                                        ),
                                    ],
                                    spacing=12,
                                    expand=True,
                                ),
                                ft.Row(
                                    [
                                        badge_resultado,
                                        ft.IconButton(
                                            icon=ft.Icons.DOWNLOAD_ROUNDED,
                                            icon_color=COLOR_PRIMARIO,
                                            tooltip="Guardar en DOCX",
                                            on_click=lambda e, r_data=r: page.run_task(descargar_doc, r_data),
                                        ),
                                    ]
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.START,
                        ),
                        ft.Divider(height=1, color=COLOR_BORDE),
                        *([
                            ft.Row(
                                [
                                    ft.Icon(ft.Icons.GROUP_ROUNDED, size=14, color=COLOR_TEXTO_SEC),
                                    ft.Text(f"Participantes: {r.get('participantes')}", size=12, color=COLOR_TEXTO_SEC),
                                ],
                                spacing=6,
                            ),
                        ] if r.get("participantes") else []),
                        ft.Text("Observaciones:", size=13, weight="w600", color=COLOR_TEXTO),
                        ft.Text(r.get("resumen", ""), size=14, color=COLOR_TEXTO_SEC),
                    ],
                    spacing=12,
                ),
                padding=20,
                bgcolor=COLOR_CARD,
                border_radius=RADIO,
                border=ft.Border.all(1, COLOR_BORDE),
                shadow=get_sombra_card(),
            )
            cards.append(card)
        return cards

    def cargar_datos():
        nonlocal reportes
        reportes = crud_reporte.listar_reportes_actividad(_tb, brigada_rol_id)
        reports_col.controls = _build_report_list()
        page.update()

    reportes = crud_reporte.listar_reportes_actividad(_tb, brigada_rol_id)
    reports_col.controls = _build_report_list()

    def _abrir_modal_nuevo(e):
        if not puede_crear_reporte:
            _mostrar_snack(page, "No tiene permisos para crear reportes de actividad.", ft.Colors.RED)
            return
        modal_nuevo_reporte_actividad(page=page, id_usuario_actual=usuario_id, on_success_callback=cargar_datos)

    acciones = []
    if puede_crear:
        acciones.append(boton_primario("Nuevo Reporte", ft.Icons.ADD_ROUNDED, on_click=_abrir_modal_nuevo))

    header_row = ft.Row(
        [
            titulo_pagina(
                "Reportes de Actividades",
                "Consulta los resúmenes y resultados de las jornadas de las brigadas",
                icono="event_note",
            ),
            ft.Container(expand=True),
            *acciones,
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    contenido = ft.Column(
        [
            header_row,
            ft.Container(height=24),
            reports_col,
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        spacing=0,
    )

    return ft.Container(content=contenido, padding=24, bgcolor=COLOR_FONDO_VERDE, expand=True)
