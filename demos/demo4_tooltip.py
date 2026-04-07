"""Demo 4 — Tooltip Elegante: tooltip nativo de Flet al hover, tarjeta limpia."""
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
    page.title = "Demo 4 — Tooltip Elegante"
    page.bgcolor = "#f0fdf4"
    page.window.maximized = True
    page.padding = 0

    cards = []
    for cfg in BRIGADAS:
        icon_circle = ft.Container(
            content=ft.Icon(cfg["icono"], color="white", size=44),
            width=90, height=90, border_radius=45,
            gradient=ft.LinearGradient(colors=cfg["grad"],
                begin=ft.Alignment.TOP_LEFT, end=ft.Alignment.BOTTOM_RIGHT),
            alignment=ft.Alignment(0, 0),
            shadow=[ft.BoxShadow(blur_radius=20, color=ft.Colors.with_opacity(0.4, cfg["color"]),
                offset=ft.Offset(0, 8))],
        )

        inner_card = ft.Container(
            content=ft.Column([
                ft.Container(height=5, border_radius=ft.BorderRadius(3, 3, 0, 0),
                    gradient=ft.LinearGradient(colors=[cfg["color"], cfg["grad"][0], cfg["color"]],
                        begin=ft.Alignment(-1, 0), end=ft.Alignment(1, 0))),
                ft.Container(
                    content=ft.Column([
                        icon_circle,
                        ft.Container(height=14),
                        ft.Text(cfg["nombre"], size=24, weight="w800", color="#1e293b", text_align=ft.TextAlign.CENTER),
                        ft.Container(height=4),
                        ft.Text(cfg["sub"], size=14, weight="w500",
                                color=ft.Colors.with_opacity(0.7, cfg["color"]), text_align=ft.TextAlign.CENTER),
                        ft.Container(height=14),
                        ft.Container(
                            content=ft.Row([
                                ft.Text("Ingresar", size=14, weight="w700", color="white"),
                                ft.Icon(ft.Icons.ARROW_FORWARD_ROUNDED, size=18, color="white"),
                            ], alignment=ft.MainAxisAlignment.CENTER, spacing=6),
                            bgcolor=cfg["color"], border_radius=10,
                            padding=ft.Padding(32, 10, 32, 10),
                        ),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
                    padding=ft.Padding(24, 20, 24, 20),
                ),
            ], spacing=0),
            bgcolor=ft.Colors.with_opacity(0.92, "white"),
            border_radius=20,
            border=ft.Border.all(1.5, ft.Colors.with_opacity(0.15, "#cbd5e1")),
            shadow=[ft.BoxShadow(blur_radius=30, spread_radius=-4,
                color=ft.Colors.with_opacity(0.12, "#1e293b"), offset=ft.Offset(0, 12))],
            width=340,
            ink=True,
            on_click=lambda _: None,
            scale=1.0,
            animate_scale=ft.Animation(250, ft.AnimationCurve.EASE_OUT),
        )

        def _hover(ref, color):
            def handler(e):
                hov = e.data == "true"
                ref.scale = 1.05 if hov else 1.0
                ref.border = ft.Border.all(2.5 if hov else 1.5,
                    ft.Colors.with_opacity(0.5 if hov else 0.15, color if hov else "#cbd5e1"))
                ref.shadow = [ft.BoxShadow(
                    blur_radius=50 if hov else 30, spread_radius=2 if hov else -4,
                    color=ft.Colors.with_opacity(0.3 if hov else 0.12, color if hov else "#1e293b"),
                    offset=ft.Offset(0, 16 if hov else 12))]
                page.update()
            return handler
        inner_card.on_hover = _hover(inner_card, cfg["color"])

        card = ft.Tooltip(
            message=f"{cfg['nombre']}\n{cfg['desc']}",
            content=inner_card,
            text_align=ft.TextAlign.CENTER,
            padding=20,
            border_radius=12,
            wait_duration=300,
            prefer_below=False,
        )
        cards.append(card)

    grid = ft.Column([
        ft.Row(cards[:2], alignment=ft.MainAxisAlignment.CENTER, spacing=28),
        ft.Row(cards[2:], alignment=ft.MainAxisAlignment.CENTER, spacing=28),
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=28)

    page.add(ft.Container(
        content=ft.Column([
            ft.Container(height=24),
            ft.Text("Demo 4 — Tooltip Elegante", size=28, weight="w800", color="#1e293b", text_align=ft.TextAlign.CENTER),
            ft.Text("Hover sobre tarjeta → tooltip con descripción (espere ~0.3s)", size=15, color="#64748b", text_align=ft.TextAlign.CENTER),
            ft.Container(height=24), grid,
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO),
        expand=True, bgcolor="#f0fdf4"))

ft.run(main)
