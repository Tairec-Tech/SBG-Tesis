"""Pantalla — Importar / Exportar Base de Datos (Solo Directivo/Coordinador)."""

import flet as ft
from theme import (
    COLOR_TEXTO,
    COLOR_TEXTO_SEC,
    COLOR_FONDO_VERDE,
    COLOR_PRIMARIO,
    COLOR_PRIMARIO_CLARO,
)
from components import titulo_pagina, card_principal, boton_primario


def build(page: ft.Page, **kwargs) -> ft.Control:
    on_back = kwargs.get("on_back", None)

    back_btn = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.ARROW_BACK, color=COLOR_PRIMARIO, size=20),
                ft.Container(width=4),
                ft.Text("Volver a Utilidades", size=14, color=COLOR_PRIMARIO),
            ],
            spacing=0,
        ),
        on_click=lambda _: on_back() if on_back else None,
        padding=ft.Padding.only(bottom=16),
    ) if on_back else ft.Container()

    def _exportar_bd(e):
        try:
            import subprocess, os, datetime
            fecha = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            archivo = f"backup_brigadas_{fecha}.sql"
            # Intenta ejecutar mysqldump 
            resultado = subprocess.run(
                ["mysqldump", "-u", "root", "db_brigadas_maracaibo"],
                capture_output=True, text=True, timeout=30,
            )
            if resultado.returncode == 0:
                ruta_desktop = os.path.join(os.path.expanduser("~"), "Desktop", archivo)
                with open(ruta_desktop, "w", encoding="utf-8") as f:
                    f.write(resultado.stdout)
                status_text.value = f"✅ Exportado exitosamente: {ruta_desktop}"
                status_text.color = "#10b981"
            else:
                status_text.value = f"❌ Error al exportar: {resultado.stderr[:200]}"
                status_text.color = "#ef4444"
        except FileNotFoundError:
            status_text.value = "❌ mysqldump no encontrado. Asegúrate de que MySQL esté en el PATH del sistema."
            status_text.color = "#ef4444"
        except Exception as ex:
            status_text.value = f"❌ Error: {str(ex)[:200]}"
            status_text.color = "#ef4444"
        page.update()

    def _importar_bd(e: ft.FilePickerResultEvent):
        if not e.files:
            return
        archivo = e.files[0].path
        try:
            import subprocess
            resultado = subprocess.run(
                ["mysql", "-u", "root", "db_brigadas_maracaibo"],
                input=open(archivo, "r", encoding="utf-8").read(),
                capture_output=True, text=True, timeout=60,
            )
            if resultado.returncode == 0:
                status_text.value = f"✅ Base de datos restaurada desde: {archivo}"
                status_text.color = "#10b981"
            else:
                status_text.value = f"❌ Error al restaurar: {resultado.stderr[:200]}"
                status_text.color = "#ef4444"
        except Exception as ex:
            status_text.value = f"❌ Error: {str(ex)[:200]}"
            status_text.color = "#ef4444"
        page.update()

    file_picker = ft.FilePicker(on_result=_importar_bd)
    page.overlay.append(file_picker)

    status_text = ft.Text("", size=13, color=COLOR_TEXTO_SEC)

    contenido = ft.Column(
        [
            back_btn,
            titulo_pagina("Importar / Exportar BD", "Gestión de respaldos de la base de datos"),
            ft.Container(height=24),
            card_principal(
                ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Icon(ft.Icons.CLOUD_DOWNLOAD_ROUNDED, color="#10b981", size=36),
                                ft.Container(width=16),
                                ft.Column(
                                    [
                                        ft.Text("Exportar Base de Datos", size=18, weight="bold", color=COLOR_TEXTO),
                                        ft.Container(height=4),
                                        ft.Text("Genera un archivo .sql con todos los datos actuales del sistema y lo guarda en el Escritorio.", 
                                                size=13, color=COLOR_TEXTO_SEC),
                                    ],
                                    spacing=0,
                                    expand=True,
                                ),
                            ],
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        ft.Container(height=16),
                        boton_primario("Exportar Ahora", ft.Icons.DOWNLOAD_ROUNDED, on_click=_exportar_bd),
                    ],
                    spacing=0,
                ),
            ),
            ft.Container(height=20),
            card_principal(
                ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Icon(ft.Icons.CLOUD_UPLOAD_ROUNDED, color="#3b82f6", size=36),
                                ft.Container(width=16),
                                ft.Column(
                                    [
                                        ft.Text("Importar / Restaurar Base de Datos", size=18, weight="bold", color=COLOR_TEXTO),
                                        ft.Container(height=4),
                                        ft.Text("Selecciona un archivo .sql previamente exportado para restaurar los datos del sistema.", 
                                                size=13, color=COLOR_TEXTO_SEC),
                                    ],
                                    spacing=0,
                                    expand=True,
                                ),
                            ],
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        ft.Container(height=16),
                        boton_primario("Seleccionar Archivo .sql", ft.Icons.UPLOAD_FILE_ROUNDED, 
                                      on_click=lambda _: file_picker.pick_files(
                                          allowed_extensions=["sql"],
                                          dialog_title="Seleccionar respaldo de BD",
                                      )),
                    ],
                    spacing=0,
                ),
            ),
            ft.Container(height=20),
            card_principal(
                ft.Column(
                    [
                        ft.Icon(ft.Icons.INFO_OUTLINE_ROUNDED, color=COLOR_PRIMARIO, size=24),
                        ft.Container(height=8),
                        ft.Text("Estado de la operación:", size=14, weight="w600", color=COLOR_TEXTO),
                        ft.Container(height=8),
                        status_text,
                    ],
                    spacing=0,
                ),
            ),
            ft.Container(height=24),
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
