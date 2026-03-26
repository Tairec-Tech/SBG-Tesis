"""Pantalla — Información Legal."""

import flet as ft
from theme import (
    COLOR_TEXTO,
    COLOR_TEXTO_SEC,
    COLOR_FONDO_VERDE,
    COLOR_PRIMARIO,
)
from components import titulo_pagina, card_principal


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

    contenido = ft.Column(
        [
            back_btn,
            titulo_pagina("Información Legal", "Términos, políticas y avisos legales"),
            ft.Container(height=24),
            card_principal(
                ft.Column(
                    [
                        ft.Text("Términos de Uso", size=18, weight="bold", color=COLOR_TEXTO),
                        ft.Container(height=12),
                        ft.Text(
                            "Este software ha sido desarrollado exclusivamente con fines educativos y de gestión interna "
                            "para las brigadas escolares de instituciones educativas del municipio Maracaibo. "
                            "Queda prohibida su reproducción total o parcial sin autorización expresa de los desarrolladores.",
                            size=13, color=COLOR_TEXTO_SEC,
                        ),
                    ],
                    spacing=0,
                ),
            ),
            ft.Container(height=16),
            card_principal(
                ft.Column(
                    [
                        ft.Text("Política de Privacidad", size=18, weight="bold", color=COLOR_TEXTO),
                        ft.Container(height=12),
                        ft.Text(
                            "Los datos personales almacenados en este sistema (nombres, cédulas, correos electrónicos) "
                            "son utilizados exclusivamente para la gestión de las brigadas y no serán compartidos "
                            "con terceros bajo ninguna circunstancia. El sistema cumple con los estándares de "
                            "protección de datos escolares vigentes.",
                            size=13, color=COLOR_TEXTO_SEC,
                        ),
                    ],
                    spacing=0,
                ),
            ),
            ft.Container(height=16),
            card_principal(
                ft.Column(
                    [
                        ft.Text("Licencia de Software", size=18, weight="bold", color=COLOR_TEXTO),
                        ft.Container(height=12),
                        ft.Text(
                            "Todos los componentes de software utilizados en esta aplicación son de código abierto o "
                            "poseen licencia educativa vigente. Flet Framework (Apache 2.0), Python (PSF License), "
                            "MySQL (GPL). El diseño visual y la lógica de negocio son propiedad del equipo de desarrollo.",
                            size=13, color=COLOR_TEXTO_SEC,
                        ),
                    ],
                    spacing=0,
                ),
            ),
            ft.Container(height=16),
            card_principal(
                ft.Column(
                    [
                        ft.Text("Aviso Legal", size=18, weight="bold", color=COLOR_TEXTO),
                        ft.Container(height=12),
                        ft.Text(
                            "Este sistema se proporciona \"tal cual\" sin garantías de ningún tipo. Los desarrolladores "
                            "no se hacen responsables por pérdida de datos o daños derivados del uso del sistema. "
                            "Se recomienda realizar copias de seguridad periódicas de la base de datos.",
                            size=13, color=COLOR_TEXTO_SEC,
                        ),
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
