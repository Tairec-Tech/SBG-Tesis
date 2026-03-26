"""Demo 3 — Flip Card: cross-fade entre cara frontal y cara trasera al hover."""
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

W, H = 340, 340

def main(page: ft.Page):
    page.title = "Demo 3 — Flip Card"
    page.bgcolor = "#f0fdf4"
    page.window.maximized = True
    page.padding = 0

    cards = []
    for cfg in BRIGADAS:
        # ── CARA FRONTAL ──
        front = ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Icon(cfg["icono"], color="white", size=48),
                    width=100, height=100, border_radius=50,
                    gradient=ft.LinearGradient(colors=cfg["grad"],
                        begin=ft.Alignment.TOP_LEFT, end=ft.Alignment.BOTTOM_RIGHT),
                    alignment=ft.Alignment(0, 0),
                    shadow=[ft.BoxShadow(blur_radius=20, color=ft.Colors.with_opacity(0.4, cfg["color"]),
                        offset=ft.Offset(0, 8))],
                ),
                ft.Container(height=16),
                ft.Text(cfg["nombre"], size=24, weight="w800", color="#1e293b", text_align=ft.TextAlign.CENTER),
                ft.Container(height=4),
                ft.Text(cfg["sub"], size=14, weight="w500",
                        color=ft.Colors.with_opacity(0.7, cfg["color"]), text_align=ft.TextAlign.CENTER),
                ft.Container(height=20),
                ft.Row([
                    ft.Icon(ft.Icons.TOUCH_APP_ROUNDED, size=16, color="#94a3b8"),
                    ft.Text("Hover para ver más", size=12, color="#94a3b8", italic=True),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=6),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0,
               alignment=ft.MainAxisAlignment.CENTER),
            width=W, height=H,
            bgcolor=ft.Colors.with_opacity(0.92, "white"),
            border_radius=20,
            opacity=1.0,
            animate_opacity=ft.Animation(400, ft.AnimationCurve.EASE_IN_OUT),
        )

        # ── CARA TRASERA ──
        back = ft.Container(
            content=ft.Column([
                ft.Icon(cfg["icono"], size=48, color=ft.Colors.with_opacity(0.3, "white")),
                ft.Container(height=8),
                ft.Text(cfg["nombre"], size=22, weight="w700", color="white", text_align=ft.TextAlign.CENTER),
                ft.Container(height=16),
                ft.Divider(height=1, color=ft.Colors.with_opacity(0.3, "white")),
                ft.Container(height=12),
                ft.Text(cfg["desc"], size=15, color=ft.Colors.with_opacity(0.95, "white"),
                        text_align=ft.TextAlign.CENTER),
                ft.Container(height=24),
                ft.Container(
                    content=ft.Row([
                        ft.Text("Ingresar", size=15, weight="w700", color=cfg["color"]),
                        ft.Icon(ft.Icons.ARROW_FORWARD_ROUNDED, size=20, color=cfg["color"]),
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=6),
                    bgcolor="white", border_radius=12,
                    padding=ft.Padding(36, 12, 36, 12),
                    shadow=[ft.BoxShadow(blur_radius=12, color=ft.Colors.with_opacity(0.3, "black"),
                        offset=ft.Offset(0, 4))],
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0,
               alignment=ft.MainAxisAlignment.CENTER),
            width=W, height=H,
            gradient=ft.LinearGradient(colors=[cfg["grad"][0], cfg["color"]],
                begin=ft.Alignment.TOP_LEFT, end=ft.Alignment.BOTTOM_RIGHT),
            border_radius=20,
            padding=28,
            opacity=0.0,
            animate_opacity=ft.Animation(400, ft.AnimationCurve.EASE_IN_OUT),
        )

        card = ft.Container(
            content=ft.Stack([front, back]),
            width=W, height=H,
            border_radius=20,
            border=ft.Border.all(1.5, ft.Colors.with_opacity(0.15, "#cbd5e1")),
            shadow=[ft.BoxShadow(blur_radius=30, spread_radius=-4,
                color=ft.Colors.with_opacity(0.12, "#1e293b"), offset=ft.Offset(0, 12))],
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            ink=True,
            on_click=lambda _: None,
            scale=1.0,
            animate_scale=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
        )

        def _hover(card_ref, front_ref, back_ref, color):
            def handler(e):
                hov = e.data == "true"
                card_ref.scale = 1.06 if hov else 1.0
                front_ref.opacity = 0.0 if hov else 1.0
                back_ref.opacity = 1.0 if hov else 0.0
                card_ref.border = ft.Border.all(2.5 if hov else 1.5,
                    ft.Colors.with_opacity(0.7 if hov else 0.15, color if hov else "#cbd5e1"))
                card_ref.shadow = [ft.BoxShadow(
                    blur_radius=50 if hov else 30, spread_radius=4 if hov else -4,
                    color=ft.Colors.with_opacity(0.4 if hov else 0.12, color if hov else "#1e293b"),
                    offset=ft.Offset(0, 16 if hov else 12))]
                page.update()
            return handler

        card.on_hover = _hover(card, front, back, cfg["color"])
        cards.append(card)

    grid = ft.Column([
        ft.Row(cards[:2], alignment=ft.MainAxisAlignment.CENTER, spacing=28),
        ft.Row(cards[2:], alignment=ft.MainAxisAlignment.CENTER, spacing=28),
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=28)

    page.add(ft.Container(
        content=ft.Column([
            ft.Container(height=24),
            ft.Text("Demo 3 — Flip Card (Cross-Fade)", size=28, weight="w800", color="#1e293b", text_align=ft.TextAlign.CENTER),
            ft.Text("Hover → la tarjeta cambia a su cara trasera con la descripción", size=15, color="#64748b", text_align=ft.TextAlign.CENTER),
            ft.Container(height=24), grid,
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO),
        expand=True, bgcolor="#f0fdf4"))

ft.run(main)
