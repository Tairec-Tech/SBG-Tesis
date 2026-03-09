"""Pantalla — Manual de Usuario."""

import flet as ft
from theme import (
    COLOR_TEXTO,
    COLOR_TEXTO_SEC,
    COLOR_FONDO_VERDE,
    COLOR_PRIMARIO,
    COLOR_PRIMARIO_CLARO,
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

    secciones = [
        ("🏠 Panel Principal", "Visualiza los KPIs principales del sistema: total de brigadas, usuarios activos, actividades completadas y pendientes. También muestra las actividades más recientes y el mensaje del día."),
        ("🛡️ Gestión de Brigadas", "Crea, edita y administra las brigadas ambientales. Asigna coordinadores y establece las áreas de operación de cada brigada."),
        ("📋 Actividades", "Planifica y registra las actividades ecológicas. Establece fechas de inicio y fin, asigna brigadas responsables y haz seguimiento del estado de cada actividad."),
        ("👥 Brigadistas", "Gestiona la lista de estudiantes brigadistas. Inscribe nuevos miembros, asígnalos a brigadas y consulta su información de contacto."),
        ("📊 Estadísticas", "Centro de mando analítico con gráficos interactivos: actividades por mes (barras), tendencia de reportes (líneas) y distribución de estados (dona). Incluye 5 indicadores clave de rendimiento."),
        ("📝 Reportes", "Genera y consulta tres tipos de reportes: Reportes de Incidentes, Reportes de Actividades y Reportes de Impacto. Cada uno puede descargarse en formato Word (.docx)."),
        ("⏰ Turnos y Horarios", "Organiza los turnos de las brigadas y establece los horarios de actividades y vigilancia ambiental."),
        ("📚 Contenido Educativo", "Accede a materiales educativos sobre medio ambiente, reciclaje y conservación para compartir con los brigadistas."),
    ]

    cards = []
    for titulo, descripcion in secciones:
        cards.append(
            card_principal(
                ft.Column(
                    [
                        ft.Text(titulo, size=16, weight="bold", color=COLOR_TEXTO),
                        ft.Container(height=8),
                        ft.Text(descripcion, size=13, color=COLOR_TEXTO_SEC),
                    ],
                    spacing=0,
                ),
                padding=20,
            )
        )
        cards.append(ft.Container(height=12))

    contenido = ft.Column(
        [
            back_btn,
            titulo_pagina("Manual de Usuario", "Guía rápida para el uso del sistema"),
            ft.Container(height=24),
        ]
        + cards,
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
