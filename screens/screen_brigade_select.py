"""Pantalla — Selección de Brigada (2×2 grid premium con gradientes y animaciones)."""

import json
import flet as ft
from theme import BRIGADAS


def build(page: ft.Page, on_select) -> ft.Control:
    """
    4 cuadrantes a pantalla completa con gradientes, iconos de fondo gigantes,
    animación escalonada de entrada, spotlight hover y descripción dinámica.
    """

    # Obtener nombre de institución del usuario logueado
    try:
        _data = (page.data or {}).get("usuario_actual", {}) if isinstance(page.data, dict) else {}
        inst_nombre = _data.get("institucion_nombre", "")
    except Exception:
        inst_nombre = ""

    # Config: (key, icono, gradiente, nombre, sub, descripcion, texto_color)
    # texto_color: "white" para fondos oscuros, "#1e293b" para Convivencia (fondo claro)
    brigadas_config = [
        (
            "riesgo", ft.Icons.HEALTH_AND_SAFETY,
            ["#b91c1c", "#dc2626", "#ef4444"],
            "Gestión de Riesgo", "Primeros Auxilios",
            "Gestión de emergencias, evacuación y primeros auxilios",
            "white",
        ),
        (
            "patrulla", ft.Icons.TRAFFIC,
            ["#c2410c", "#ea580c", "#f97316"],
            "Patrulla Escolar", "Seguridad Vial",
            "Seguridad vial, control de tránsito y protección escolar",
            "white",
        ),
        (
            "convivencia", ft.Icons.HANDSHAKE,
            ["#94a3b8", "#cbd5e1", "#e2e8f0"],  # Gradient: gris perla (tono blanco visible)
            "Convivencia y Paz", "Prevención Integral",
            "Mediación de conflictos, cultura de paz y convivencia",
            "#1e293b",  # Texto oscuro sobre fondo claro
        ),
        (
            "ecologica", ft.Icons.ECO,
            ["#047857", "#059669", "#10b981"],
            "Brigada Ecológica", "Medio Ambiente",
            "Conservación ambiental, reciclaje y reforestación",
            "white",
        ),
    ]

    def _on_click(key):
        def handler(_):
            on_select(key)
        return handler

    # Almacenar refs para spotlight hover
    all_containers = []

    def _on_hover_spotlight(idx, grad_normal, grad_hover):
        """Hover: el cuadrante activo se ilumina y agranda, los demás se oscurecen."""
        def handler(e):
            is_hover = e.data == "true"
            for i, (cont, desc_cont) in enumerate(all_containers):
                if i == idx:
                    # El activo: más brillante + scale up + mostrar descripción
                    cont.opacity = 1.0
                    cont.content.controls[1].scale = 1.04 if is_hover else 1.0  # inner content
                    desc_cont.opacity = 1.0 if is_hover else 0.0
                else:
                    # Los demás: oscurecer
                    cont.opacity = 0.65 if is_hover else 1.0
            page.update()
        return handler

    cuadrantes = []
    for idx, (key, icono, grad, nombre, sub, descripcion, txt_color) in enumerate(brigadas_config):
        # Descripción hover (aparece con fade)
        desc_container = ft.Container(
            content=ft.Text(descripcion, size=15, color=ft.Colors.with_opacity(0.8, txt_color),
                            text_align=ft.TextAlign.CENTER, italic=True),
            opacity=0,
            animate_opacity=ft.Animation(250, ft.AnimationCurve.EASE_OUT),
        )

        # Icono de fondo gigante semi-transparente
        is_right_col = idx in (1, 3)
        icon_opacity = 0.12 if key == "convivencia" else 0.07
        bg_icon = ft.Container(
            content=ft.Icon(icono, color=ft.Colors.with_opacity(icon_opacity, txt_color), size=220),
            bottom=-30,
            left=-30 if is_right_col else None,
            right=None if is_right_col else -30,
        )

        # Contenido principal
        circle_bg = ft.Colors.with_opacity(0.15, txt_color)
        circle_border = ft.Colors.with_opacity(0.25, txt_color)
        inner = ft.Column(
            [
                ft.Container(
                    content=ft.Icon(icono, color=txt_color, size=56),
                    width=100,
                    height=100,
                    border_radius=50,
                    bgcolor=circle_bg,
                    alignment=ft.Alignment.CENTER,
                    border=ft.Border.all(2, circle_border),
                ),
                ft.Container(height=16),
                ft.Text(nombre, size=28, weight="bold", color=txt_color,
                        text_align=ft.TextAlign.CENTER),
                ft.Container(height=6),
                ft.Text(sub, size=16, color=ft.Colors.with_opacity(0.7, txt_color),
                        text_align=ft.TextAlign.CENTER),
                ft.Container(height=10),
                desc_container,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            scale=1.0,
            animate_scale=ft.Animation(250, ft.AnimationCurve.EASE_OUT),
        )

        # Stack: icono de fondo gigante + contenido
        stack_content = ft.Stack(
            controls=[bg_icon, ft.Container(content=inner, expand=True, alignment=ft.Alignment.CENTER)],
            expand=True,
        )

        container = ft.Container(
            content=stack_content,
            gradient=ft.LinearGradient(
                begin=ft.Alignment.TOP_LEFT,
                end=ft.Alignment.BOTTOM_RIGHT,
                colors=grad,
            ),
            expand=True,
            alignment=ft.Alignment.CENTER,
            opacity=1.0,
            animate_opacity=ft.Animation(250, ft.AnimationCurve.EASE_OUT),
            on_click=_on_click(key),
            ink=True,
            # Entrada escalonada: empieza invisible
            scale=0.92,
            animate_scale=ft.Animation(500 + idx * 100, ft.AnimationCurve.EASE_OUT_BACK),
        )

        all_containers.append((container, desc_container))
        cuadrantes.append(container)

    # Asignar hover después de tener todos los contenedores
    for idx, (key, icono, grad, nombre, sub, desc, txt) in enumerate(brigadas_config):
        # Gradient hover más brillante
        grad_hover = [grad[1], grad[2], grad[2]]
        cuadrantes[idx].on_hover = _on_hover_spotlight(idx, grad, grad_hover)

    # Header flotante
    header_items = [
        ft.Text("Sistema de Brigadas Escolares", size=26, weight="bold", color="white",
                text_align=ft.TextAlign.CENTER),
    ]
    if inst_nombre:
        header_items.append(ft.Container(height=2))
        header_items.append(
            ft.Text(inst_nombre, size=14, color=ft.Colors.with_opacity(0.85, "white"),
                    text_align=ft.TextAlign.CENTER, italic=True)
        )
    header_items.append(ft.Container(height=6))
    header_items.append(
        ft.Text("Seleccione el tipo de brigada", size=15,
                color=ft.Colors.with_opacity(0.8, "white"),
                text_align=ft.TextAlign.CENTER)
    )

    header = ft.Container(
        content=ft.Container(
            content=ft.Column(
                header_items,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
            ),
            padding=ft.Padding.symmetric(horizontal=28, vertical=14),
            border_radius=16,
            bgcolor=ft.Colors.with_opacity(0.35, "black"),
            blur=ft.Blur(10, 10),
        ),
        top=24,
        left=0,
        right=0,
        alignment=ft.Alignment.CENTER,
    )

    # Grid con spacing=2 sobre fondo oscuro para crear líneas separadoras sin bloquear clicks
    grid = ft.Container(
        content=ft.Column(
            [
                ft.Row([cuadrantes[0], cuadrantes[1]], expand=True, spacing=2),
                ft.Row([cuadrantes[2], cuadrantes[3]], expand=True, spacing=2),
            ],
            expand=True,
            spacing=2,
        ),
        bgcolor=ft.Colors.with_opacity(0.3, "white"),
        expand=True,
    )

    page_content = ft.Stack(
        controls=[grid, header],
        expand=True,
    )

    # Animación escalonada de entrada: hacer visible con delay
    async def _animar_entrada():
        import asyncio
        await asyncio.sleep(0.15)
        for i, (cont, _) in enumerate(all_containers):
            cont.scale = 1.0
            page.update()
            await asyncio.sleep(0.08)

    page.run_task(_animar_entrada)

    return page_content
