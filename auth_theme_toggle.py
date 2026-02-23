import flet as ft
from theme import COLOR_PRIMARIO, COLOR_TEXTO, COLOR_CARD, COLOR_BORDE

def create_auth_theme_toggle(page: ft.Page) -> ft.Container:
    """Botón flotante (sol/luna) para cambiar el tema en las pantallas de Auth (Login, Registro, Recuperar)."""

    def on_toggle_theme(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
        
        actualizar_icono()
        page.update()

    btn_icon = ft.Icon(
        ft.Icons.LIGHT_MODE if page.theme_mode == ft.ThemeMode.DARK else ft.Icons.DARK_MODE,
        size=24,
        color=COLOR_TEXTO,
    )

    def actualizar_icono():
        btn_icon.icon = ft.Icons.LIGHT_MODE if page.theme_mode == ft.ThemeMode.DARK else ft.Icons.DARK_MODE
        btn_icon.color = COLOR_TEXTO

    toggle_btn = ft.Container(
        content=btn_icon,
        width=48,
        height=48,
        border_radius=24,
        bgcolor=COLOR_CARD,
        border=ft.Border.all(1, COLOR_BORDE),
        ink=True,
        on_click=on_toggle_theme,
        alignment=ft.Alignment(0, 0),
        shadow=ft.BoxShadow(
            blur_radius=8,
            spread_radius=0,
            color=ft.Colors.with_opacity(0.1, "black"),
            offset=ft.Offset(0, 4),
        ),
        top=24,
        right=24,
    )
    
    return toggle_btn
