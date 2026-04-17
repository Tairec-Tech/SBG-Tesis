import os

file_path = 'screens/screen_statistics.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

import re

# We will split the file to insert helper functions right before _build_con_graficos
split_idx = content.find("def _build_con_graficos(")

helpers = """
def _build_kpis(kpis, cfg):
    lbl_vol, ico_vol, clr_vol = cfg["kpi_voluntarios"]
    lbl_hrs, ico_hrs, clr_hrs = cfg["kpi_horas"]
    lbl_dep, ico_dep, clr_dep = cfg["kpi_despliegue"]
    lbl_imp, ico_imp, clr_imp = cfg["kpi_impactos"]
    lbl_efe, ico_efe, clr_efe = cfg["kpi_efectividad"]

    return ft.Row(
        [
            ft.Container(card_kpi(lbl_vol, kpis.get("voluntariado_activo", 0), ico_vol, clr_vol), expand=True),
            ft.Container(card_kpi(lbl_hrs, kpis.get("horas_invertidas", 0), ico_hrs, clr_hrs), expand=True),
            ft.Container(card_kpi(lbl_dep, f"{kpis.get('despliegue_operativo', 0)}%", ico_dep, clr_dep), expand=True),
            ft.Container(card_kpi(lbl_imp, kpis.get("impacto_documentado", 0), ico_imp, clr_imp), expand=True),
            ft.Container(card_kpi(lbl_efe, f"{kpis.get('tasa_efectividad', 0)}%", ico_efe, clr_efe), expand=True),
        ],
        spacing=16,
        alignment=ft.MainAxisAlignment.START,
    )

def _build_bar_chart(act_por_mes, cfg, tooltip_barras):
    bar_groups = []
    bar_labels = []
    meses_es = {1: "Ene", 2: "Feb", 3: "Mar", 4: "Abr", 5: "May", 6: "Jun",
                7: "Jul", 8: "Ago", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dic"}
    colores_barras = cfg["colores_barras"]

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
                    tooltip=f"{nombre_mes}: {cantidad} {tooltip_barras}",
                )],
            ))
    max_actividades = max([item[1] for item in act_por_mes]) if act_por_mes else 10
    return fch.BarChart(
        expand=True, interactive=True, max_y=max_actividades + max(5, int(max_actividades * 0.25)),
        border=ft.Border.all(1, COLOR_BORDE),
        horizontal_grid_lines=fch.ChartGridLines(color=ft.Colors.with_opacity(0.1, "grey"), width=1, dash_pattern=[4, 4]),
        left_axis=fch.ChartAxis(label_size=40, title=ft.Text(tooltip_barras.capitalize(), size=12, color=COLOR_TEXTO_SEC, weight="w500"), title_size=42),
        bottom_axis=fch.ChartAxis(label_size=48, labels=bar_labels),
        groups=bar_groups,
    )

def _build_line_chart(reportes_tendencia, cfg):
    puntos_linea = []
    line_labels = []
    meses_es = {1: "Ene", 2: "Feb", 3: "Mar", 4: "Abr", 5: "May", 6: "Jun",
                7: "Jul", 8: "Ago", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dic"}
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

            puntos_linea.append(fch.LineChartDataPoint(idx, val, tooltip=f"{nombre_mes}: {val} reportes"))
            line_labels.append(fch.ChartAxisLabel(value=idx, label=ft.Container(ft.Text(nombre_mes, size=12, weight="w500", color=COLOR_TEXTO_SEC), padding=ft.padding.only(top=6))))
    max_reportes = max([item[1] for item in reportes_tendencia]) if reportes_tendencia else 10
    return fch.LineChart(
        expand=True,
        data_series=[fch.LineChartData(stroke_width=4, color=cfg["color_linea"], curved=True, rounded_stroke_cap=True, points=puntos_linea)],
        min_y=0, max_y=max_reportes + max(3, int(max_reportes * 0.25)), min_x=0, max_x=max(len(puntos_linea)-1, 1),
        border=ft.Border.all(1, COLOR_BORDE),
        horizontal_grid_lines=fch.ChartGridLines(color=ft.Colors.with_opacity(0.1, "grey"), width=1, dash_pattern=[4, 4]),
        left_axis=fch.ChartAxis(label_size=40, show_labels=True), bottom_axis=fch.ChartAxis(label_size=48, labels=line_labels),
    )

def _build_pie_chart(estados):
    pie_sections = []
    leyenda_items = []
    colores_estados = {"Completada": "#10b981", "Pendiente": "#3b82f6", "En progreso": "#f59e0b", "Cancelada": "#ef4444"}
    if not estados:
        pie_sections.append(fch.PieChartSection(value=100, title="Sin Datos", color=COLOR_BORDE, radius=80, title_style=ft.TextStyle(size=13, color=COLOR_TEXTO_SEC, weight="bold")))
    else:
        total_actividades = sum([e["conteo"] for e in estados])
        for est in estados:
            nombre = est.get("estado", "Otro")
            conteo = est["conteo"]
            color_est = colores_estados.get(nombre, "#94a3b8")
            porcentaje = (conteo / total_actividades) * 100 if total_actividades > 0 else 0
            titulo_seccion = f"{int(porcentaje)}%" if porcentaje > 8 else ""
            pie_sections.append(fch.PieChartSection(value=conteo, title=titulo_seccion, color=color_est, radius=80, title_style=ft.TextStyle(size=13, color=ft.Colors.WHITE, weight="bold")))
            leyenda_items.append(ft.Row([
                ft.Container(width=14, height=14, bgcolor=color_est, border_radius=4),
                ft.Container(width=8), ft.Text(f"{nombre}", size=13, color=COLOR_TEXTO, weight="w500"),
                ft.Container(width=4), ft.Text(f"({conteo} — {int(porcentaje)}%)", size=12, color=COLOR_TEXTO_SEC)
            ], spacing=0, vertical_alignment=ft.CrossAxisAlignment.CENTER))
    return fch.PieChart(expand=True, sections_space=3, center_space_radius=46, center_space_color=ft.Colors.SURFACE, sections=pie_sections), leyenda_items

"""

new_build_main = """def _build_con_graficos(page: ft.Page) -> ft.Control:
    # 1. Obtener tipo de brigada y cfg sincrónicamente
    _tb = (page.data or {}).get("brigada_activa")
    cfg = _get_config(_tb)

    ck_kpis = f"_cache_stats_kpis_{_tb}"
    ck_bar  = f"_cache_stats_bar_{_tb}"
    ck_line = f"_cache_stats_line_{_tb}"
    ck_pie  = f"_cache_stats_pie_{_tb}"
    
    loading_key = f"_stats_loading_{_tb}"
    loaded_key = f"_stats_loaded_{_tb}"
    
    is_loaded = bool(page.data.get(loaded_key))
    
    # Contenedores vacíos para reemplazo de contenido dinámico
    kpis_container = ft.Container(height=110, alignment=ft.alignment.center)
    bar_container = ft.Container(height=320, alignment=ft.alignment.center)
    line_container = ft.Container(height=320, alignment=ft.alignment.center)
    pie_chart_container = ft.Container(height=280, alignment=ft.alignment.center, expand=True)
    pie_legend_container = ft.Container(alignment=ft.alignment.center)

    def popular_vistas():
        kpis_data = page.data.get(ck_kpis, {})
        kpis_container.content = _build_kpis(kpis_data, cfg)
        
        acts_data = page.data.get(ck_bar, [])
        bar_container.content = _build_bar_chart(acts_data, cfg, cfg["chart_barras_tooltip"])
        
        rep_data = page.data.get(ck_line, [])
        line_container.content = _build_line_chart(rep_data, cfg)
        
        est_data = page.data.get(ck_pie, [])
        pie_ch, pie_leg = _build_pie_chart(est_data)
        pie_chart_container.content = pie_ch
        pie_legend_container.content = ft.Column(
            pie_leg if pie_leg else [ft.Text("Sin datos", color=COLOR_TEXTO_SEC, italic=True)],
            spacing=12, alignment=ft.MainAxisAlignment.CENTER,
        )

    if is_loaded:
        popular_vistas()
    else:
        # Skeletons
        kpis_container.content = ft.ProgressRing()
        bar_container.content = ft.ProgressRing()
        line_container.content = ft.ProgressRing()
        pie_chart_container.content = ft.ProgressRing()
        pie_legend_container.content = ft.Text("Cargando...", color=COLOR_TEXTO_SEC)

    async def _load_data_async():
        if getattr(page, "data", None) is None: return
        if page.data.get(loading_key) or page.data.get(loaded_key): return
        page.data[loading_key] = True

        try:
            import asyncio
            kpis = await asyncio.to_thread(crud_est.get_kpis_estadisticas, _tb)
            act_por_mes = await asyncio.to_thread(crud_est.get_actividades_por_mes, _tb)
            reportes_tendencia = await asyncio.to_thread(crud_est.get_tendencia_reportes_por_mes, _tb)
            estados = await asyncio.to_thread(crud_est.get_distribucion_estados_actividades, _tb)

            page.data[ck_kpis] = kpis
            page.data[ck_bar] = act_por_mes
            page.data[ck_line] = reportes_tendencia
            page.data[ck_pie] = estados
            
            # Popular la vista con los datos ya cacheados
            popular_vistas()
            if page.session: page.update()
            
            # Solo si todo fue bien marcamos como loaded (sin excepciones)
            page.data[loaded_key] = True

        except Exception as e:
            print(f"Error en carga asíncrona de estadísticas: {e}")
        finally:
            page.data[loading_key] = False

    if not is_loaded:
        page.run_task(_load_data_async)

    # Layout Principal
    fila_1 = ft.Row([
        ft.Container(content=_tarjeta_grafico(cfg["chart_barras_titulo"], bar_container), expand=True),
        ft.Container(width=20),
        ft.Container(content=_tarjeta_grafico(cfg["chart_linea_titulo"], line_container), expand=True),
    ], spacing=0)

    contenido_pie = ft.Row([
        pie_chart_container, ft.Container(width=24), pie_legend_container
    ], vertical_alignment=ft.CrossAxisAlignment.CENTER)

    tarjeta_pie = card_principal(
        ft.Column([
            ft.Text(cfg["chart_pie_titulo"], size=18, weight="bold", color=COLOR_TEXTO),
            ft.Container(height=16),
            contenido_pie,
        ], spacing=0), padding=24
    )

    return ft.Column(
        [
            titulo_pagina(cfg["titulo"], cfg["subtitulo"]),
            ft.Container(height=16),
            kpis_container,
            ft.Container(height=24),
            fila_1,
            ft.Container(height=24),
            tarjeta_pie,
            ft.Container(height=24),
        ], scroll=ft.ScrollMode.AUTO, expand=True, spacing=0
    )
"""

before_build = content[:split_idx]
end_build_idx = content.find("def _build_sin_graficos() -> ft.Control:")
after_build = content[end_build_idx:]

final_content = before_build + helpers + new_build_main + "\n\n" + after_build

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(final_content)
print("File updated successfully.")
