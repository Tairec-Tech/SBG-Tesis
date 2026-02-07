"""
Componentes reutilizables del SGB — estilo Figma, tema brigadas ambientales (verde).
"""

import json
import flet as ft
from theme import (
    COLOR_PRIMARIO,
    COLOR_PRIMARIO_CLARO,
    COLOR_SIDEBAR,
    COLOR_SIDEBAR_ACTIVO,
    COLOR_SIDEBAR_TEXTO,
    COLOR_SIDEBAR_TEXTO_SEC,
    COLOR_TEXTO,
    COLOR_TEXTO_SEC,
    COLOR_CARD,
    COLOR_BORDE,
    COLOR_CANCELAR,
    RADIO,
    RADIO_GRANDE,
    get_sombra_suave,
    get_sombra_card,
)


async def build_sidebar(page: ft.Page, contenido_area: ft.Container, vista_actual: list, on_logout, on_nav_change=None, on_go_register=None, on_go_recovery=None):
    """
    Barra lateral verde oscuro: logo, navegación (con subrayado del activo), Modo día/noche compacto, Usuario, Cerrar sesión.
    vista_actual: list de 1 elemento con el nombre de la vista activa.
    on_nav_change: callback para reconstruir el sidebar al cambiar de vista (así se ilumina el ítem correcto).
    """
    def ir(vista_nombre, builder):
        def _(e):
            vista_actual[0] = vista_nombre
            contenido_area.content = builder(page, content_area=contenido_area)
            if on_nav_change:
                on_nav_change()
            page.update()
        return _

    sel = vista_actual[0]

    from screens import (
        screen_dashboard,
        screen_brigades,
        screen_brigadistas,
        screen_shifts,
        screen_reports,
        screen_statistics,
        screen_content,
    )

    items = [
        ("Panel Principal", ft.Icons.DASHBOARD_OUTLINED, screen_dashboard.build),
        ("Gestión de Brigadas", ft.Icons.SHIELD_OUTLINED, screen_brigades.build),
        ("Brigadistas", ft.Icons.PEOPLE_OUTLINED, screen_brigadistas.build),
        ("Turnos y Horarios", ft.Icons.CALENDAR_MONTH_OUTLINED, screen_shifts.build),
        ("Reportes de Incidentes", ft.Icons.ASSIGNMENT_OUTLINED, screen_reports.build),
        ("Estadísticas", ft.Icons.BAR_CHART_OUTLINED, screen_statistics.build),
        ("Contenido Educativo", ft.Icons.MENU_BOOK_OUTLINED, screen_content.build),
    ]

    nav_items = []
    for label, icon, builder in items:
        activo = sel == label
        bg = COLOR_SIDEBAR_ACTIVO if activo else "transparent"
        color_txt = COLOR_SIDEBAR_TEXTO if activo else COLOR_SIDEBAR_TEXTO_SEC
        # Subrayado del ítem activo: borde izquierdo en verde claro
        borde_activo = ft.Border(left=ft.BorderSide(3, COLOR_PRIMARIO_CLARO)) if activo else None
        nav_items.append(
            ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(icon, color=color_txt, size=22),
                        ft.Container(width=12),
                        ft.Text(label, size=14, weight="w500" if activo else "w400", color=color_txt),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                padding=ft.Padding.symmetric(vertical=14, horizontal=20),
                border_radius=10,
                border=borde_activo,
                bgcolor=bg,
                on_click=ir(label, builder),
                data=label,
            )
        )

    # Modo interfaz: toggle compacto (solo iconos) para que Día y Noche quepan en el menú
    modo_dia_activo = True  # estado visual solamente
    btn_dia = ft.IconButton(
        icon=ft.Icons.LIGHT_MODE,
        icon_color=COLOR_SIDEBAR_TEXTO,
        icon_size=22,
        style=ft.ButtonStyle(bgcolor=COLOR_SIDEBAR_ACTIVO, shape=ft.RoundedRectangleBorder(radius=8)),
        tooltip="Modo Día",
    )
    btn_noche = ft.IconButton(
        icon=ft.Icons.DARK_MODE,
        icon_color=COLOR_SIDEBAR_TEXTO_SEC,
        icon_size=22,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        tooltip="Modo Noche",
    )
    modo_toggle = ft.Container(
        content=ft.Column(
            [
                ft.Text("Modo de interfaz", size=12, color=COLOR_SIDEBAR_TEXTO_SEC),
                ft.Container(height=8),
                ft.Row(
                    [btn_dia, ft.Container(width=8), btn_noche],
                    spacing=0,
                ),
            ],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.START,
        ),
        padding=ft.Padding.symmetric(horizontal=20, vertical=12),
    )

    # Usuario activo (desde login) — se guarda como JSON string
    raw = await page.shared_preferences.get("usuario_actual")
    if isinstance(raw, str):
        try:
            usuario_data = json.loads(raw) or {}
        except (json.JSONDecodeError, TypeError):
            usuario_data = {}
    else:
        usuario_data = raw if isinstance(raw, dict) else {}
    nombre_display = f"{usuario_data.get('nombre', '')} {usuario_data.get('apellido', '')}".strip() or usuario_data.get("email", "Usuario")
    rol_display = usuario_data.get("rol", "Directivo")
    usuario_card = ft.Container(
        content=ft.Column(
            [
                ft.Text("Usuario activo", size=12, color=COLOR_SIDEBAR_TEXTO_SEC),
                ft.Container(height=4),
                ft.Text(nombre_display, size=16, weight="bold", color=COLOR_SIDEBAR_TEXTO),
                ft.Text(rol_display, size=13, color=COLOR_SIDEBAR_TEXTO_SEC),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.START,
            spacing=0,
        ),
        padding=ft.Padding.symmetric(horizontal=20, vertical=12),
    )

    # Cerrar sesión
    btn_logout = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.LOGOUT, color=COLOR_SIDEBAR_TEXTO, size=20),
                ft.Container(width=12),
                ft.Text("Cerrar Sesión", size=14, weight="w500", color=COLOR_SIDEBAR_TEXTO),
            ],
            alignment=ft.MainAxisAlignment.START,
        ),
        padding=ft.Padding.symmetric(vertical=14, horizontal=20),
        border_radius=10,
        on_click=lambda e: on_logout(),
    )

    sidebar = ft.Column(
        [
            ft.Container(height=24),
            ft.Row(
                [
                    ft.Icon(ft.Icons.SHIELD_ROUNDED, color=COLOR_PRIMARIO_CLARO, size=28),
                    ft.Container(width=10),
                    ft.Column(
                        [
                            ft.Text("Brigadas Escolares", size=16, weight="bold", color=COLOR_SIDEBAR_TEXTO),
                            ft.Text("Brigadas Ambientales", size=11, color=COLOR_SIDEBAR_TEXTO_SEC),
                        ],
                        spacing=0,
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            ft.Container(height=28),
            ft.Divider(height=1, color=ft.Colors.with_opacity(0.2, "white")),
            ft.Container(height=16),
        ]
        + nav_items
        + [
            ft.Container(expand=True),
            ft.Divider(height=1, color=ft.Colors.with_opacity(0.2, "white")),
            ft.Container(height=12),
            modo_toggle,
            ft.Container(height=16),
            usuario_card,
            ft.Container(height=12),
            btn_logout,
            ft.Container(height=24),
        ],
        spacing=0,
        expand=True,
    )

    return ft.Container(
        content=sidebar,
        width=260,
        bgcolor=COLOR_SIDEBAR,
        padding=0,
    )


def card_principal(content, padding=24):
    """Tarjeta blanca con sombra y bordes redondeados (estilo Figma)."""
    return ft.Container(
        content=content,
        bgcolor=COLOR_CARD,
        border_radius=RADIO_GRANDE,
        border=ft.Border.all(1, COLOR_BORDE),
        shadow=get_sombra_card(),
        padding=padding,
    )


def titulo_pagina(titulo, subtitulo, icono=None, accion=None):
    """Encabezado de página: X (opcional), título, subtítulo, y botón de acción a la derecha."""
    fila = [
        ft.Icon(ft.Icons.CLOSE, color=COLOR_TEXTO_SEC, size=22) if icono == "close" else ft.Container(width=0),
        ft.Container(width=16) if icono else None,
        ft.Column(
            [
                ft.Text(titulo, size=24, weight="bold", color=COLOR_TEXTO),
                ft.Text(subtitulo, size=14, color=COLOR_TEXTO_SEC),
            ],
            spacing=4,
            horizontal_alignment=ft.CrossAxisAlignment.START,
        ),
    ]
    if accion:
        fila.append(ft.Container(expand=True))
        fila.append(accion)
    return ft.Row(
        [c for c in fila if c is not None],
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )


def boton_primario(texto, icono=None, on_click=None, width=None):
    """Botón principal verde (brigadas ambientales)."""
    content = [ft.Text(texto, size=14, weight="w600", color="white")]
    if icono:
        content.insert(0, ft.Icon(icono, color="white", size=20))
        content.insert(1, ft.Container(width=8))
    return ft.FilledButton(
        content=ft.Row(content, alignment=ft.MainAxisAlignment.CENTER, spacing=0),
        style=ft.ButtonStyle(
            bgcolor=COLOR_PRIMARIO,
            color="white",
            shape=ft.RoundedRectangleBorder(radius=RADIO),
            padding=ft.Padding.symmetric(vertical=14, horizontal=24),
        ),
        on_click=on_click,
        width=width,
    )


def boton_secundario(texto, icono=None, on_click=None, width=None):
    """Botón outline verde."""
    content = [ft.Text(texto, size=14, weight="w500", color=COLOR_PRIMARIO)]
    if icono:
        content.insert(0, ft.Icon(icono, color=COLOR_PRIMARIO, size=20))
        content.insert(1, ft.Container(width=8))
    return ft.OutlinedButton(
        content=ft.Row(content, alignment=ft.MainAxisAlignment.CENTER, spacing=0),
        style=ft.ButtonStyle(
            side=ft.BorderSide(2, COLOR_PRIMARIO),
            shape=ft.RoundedRectangleBorder(radius=RADIO),
            padding=ft.Padding.symmetric(vertical=12, horizontal=24),
        ),
        on_click=on_click,
        width=width,
    )


