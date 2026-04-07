"""Demo 2 — Layout Horizontal: tarjetas anchas en 4 filas con hover dramático."""
import flet as ft

BRIGADAS = [
    {"nombre": "Gestión de Riesgo", "sub": "y Primeros Auxilios", "icono": ft.Icons.HEALTH_AND_SAFETY,
     "color": "#dc2626", "grad": ["#b91c1c", "#dc2626"],
     "desc": "Gestión de emergencias, evacuación, simulacros y primeros auxilios ante desastres naturales y situaciones de riesgo."},
    {"nombre": "Patrulla Escolar", "sub": "Seguridad Vial", "icono": ft.Icons.TRAFFIC,
     "color": "#ea580c", "grad": ["#c2410c", "#ea580c"],
     "desc": "Seguridad vial, control de tránsito peatonal, protección de la comunidad escolar en zonas de alto riesgo."},
    {"nombre": "Convivencia y Paz", "sub": "Prevención Integral", "icono": ft.Icons.HANDSHAKE,
     "color": "#64748b", "grad": ["#475569", "#64748b"],
     "desc": "Mediación de conflictos, cultura de paz, prevención de violencia escolar y promoción de valores de convivencia."},
    {"nombre": "Brigada Ecológica", "sub": "Medio Ambiente", "icono": ft.Icons.ECO,
     "color": "#059669", "grad": ["#047857", "#059669"],
     "desc": "Conservación ambiental, reciclaje, reforestación, cuidado del agua y educación ecológica en la comunidad."},
]

def main(page: ft.Page):
    page.title = "Demo 2 — Layout Horizontal"
    page.bgcolor = "#f0fdf4"
    page.window.maximized = True
    page.padding = 40

    cards = []
    for cfg in BRIGADAS:
        icon_circle = ft.Container(
            content=ft.Icon(cfg["icono"], color="white", size=36),
            width=70, height=70, border_radius=35,
            gradient=ft.LinearGradient(colors=cfg["grad"],
                begin=ft.Alignment.TOP_LEFT, end=ft.Alignment.BOTTOM_RIGHT),
            alignment=ft.Alignment(0, 0),
            shadow=[ft.BoxShadow(blur_radius=16, spread_radius=0,
                color=ft.Colors.with_opacity(0.4, cfg["color"]), offset=ft.Offset(0, 6))],
        )

        side_bar = ft.Container(
            width=6, border_radius=3, bgcolor=cfg["color"],
            animate=ft.Animation(250, ft.AnimationCurve.EASE_OUT),
        )

        card = ft.Container(
            content=ft.Row([
                side_bar,
                ft.Container(width=20),
                icon_circle,
                ft.Container(width=24),
                ft.Column([
                    ft.Text(cfg["nombre"], size=22, weight="w800", color="#1e293b"),
                    ft.Text(cfg["sub"], size=13, weight="w500",
                            color=ft.Colors.with_opacity(0.7, cfg["color"])),
                ], spacing=2),
                ft.Container(expand=True),
                ft.Container(
                    content=ft.Text(cfg["desc"], size=13, color="#475569"),
                    width=380, padding=ft.Padding(16, 12, 16, 12),
                    bgcolor=ft.Colors.with_opacity(0.06, cfg["color"]),
                    border_radius=12,
                    border=ft.Border.all(1, ft.Colors.with_opacity(0.15, cfg["color"])),
                ),
                ft.Container(width=24),
                ft.Container(
                    content=ft.Row([
                        ft.Text("Ingresar", size=14, weight="w700", color="white"),
                        ft.Icon(ft.Icons.ARROW_FORWARD_ROUNDED, size=18, color="white"),
                    ], spacing=6),
                    bgcolor=cfg["color"], border_radius=10,
                    padding=ft.Padding(24, 12, 24, 12),
                ),
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.Colors.with_opacity(0.92, "white"),
            border_radius=20,
            border=ft.Border.all(1.5, ft.Colors.with_opacity(0.15, "#cbd5e1")),
            shadow=[ft.BoxShadow(blur_radius=24, spread_radius=-4,
                color=ft.Colors.with_opacity(0.1, "#1e293b"), offset=ft.Offset(0, 8))],
            padding=ft.Padding(0, 20, 24, 20),
            ink=True,
            on_click=lambda _: None,
            scale=1.0,
            animate_scale=ft.Animation(250, ft.AnimationCurve.EASE_OUT),
            offset=ft.Offset(0, 0),
            animate_offset=ft.Animation(250, ft.AnimationCurve.EASE_OUT),
        )

        def _hover(card_ref, side_ref, color):
            def handler(e):
                hov = e.data == "true"
                card_ref.scale = 1.03 if hov else 1.0
                card_ref.offset = ft.Offset(-0.005, 0) if hov else ft.Offset(0, 0)
                card_ref.border = ft.Border.all(2.5 if hov else 1.5,
                    ft.Colors.with_opacity(0.5 if hov else 0.15, color if hov else "#cbd5e1"))
                card_ref.shadow = [ft.BoxShadow(
                    blur_radius=40 if hov else 24, spread_radius=2 if hov else -4,
                    color=ft.Colors.with_opacity(0.25 if hov else 0.1, color if hov else "#1e293b"),
                    offset=ft.Offset(0, 14 if hov else 8))]
                side_ref.width = 10 if hov else 6
                page.update()
            return handler

        card.on_hover = _hover(card, side_bar, cfg["color"])
        cards.append(card)

    page.add(ft.Column([
        ft.Text("Demo 2 — Layout Horizontal", size=28, weight="w800", color="#1e293b"),
        ft.Text("Pase el mouse → escala + borde + sombra con color de la brigada", size=15, color="#64748b"),
        ft.Container(height=16),
        *cards,
    ], spacing=16, scroll=ft.ScrollMode.AUTO, expand=True))

ft.run(main)
