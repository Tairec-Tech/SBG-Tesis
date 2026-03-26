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
from components import titulo_pagina, card_principal, card_kpi
import database.crud_estadisticas as crud_est

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
                ft.Container(content=grafico, height=altura),
            ],
            spacing=0,
        ),
        padding=24,
    )


def _build_con_graficos(page: ft.Page) -> ft.Control:
    """Construye la vista de estadísticas con BarChart, LineChart y PieChart con DATOS REALES."""
    # Obtener datos matemáticos (filtrados por tipo de brigada activa)
    _tb = (page.data or {}).get("brigada_activa")
    kpis = crud_est.get_kpis_estadisticas(_tb)
    act_por_mes = crud_est.get_actividades_por_mes(_tb)
    reportes_tendencia = crud_est.get_tendencia_reportes_por_mes(_tb)
    estados = crud_est.get_distribucion_estados_actividades(_tb)

    # Colores base
    verde_1 = COLOR_PRIMARIO_OSCURO
    verde_2 = COLOR_PRIMARIO
    verde_3 = COLOR_PRIMARIO_CLARO
    verde_4 = COLOR_VERDE_SUAVE

    # --- Nueva Fila de KPIs (Métricas Globales de Alto Impacto) ---
    fila_kpis = ft.Row(
        [
            ft.Container(card_kpi("Voluntarios", kpis.get("voluntariado_activo", 0), ft.Icons.PEOPLE_ALT_ROUNDED, ft.Colors.BLUE), expand=True),
            ft.Container(card_kpi("Horas Ecológicas", kpis.get("horas_invertidas", 0), ft.Icons.HOURGLASS_BOTTOM_ROUNDED, ft.Colors.GREEN), expand=True),
            ft.Container(card_kpi("Despliegue", f"{kpis.get('despliegue_operativo', 0)}%", ft.Icons.SHARE_LOCATION_ROUNDED, ft.Colors.ORANGE), expand=True),
            ft.Container(card_kpi("Impactos", kpis.get("impacto_documentado", 0), ft.Icons.PUBLIC_ROUNDED, ft.Colors.PURPLE), expand=True),
            ft.Container(card_kpi("Efectividad", f"{kpis.get('tasa_efectividad', 0)}%", ft.Icons.TRENDING_UP_ROUNDED, ft.Colors.TEAL), expand=True),
        ],
        spacing=16,
        alignment=ft.MainAxisAlignment.START,
    )

    # --- BarChart mejorado: Actividades por mes ---
    bar_groups = []
    bar_labels = []
    import calendar
    
    # Nombres de meses en español
    meses_es = {1: "Ene", 2: "Feb", 3: "Mar", 4: "Abr", 5: "May", 6: "Jun",
                7: "Jul", 8: "Ago", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dic"}
    
    # Gradiente visual de barras (de claro a oscuro según actividad)
    colores_barras = [
        "#10b981", "#059669", "#047857", "#065f46", "#064e3b", "#022c22"
    ]
    
    if not act_por_mes:
        bar_labels.append(fch.ChartAxisLabel(value=0, label=ft.Container(ft.Text("Sin datos", size=11, color=COLOR_TEXTO_SEC), padding=8)))
        bar_groups.append(fch.BarChartGroup(x=0, rods=[fch.BarChartRod(from_y=0, to_y=0, width=36, color=COLOR_BORDE, border_radius=8)]))
    else:
        for index, item in enumerate(act_por_mes):
            mes_str = item[0]
            cantidad = item[1]
            try:
                mes_num = int(mes_str.split("-")[1])
                nombre_mes = meses_es.get(mes_num, mes_str)
            except:
                nombre_mes = mes_str
            
            bar_labels.append(fch.ChartAxisLabel(
                value=index, 
                label=ft.Container(ft.Text(nombre_mes, size=12, weight="w500", color=COLOR_TEXTO_SEC), padding=ft.padding.only(top=8))
            ))
            color_barra = colores_barras[index % len(colores_barras)]
            bar_groups.append(fch.BarChartGroup(
                x=index, 
                rods=[fch.BarChartRod(
                    from_y=0, to_y=cantidad, width=36, color=color_barra, border_radius=8,
                    tooltip=f"{nombre_mes}: {cantidad} actividades",
                )],
            ))

    max_actividades = max([item[1] for item in act_por_mes]) if act_por_mes else 10

    chart_barras = fch.BarChart(
        expand=True,
        interactive=True,
        max_y=max_actividades + max(5, int(max_actividades * 0.25)),
        border=ft.Border.all(1, COLOR_BORDE),
        horizontal_grid_lines=fch.ChartGridLines(color=ft.Colors.with_opacity(0.1, "grey"), width=1, dash_pattern=[4, 4]),
        left_axis=fch.ChartAxis(label_size=40, title=ft.Text("Actividades", size=12, color=COLOR_TEXTO_SEC, weight="w500"), title_size=42),
        bottom_axis=fch.ChartAxis(label_size=48, labels=bar_labels),
        groups=bar_groups,
    )

    # --- LineChart mejorado: Tendencia de reportes ---
    puntos_linea = []
    line_labels = []
    if not reportes_tendencia:
        puntos_linea.append(fch.LineChartDataPoint(0, 0))
        puntos_linea.append(fch.LineChartDataPoint(1, 0))
        line_labels.append(fch.ChartAxisLabel(value=0, label=ft.Text("-", size=11, color=COLOR_TEXTO_SEC)))
    else:
        for idx, rt in enumerate(reportes_tendencia):
            mes_str = rt[0]
            val = rt[1]
            try:
                mes_num = int(mes_str.split("-")[1])
                nombre_mes = meses_es.get(mes_num, mes_str)
            except:
                nombre_mes = mes_str
                
            puntos_linea.append(fch.LineChartDataPoint(
                idx, val,
                tooltip=f"{nombre_mes}: {val} reportes",
            ))
            line_labels.append(fch.ChartAxisLabel(
                value=idx, 
                label=ft.Container(ft.Text(nombre_mes, size=12, weight="w500", color=COLOR_TEXTO_SEC), padding=ft.padding.only(top=6))
            ))
            
    max_reportes = max([item[1] for item in reportes_tendencia]) if reportes_tendencia else 10
    
    chart_linea = fch.LineChart(
        expand=True,
        data_series=[
            fch.LineChartData(
                stroke_width=4, 
                color="#10b981",
                curved=True, 
                rounded_stroke_cap=True,
                points=puntos_linea,
            ),
        ],
        min_y=0,
        max_y=max_reportes + max(3, int(max_reportes * 0.25)),
        min_x=0,
        max_x=max(len(puntos_linea)-1, 1),
        border=ft.Border.all(1, COLOR_BORDE),
        horizontal_grid_lines=fch.ChartGridLines(color=ft.Colors.with_opacity(0.1, "grey"), width=1, dash_pattern=[4, 4]),
        left_axis=fch.ChartAxis(label_size=40, show_labels=True),
        bottom_axis=fch.ChartAxis(label_size=48, labels=line_labels),
    )

    # --- PieChart mejorado: Distribución de estados con leyenda ---
    pie_sections = []
    leyenda_items = []
    
    colores_estados = {
        "Completada": "#10b981",   # Verde esmeralda
        "Pendiente": "#3b82f6",    # Azul 
        "En progreso": "#f59e0b",  # Ámbar
        "Cancelada": "#ef4444",    # Rojo
    }
    
    if not estados:
        pie_sections.append(
            fch.PieChartSection(value=100, title="Sin Datos", color=COLOR_BORDE, radius=80, 
                               title_style=ft.TextStyle(size=13, color=COLOR_TEXTO_SEC, weight="bold"))
        )
    else:
        total_actividades = sum([e["conteo"] for e in estados])
        for est in estados:
            nombre = est.get("estado", "Otro")
            conteo = est["conteo"]
            color_est = colores_estados.get(nombre, "#94a3b8")
            porcentaje = (conteo / total_actividades) * 100 if total_actividades > 0 else 0
            
            titulo_seccion = f"{int(porcentaje)}%" if porcentaje > 8 else ""
            pie_sections.append(
                fch.PieChartSection(
                    value=conteo, 
                    title=titulo_seccion, 
                    color=color_est, 
                    radius=80, 
                    title_style=ft.TextStyle(size=13, color=ft.Colors.WHITE, weight="bold"),
                )
            )
            # Construir item de leyenda visual
            leyenda_items.append(
                ft.Row([
                    ft.Container(width=14, height=14, bgcolor=color_est, border_radius=4),
                    ft.Container(width=8),
                    ft.Text(f"{nombre}", size=13, color=COLOR_TEXTO, weight="w500"),
                    ft.Container(width=4),
                    ft.Text(f"({conteo} — {int(porcentaje)}%)", size=12, color=COLOR_TEXTO_SEC),
                ], spacing=0, vertical_alignment=ft.CrossAxisAlignment.CENTER)
            )

    chart_pie = fch.PieChart(
        expand=True,
        sections_space=3,
        center_space_radius=46,
        center_space_color=ft.Colors.SURFACE,
        sections=pie_sections,
    )
    
    # Contenedor de la Dona con su leyenda al lado
    contenido_pie = ft.Row(
        [
            ft.Container(content=chart_pie, expand=True, height=280),
            ft.Container(width=24),
            ft.Column(
                leyenda_items if leyenda_items else [ft.Text("Sin datos", color=COLOR_TEXTO_SEC, italic=True)],
                spacing=12,
                alignment=ft.MainAxisAlignment.CENTER,
            )
        ],
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # --- Layout de las tarjetas de gráficos ---
    fila_1 = ft.Row(
        [
            ft.Container(content=_tarjeta_grafico("📊 Actividades por Mes", chart_barras), expand=True),
            ft.Container(width=20),
            ft.Container(content=_tarjeta_grafico("📈 Tendencia de Reportes", chart_linea), expand=True),
        ],
        spacing=0,
    )
    
    # El PieChart usa un layout especial con leyenda integrada
    tarjeta_pie = card_principal(
        ft.Column(
            [
                ft.Text("🍩 Distribución de Estados de Actividades", size=18, weight="bold", color=COLOR_TEXTO),
                ft.Container(height=16),
                contenido_pie,
            ],
            spacing=0,
        ),
        padding=24,
    )

    return ft.Column(
        [
            titulo_pagina(
                "Centro de Mando Estadístico",
                "Monitoreo global del avance e impacto de las brigadas",
            ),
            ft.Container(height=16),
            fila_kpis,
            ft.Container(height=24),
            fila_1,
            ft.Container(height=24),
            tarjeta_pie,
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
