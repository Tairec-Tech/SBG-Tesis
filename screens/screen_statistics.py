"""
Estadísticas — Gráficos con flet_charts (BarChart, LineChart, PieChart).
Tonos verdes (brigadas ambientales). Fallback "En construcción" si flet_charts no está instalado.
"""

import flet as ft
from theme import (
    COLOR_TEXTO,
    COLOR_TEXTO_SEC,
    COLOR_FONDO_VERDE,
    COLOR_PRIMARIO,
    COLOR_PRIMARIO_CLARO,
    COLOR_PRIMARIO_OSCURO,
    COLOR_VERDE_SUAVE,
    COLOR_BORDE,
)
from components import titulo_pagina, card_principal

# Gráficos: paquete opcional (pip install flet-charts)
try:
    import flet_charts as fch
    HAS_CHARTS = True
except ImportError:
    fch = None
    HAS_CHARTS = False


def _tarjeta_grafico(titulo: str, grafico: ft.Control, altura: float = 320) -> ft.Container:
    return card_principal(
        ft.Column(
            [
                ft.Text(titulo, size=18, weight="bold", color=COLOR_TEXTO),
                ft.Container(height=20),
                ft.Container(content=grafico, height=altura, expand=True),
            ],
            spacing=0,
            expand=True,
        ),
        padding=24,
    )


def _build_con_graficos(page: ft.Page) -> ft.Control:
    """Construye la vista de estadísticas con BarChart, LineChart y PieChart (tonos verdes)."""
    # Colores para gráficos (brigadas ambientales)
    verde_1 = COLOR_PRIMARIO_OSCURO
    verde_2 = COLOR_PRIMARIO
    verde_3 = COLOR_PRIMARIO_CLARO
    verde_4 = COLOR_VERDE_SUAVE

    # --- BarChart: Actividades por mes ---
    chart_barras = fch.BarChart(
        expand=True,
        interactive=True,
        max_y=120,
        border=ft.Border.all(1, COLOR_BORDE),
        horizontal_grid_lines=fch.ChartGridLines(
            color=ft.Colors.with_opacity(0.15, "grey"), width=1, dash_pattern=[3, 3]
        ),
        tooltip=fch.BarChartTooltip(
            bgcolor=ft.Colors.with_opacity(0.92, "#f0fdf4"),
            border_radius=ft.BorderRadius.all(8),
        ),
        left_axis=fch.ChartAxis(
            label_size=40,
            title=ft.Text("Cantidad", size=12, color=COLOR_TEXTO_SEC),
            title_size=40,
        ),
        right_axis=fch.ChartAxis(show_labels=False),
        bottom_axis=fch.ChartAxis(
            label_size=40,
            labels=[
                fch.ChartAxisLabel(value=0, label=ft.Container(ft.Text("Ene", size=11, color=COLOR_TEXTO_SEC), padding=8)),
                fch.ChartAxisLabel(value=1, label=ft.Container(ft.Text("Feb", size=11, color=COLOR_TEXTO_SEC), padding=8)),
                fch.ChartAxisLabel(value=2, label=ft.Container(ft.Text("Mar", size=11, color=COLOR_TEXTO_SEC), padding=8)),
                fch.ChartAxisLabel(value=3, label=ft.Container(ft.Text("Abr", size=11, color=COLOR_TEXTO_SEC), padding=8)),
                fch.ChartAxisLabel(value=4, label=ft.Container(ft.Text("May", size=11, color=COLOR_TEXTO_SEC), padding=8)),
                fch.ChartAxisLabel(value=5, label=ft.Container(ft.Text("Jun", size=11, color=COLOR_TEXTO_SEC), padding=8)),
            ],
        ),
        groups=[
            fch.BarChartGroup(x=0, rods=[fch.BarChartRod(from_y=0, to_y=0, width=32, color=verde_1, border_radius=6)]),
            fch.BarChartGroup(x=1, rods=[fch.BarChartRod(from_y=0, to_y=0, width=32, color=verde_2, border_radius=6)]),
            fch.BarChartGroup(x=2, rods=[fch.BarChartRod(from_y=0, to_y=0, width=32, color=verde_1, border_radius=6)]),
            fch.BarChartGroup(x=3, rods=[fch.BarChartRod(from_y=0, to_y=0, width=32, color=verde_3, border_radius=6)]),
            fch.BarChartGroup(x=4, rods=[fch.BarChartRod(from_y=0, to_y=0, width=32, color=verde_2, border_radius=6)]),
            fch.BarChartGroup(x=5, rods=[fch.BarChartRod(from_y=0, to_y=0, width=32, color=verde_1, border_radius=6)]),
        ],
    )

    # --- LineChart: Tendencia de reportes ---
    chart_linea = fch.LineChart(
        expand=True,
        data_series=[
            fch.LineChartData(
                stroke_width=5,
                color=verde_2,
                curved=True,
                rounded_stroke_cap=True,
                points=[fch.LineChartDataPoint(0, 0), fch.LineChartDataPoint(10, 0)],
            ),
        ],
        min_y=0,
        max_y=10,
        min_x=0,
        max_x=10,
        border=ft.Border.all(1, COLOR_BORDE),
        horizontal_grid_lines=fch.ChartGridLines(
            color=ft.Colors.with_opacity(0.12, "grey"), width=1
        ),
        tooltip=fch.LineChartTooltip(
            bgcolor=ft.Colors.with_opacity(0.92, "#f0fdf4"),
        ),
        left_axis=fch.ChartAxis(label_size=40, show_labels=True),
        bottom_axis=fch.ChartAxis(
            label_size=32,
            labels=[
                fch.ChartAxisLabel(value=2, label=ft.Text("Sem 1", size=11, color=COLOR_TEXTO_SEC)),
                fch.ChartAxisLabel(value=5, label=ft.Text("Sem 2", size=11, color=COLOR_TEXTO_SEC)),
                fch.ChartAxisLabel(value=8, label=ft.Text("Sem 3", size=11, color=COLOR_TEXTO_SEC)),
            ],
        ),
    )

    # --- PieChart: Distribución (donut) ---
    chart_pie = fch.PieChart(
        expand=True,
        sections_space=2,
        center_space_radius=42,
        sections=[
            fch.PieChartSection(
                value=100,
                title="Sin datos",
                color=verde_2,
                radius=72,
                title_style=ft.TextStyle(size=14, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
            ),
        ],
    )

    fila_1 = ft.Row(
        [
            ft.Container(content=_tarjeta_grafico("Actividades por mes", chart_barras), expand=True),
            ft.Container(width=24),
            ft.Container(content=_tarjeta_grafico("Tendencia de reportes", chart_linea), expand=True),
        ],
        spacing=0,
        expand=True,
    )
    fila_2 = ft.Row(
        [
            ft.Container(content=_tarjeta_grafico("Distribución", chart_pie, altura=320), expand=True),
        ],
        spacing=0,
        expand=True,
    )

    return ft.Column(
        [
            titulo_pagina(
                "Estadísticas",
                "Sistema de coordinación de brigadas escolares — Brigadas Ambientales",
            ),
            ft.Container(height=24),
            fila_1,
            ft.Container(height=24),
            fila_2,
            ft.Container(height=24),
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        spacing=0,
    )


def _build_sin_graficos() -> ft.Control:
    """Vista cuando flet_charts no está instalado."""
    return ft.Column(
        [
            titulo_pagina(
                "Estadísticas",
                "Sistema de coordinación de brigadas escolares",
            ),
            ft.Container(height=32),
            card_principal(
                ft.Column(
                    [
                        ft.Icon(ft.Icons.CONSTRUCTION_OUTLINED, color=COLOR_PRIMARIO, size=64),
                        ft.Container(height=24),
                        ft.Text("En construcción", size=22, weight="bold", color=COLOR_TEXTO),
                        ft.Container(height=8),
                        ft.Text(
                            "Los gráficos requieren el paquete flet-charts. Instálalo con: pip install flet-charts",
                            size=14,
                            color=COLOR_TEXTO_SEC,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Container(height=8),
                        ft.Text(
                            "Después reinicia la aplicación.",
                            size=13,
                            color=COLOR_TEXTO_SEC,
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=0,
                ),
                padding=48,
            ),
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        spacing=0,
    )


def build(page: ft.Page, **kwargs) -> ft.Control:
    if HAS_CHARTS:
        contenido = _build_con_graficos(page)
    else:
        contenido = _build_sin_graficos()

    return ft.Container(
        content=contenido,
        padding=24,
        bgcolor=COLOR_FONDO_VERDE,
        expand=True,
    )
