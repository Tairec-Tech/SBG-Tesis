"""Pantalla — Importar / Exportar Base de Datos (Solo Directivo/Coordinador)."""

import os
import shutil
from pathlib import Path

import flet as ft

from theme import (
    COLOR_TEXTO,
    COLOR_TEXTO_SEC,
    COLOR_FONDO_VERDE,
    COLOR_PRIMARIO,
)
from components import titulo_pagina, card_principal, boton_primario


DEFAULT_DB_NAME = "db_brigadas_maracaibo"
DEFAULT_DB_USER = "root"
DEFAULT_XAMPP_MYSQL_BIN = Path(r"C:\xampp\mysql\bin")


def build(page: ft.Page, **kwargs) -> ft.Control:
    on_back = kwargs.get("on_back", None)

    back_btn = (
        ft.Container(
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
        )
        if on_back
        else ft.Container()
    )

    status_text = ft.Text("", size=13, color=COLOR_TEXTO_SEC)
    file_picker = ft.FilePicker()

    def _set_status(message: str, color: str):
        status_text.value = message
        status_text.color = color
        page.update()

    def _resolve_executable(name: str) -> str | None:
        """Busca el ejecutable en PATH y luego en XAMPP por defecto."""
        found = shutil.which(name)
        if found:
            return found

        xampp_candidate = DEFAULT_XAMPP_MYSQL_BIN / f"{name}.exe"
        if xampp_candidate.exists():
            return str(xampp_candidate)

        return None

    def _desktop_dir() -> Path:
        desktop = Path.home() / "Desktop"
        return desktop if desktop.exists() else Path.home()

    async def _exportar_bd_async():
        try:
            import datetime
            import subprocess

            mysqldump_path = _resolve_executable("mysqldump")
            if not mysqldump_path:
                _set_status(
                    "❌ mysqldump no encontrado. Verifica PATH o la instalación de XAMPP.",
                    "#ef4444",
                )
                return

            fecha = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            archivo = f"backup_brigadas_{fecha}.sql"
            ruta_destino = _desktop_dir() / archivo

            cmd = [
                mysqldump_path,
                "-u",
                DEFAULT_DB_USER,
                f"--result-file={ruta_destino}",
                DEFAULT_DB_NAME,
            ]

            resultado = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
            )

            if resultado.returncode == 0 and ruta_destino.exists():
                _set_status(f"✅ Exportado exitosamente: {ruta_destino}", "#10b981")
                return

            stderr = (resultado.stderr or "").strip()
            stdout = (resultado.stdout or "").strip()
            detalle = stderr or stdout or "No se pudo generar el archivo de respaldo."
            _set_status(f"❌ Error al exportar: {detalle[:250]}", "#ef4444")

        except Exception as ex:
            _set_status(f"❌ Error: {str(ex)[:250]}", "#ef4444")

    async def _importar_bd_async():
        try:
            import subprocess

            mysql_path = _resolve_executable("mysql")
            if not mysql_path:
                _set_status(
                    "❌ mysql no encontrado. Verifica PATH o la instalación de XAMPP.",
                    "#ef4444",
                )
                return

            files = await file_picker.pick_files(
                allow_multiple=False,
                allowed_extensions=["sql"],
                dialog_title="Seleccionar respaldo de BD",
            )

            if not files:
                _set_status("⚠️ Restauración cancelada por el usuario.", "#f59e0b")
                return

            selected = files[0]
            archivo = getattr(selected, "path", None) or str(selected)
            if not archivo or not os.path.exists(archivo):
                _set_status("❌ No se pudo determinar la ruta del archivo seleccionado.", "#ef4444")
                return

            with open(archivo, "r", encoding="utf-8", errors="ignore") as f:
                sql_content = f.read()

            resultado = subprocess.run(
                [mysql_path, "-u", DEFAULT_DB_USER, DEFAULT_DB_NAME],
                input=sql_content,
                capture_output=True,
                text=True,
                timeout=120,
            )

            if resultado.returncode == 0:
                _set_status(f"✅ Base de datos restaurada desde: {archivo}", "#10b981")
                return

            stderr = (resultado.stderr or "").strip()
            stdout = (resultado.stdout or "").strip()
            detalle = stderr or stdout or "No se pudo restaurar la base de datos."
            _set_status(f"❌ Error al restaurar: {detalle[:250]}", "#ef4444")

        except Exception as ex:
            _set_status(f"❌ Error: {str(ex)[:250]}", "#ef4444")

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
                                        ft.Text(
                                            "Exportar Base de Datos",
                                            size=18,
                                            weight="bold",
                                            color=COLOR_TEXTO,
                                        ),
                                        ft.Container(height=4),
                                        ft.Text(
                                            "Genera un archivo .sql con todos los datos actuales del sistema y lo guarda en el Escritorio.",
                                            size=13,
                                            color=COLOR_TEXTO_SEC,
                                        ),
                                    ],
                                    spacing=0,
                                    expand=True,
                                ),
                            ],
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        ft.Container(height=16),
                        boton_primario(
                            "Exportar Ahora",
                            ft.Icons.DOWNLOAD_ROUNDED,
                            on_click=lambda _: page.run_task(_exportar_bd_async),
                        ),
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
                                        ft.Text(
                                            "Importar / Restaurar Base de Datos",
                                            size=18,
                                            weight="bold",
                                            color=COLOR_TEXTO,
                                        ),
                                        ft.Container(height=4),
                                        ft.Text(
                                            "Selecciona un archivo .sql previamente exportado para restaurar los datos del sistema.",
                                            size=13,
                                            color=COLOR_TEXTO_SEC,
                                        ),
                                    ],
                                    spacing=0,
                                    expand=True,
                                ),
                            ],
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        ft.Container(height=16),
                        boton_primario(
                            "Seleccionar Archivo .sql",
                            ft.Icons.UPLOAD_FILE_ROUNDED,
                            on_click=lambda _: page.run_task(_importar_bd_async),
                        ),
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
