import asyncio
import random
import flet as ft

from views import build_views_content

def main(page: ft.Page):
    page.title = "Sistema de Brigadas Escolares"
    page.bgcolor = "#f5f0e8"  # Blanco hueso
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 24
    # Abrir ventana maximizada (resolución máxima disponible)
    page.window.maximized = True
    page.update()

    animacion_entrada = ft.Animation(
        duration=ft.Duration(milliseconds=600),
        curve=ft.AnimationCurve.EASE_OUT_BACK,
    )

    # --- Animación inicial: bloques SGB que se construyen solos ---
    size_bloque = 14
    gap_bloque = 4
    duracion_anim = 1200
    c_s, c_g, c_b = "#2563eb", "#3b82f6", "#1d4ed8"
    partes_sgb = [
        (0, 0, c_s), (1, 0, c_s), (2, 0, c_s), (0, 1, c_s), (0, 2, c_s), (1, 2, c_s), (2, 2, c_s), (2, 3, c_s), (0, 4, c_s), (1, 4, c_s), (2, 4, c_s),
        (4, 0, c_g), (5, 0, c_g), (6, 0, c_g), (4, 1, c_g), (4, 2, c_g), (5, 2, c_g), (6, 2, c_g), (4, 3, c_g), (6, 3, c_g), (4, 4, c_g), (5, 4, c_g), (6, 4, c_g),
        (8, 0, c_b), (9, 0, c_b), (10, 0, c_b), (8, 1, c_b), (10, 1, c_b), (8, 2, c_b), (9, 2, c_b), (10, 2, c_b), (8, 3, c_b), (10, 3, c_b), (8, 4, c_b), (9, 4, c_b), (10, 4, c_b),
    ]
    ancho_canvas = 11 * (size_bloque + gap_bloque)
    alto_canvas = 5 * (size_bloque + gap_bloque)
    bloques_containers = [
        ft.Container(animate=duracion_anim, animate_position=duracion_anim, animate_rotation=duracion_anim)
        for _ in partes_sgb
    ]
    canvas_sgb = ft.Stack(
        controls=bloques_containers,
        width=ancho_canvas,
        height=alto_canvas,
        animate_scale=duracion_anim,
        animate_opacity=duracion_anim,
    )

    def dispersar_bloques():
        random.seed()
        for i in range(len(partes_sgb)):
            c = canvas_sgb.controls[i]
            tam = random.randrange(size_bloque - 2, size_bloque + 10)
            c.left = random.randrange(0, max(1, ancho_canvas - tam))
            c.top = random.randrange(0, max(1, alto_canvas - tam))
            c.bgcolor = partes_sgb[i][2]
            c.width, c.height = tam, tam
            c.border_radius = random.randrange(2, 8)
            c.rotate = random.randrange(-30, 30) * 3.14159 / 180
        canvas_sgb.scale = 0.85
        canvas_sgb.opacity = 0.9

    def ensamblar_bloques():
        for i, (col, fila, color) in enumerate(partes_sgb):
            c = canvas_sgb.controls[i]
            c.left = col * (size_bloque + gap_bloque)
            c.top = fila * (size_bloque + gap_bloque)
            c.bgcolor = color
            c.width = c.height = size_bloque
            c.border_radius = 4
            c.rotate = 0
        canvas_sgb.scale = 1
        canvas_sgb.opacity = 1

    texto_subtitulo_intro = ft.Text("Sistema de Brigadas Escolares", size=15, color="#64748b", text_align=ft.TextAlign.CENTER)
    texto_subtitulo_intro_container = ft.Container(
        content=texto_subtitulo_intro,
        opacity=0,
        animate_opacity=ft.Animation(duration=ft.Duration(milliseconds=500), curve=ft.AnimationCurve.EASE_OUT),
    )
    intro_overlay = ft.Container(
        content=ft.Column(
            [
                ft.Container(content=canvas_sgb, scale=2.2),
                ft.Container(height=56),
                texto_subtitulo_intro_container,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=0,
        ),
        expand=True,
        bgcolor="#f5f0e8",
        alignment=ft.Alignment.CENTER,
        animate_opacity=ft.Animation(duration=ft.Duration(milliseconds=500), curve=ft.AnimationCurve.EASE_OUT),
    )

    async def animacion_inicio_automatica():
        await asyncio.sleep(0.5)
        ensamblar_bloques()
        page.update()
        await asyncio.sleep(1.3)
        texto_subtitulo_intro_container.opacity = 1
        page.update()
        await asyncio.sleep(1.2)
        intro_overlay.opacity = 0
        page.update()
        await asyncio.sleep(0.55)
        intro_overlay.visible = False
        login_card.opacity = 1
        login_card.offset = ft.Offset(0, 0)
        page.update()

    # --- Header / Branding (arriba del todo) ---
    logo_escudo = ft.Container(
        content=ft.Icon(
            ft.Icons.SHIELD_ROUNDED,
            size=56,
            color="#2563eb",
        ),
        width=88,
        height=88,
        border_radius=44,
        bgcolor="#ffffff",
        border=ft.Border.all(2, "#e2e8f0"),
        alignment=ft.Alignment.CENTER,
        shadow=ft.BoxShadow(
            blur_radius=12,
            spread_radius=0,
            color=ft.Colors.with_opacity(0.08, "black"),
            offset=ft.Offset(0, 4),
        ),
    )

    titulo_principal = ft.Text(
        "Sistema de Brigadas Escolares",
        size=26,
        weight="bold",
        color="#1e293b",
        text_align=ft.TextAlign.CENTER,
    )
    subtitulo_1 = ft.Text(
        "Plataforma Digital para Coordinación de Brigadas",
        size=14,
        color="#64748b",
        text_align=ft.TextAlign.CENTER,
    )
    subtitulo_2 = ft.Text(
        "Municipio Maracaibo",
        size=12,
        color="#94a3b8",
        text_align=ft.TextAlign.CENTER,
    )

    header = ft.Column(
        [
            logo_escudo,
            ft.Container(height=16),
            titulo_principal,
            ft.Container(height=6),
            subtitulo_1,
            ft.Container(height=4),
            subtitulo_2,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0,
    )

    # --- Campos de la tarjeta ---
    estilo_campo = dict(
        border_color="#cbd5e1",
        focused_border_color="#2563eb",
        cursor_color="#2563eb",
        text_style=ft.TextStyle(color="#1e293b"),
        label_style=ft.TextStyle(color="#475569"),
        width=320,
        border_radius=12,
    )

    campo_institucion = ft.TextField(
        label="Institución Educativa",
        hint_text="Nombre de la institución",
        prefix_icon=ft.Icons.SCHOOL_OUTLINED,
        **estilo_campo,
    )
    campo_usuario = ft.TextField(
        label="Usuario",
        hint_text="Ingrese su usuario",
        prefix_icon=ft.Icons.PERSON_OUTLINED,
        **estilo_campo,
    )
    campo_password = ft.TextField(
        label="Contraseña",
        hint_text="Ingrese su contraseña",
        prefix_icon=ft.Icons.LOCK_OUTLINED,
        password=True,
        can_reveal_password=True,
        **estilo_campo,
    )

    # Botón Iniciar Sesión (primario) — al hacer clic va a la sección de vistas
    boton_iniciar = ft.Button(
        content=ft.Text("Iniciar Sesión", size=16, weight="w600"),
        style=ft.ButtonStyle(
            color="white",
            bgcolor="#2563eb",
            overlay_color=ft.Colors.with_opacity(0.2, "white"),
            shape=ft.RoundedRectangleBorder(radius=12),
            padding=ft.Padding.symmetric(vertical=16, horizontal=24),
            elevation=4,
            shadow_color=ft.Colors.with_opacity(0.35, "#1e3a5f"),
        ),
        width=320,
        height=52,
    )

    # Enlace ¿Olvidó su contraseña?
    enlace_olvido = ft.TextButton(
        content=ft.Text("¿Olvidó su contraseña?", color="#2563eb", size=14),
    )

    # Divisor con "o"
    divisor = ft.Row(
        [
            ft.Container(expand=True, height=1, bgcolor="#e2e8f0"),
            ft.Container(
                content=ft.Text(" o ", size=13, color="#94a3b8"),
                padding=ft.Padding.symmetric(horizontal=12),
            ),
            ft.Container(expand=True, height=1, bgcolor="#e2e8f0"),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # Botón Registrar Nueva Institución (secundario / outline)
    boton_registrar = ft.OutlinedButton(
        content=ft.Text("Registrar Nueva Institución", size=14, weight="w500", color="#2563eb"),
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=12),
            padding=ft.Padding.symmetric(vertical=14, horizontal=24),
            side=ft.BorderSide(2, "#2563eb"),
        ),
        width=320,
        height=48,
    )

    # --- Tarjeta de login ---
    login_card = ft.Container(
        content=ft.Column(
            [
                campo_institucion,
                ft.Container(height=16),
                campo_usuario,
                ft.Container(height=16),
                campo_password,
                ft.Container(height=24),
                boton_iniciar,
                ft.Container(height=12),
                enlace_olvido,
                ft.Container(height=20),
                divisor,
                ft.Container(height=20),
                boton_registrar,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
        ),
        bgcolor="#ffffff",
        width=400,
        padding=ft.Padding.symmetric(vertical=40, horizontal=44),
        border_radius=24,
        shadow=ft.BoxShadow(
            blur_radius=32,
            spread_radius=-4,
            color=ft.Colors.with_opacity(0.18, "black"),
            offset=ft.Offset(0, 12),
        ),
        border=ft.Border.all(1, "#e2e8f0"),
        animate_opacity=animacion_entrada,
        animate_offset=animacion_entrada,
        opacity=0,
        offset=ft.Offset(0, 20),
    )

    # --- Footer ---
    footer = ft.Text(
        "© 2026 Sistema de Brigadas Escolares - Municipio Maracaibo",
        size=12,
        color="#94a3b8",
        text_align=ft.TextAlign.CENTER,
    )

    # --- Botón de ayuda (esquina inferior derecha) ---
    boton_ayuda = ft.Container(
        content=ft.IconButton(
            icon=ft.Icons.HELP_OUTLINED,
            icon_color="#64748b",
            icon_size=24,
            style=ft.ButtonStyle(
                bgcolor="#ffffff",
                shape=ft.CircleBorder(),
                elevation=2,
                shadow_color=ft.Colors.with_opacity(0.15, "black"),
            ),
        ),
        right=24,
        bottom=24,
    )

    # --- Vista de login (pantalla inicial) ---
    contenido_central = ft.Column(
        [
            header,
            ft.Container(height=32),
            login_card,
            ft.Container(height=40),
            footer,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0,
    )
    vista_login = ft.Stack(
        [
            contenido_central,
            boton_ayuda,
        ],
        expand=True,
        alignment=ft.Alignment.CENTER,
    )

    # --- Vista principal (views: HIPO — menú lateral + área de contenido) ---
    vista_principal = ft.Container(expand=True, visible=False)

    def cerrar_sesion():
        vista_login.visible = True
        vista_principal.visible = False
        page.update()

    vista_principal.content = build_views_content(page, on_logout=cerrar_sesion)

    def ir_a_views(_):
        vista_login.visible = False
        vista_principal.visible = True
        page.update()

    boton_iniciar.on_click = ir_a_views

    async def animar_entrada():
        await asyncio.sleep(0.05)
        login_card.opacity = 1
        login_card.offset = ft.Offset(0, 0)
        page.update()

    # Contenedor principal: login, views e intro (intro encima al inicio)
    page.add(
        ft.Stack(
            [
                vista_login,
                vista_principal,
                intro_overlay,
            ],
            expand=True,
        ),
    )
    dispersar_bloques()
    page.run_task(animacion_inicio_automatica)


if __name__ == "__main__":
    ft.run(main)
