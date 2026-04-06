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
from util_docx import generar_reporte_impacto_docx
from forms import modal_nuevo_reporte_impacto
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

    usuario_actual = _obtener_usuario_actual(page)
    usuario_id = usuario_actual.get("id") or usuario_actual.get("idUsuario") or 0
    rol_actual = usuario_actual.get("rol", "")

    puede_crear = _puede_crear_reportes(rol_actual)
    _tb = (page.data or {}).get("brigada_activa")
    file_picker = ft.FilePicker()

    def cargar_datos():
        nonlocal reportes
        reportes = crud_reporte.listar_reportes_impacto(_tb)
        reports_col.controls = _build_report_list()
        page.update()

    reportes = crud_reporte.listar_reportes_impacto(_tb)

    async def descargar_doc(reporte_data):
        default_name = f"Reporte_Impacto_IMP-{reporte_data.get('id', 'X')}.docx"
        path = await file_picker.save_file(
            dialog_title="Guardar análisis de impacto",
            file_name=default_name,
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["docx"],
        )
        if not path:
            _mostrar_snack(page, "Exportación cancelada por el usuario.", ft.Colors.ORANGE)
            return
        save_path = generar_reporte_impacto_docx(reporte_data, save_path=path)
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
                            ft.Icon(ft.Icons.PUBLIC_OFF_ROUNDED, size=48, color=COLOR_BORDE),
                            ft.Text("No hay reportes de impacto registrados", size=16, color=COLOR_TEXTO_SEC),
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
            fecha_dt = r.get("fecha_generacion")
            fecha_str = fecha_dt.strftime("%d/%m/%Y %H:%M") if isinstance(fecha_dt, datetime) else str(fecha_dt)

            # Título: usar brigada + área si existen, sino actividad (legacy)
            titulo_card = ""
            if r.get("brigada") and r.get("area_evaluada"):
                titulo_card = f"{r['brigada']} — {r['area_evaluada']}"
            elif r.get("actividad_titulo"):
                titulo_card = f"Impacto: {r['actividad_titulo']}"
            else:
                titulo_card = "Reporte de Impacto"

            # Indicador badge
            indicador_info = []
            if r.get("indicador"):
                ind_txt = r["indicador"]
                if r.get("valor"):
                    ind_txt += f": {r['valor']}"
                if r.get("unidad"):
                    ind_txt += f" {r['unidad']}"
                indicador_info.append(
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Icon(ft.Icons.INSIGHTS_ROUNDED, color=COLOR_PRIMARIO, size=14),
                                ft.Text(ind_txt, size=12, weight="w600", color=COLOR_PRIMARIO),
                            ],
                            spacing=4,
                        ),
                        padding=ft.Padding(8, 4, 8, 4),
                        bgcolor=ft.Colors.with_opacity(0.1, COLOR_PRIMARIO),
                        border_radius=8,
                    )
                )

            card = ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Row(
                                    [
                                        ft.Container(
                                            content=ft.Icon(ft.Icons.PUBLIC_ROUNDED, color=COLOR_PRIMARIO, size=24),
                                            padding=10,
                                            bgcolor=ft.Colors.with_opacity(0.1, COLOR_PRIMARIO),
                                            border_radius=8,
                                        ),
                                        ft.Column(
                                            [
                                                ft.Text(titulo_card, size=16, weight="bold", color=COLOR_TEXTO),
                                                ft.Text(f"Por: {r.get('usuario_nombre')} — {fecha_str}", size=12, color=COLOR_TEXTO_SEC),
                                            ],
                                            spacing=2,
                                        ),
                                    ],
                                    spacing=12,
                                    expand=True,
                                ),
                                ft.Row(
                                    [
                                        *indicador_info,
                                        ft.IconButton(
                                            icon=ft.Icons.DOWNLOAD_ROUNDED,
                                            icon_color=COLOR_PRIMARIO,
                                            tooltip="Guardar en DOCX",
                                            on_click=lambda e, r_data=r: page.run_task(descargar_doc, r_data),
                                        ),
                                    ],
                                    spacing=4,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.START,
                        ),
                        ft.Divider(height=1, color=COLOR_BORDE),
                        ft.Text("Descripción del Impacto:", size=13, weight="w600", color=COLOR_TEXTO),
                        ft.Text(r.get("contenido", "Sin descripción") or "Sin descripción", size=14, color=COLOR_TEXTO_SEC, italic=True),
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

    reports_col.controls = _build_report_list()

    def _abrir_modal_nuevo(e):
        if not puede_crear:
            _mostrar_snack(page, "No tiene permisos para crear análisis de impacto.", ft.Colors.RED)
            return
        modal_nuevo_reporte_impacto(page=page, id_usuario_actual=usuario_id, on_success_callback=cargar_datos)

    acciones = []
    if puede_crear:
        acciones.append(boton_primario("Nuevo Análisis", ft.Icons.ADD_CHART_ROUNDED, on_click=_abrir_modal_nuevo))

    header_row = ft.Row(
        [
            titulo_pagina(
                "Reportes de Impacto",
                "Evaluación y seguimiento del impacto de las brigadas",
                icono="public",
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
