"""Login — fondo animado, blobs difuminados, inputs con glow, tema verde (brigadas ambientales)."""

import asyncio
import json
import flet as ft

from database.crud_usuario import verificar_login_por_usuario_e_institucion, listar_instituciones, obtener_institucion_por_usuario
from util_log import log

from theme import (
    COLOR_TEXTO,
    COLOR_TEXTO_SEC,
    COLOR_BORDE,
    COLOR_PRIMARIO,
    COLOR_PRIMARIO_CLARO,
    COLOR_FONDO_VERDE,
    COLOR_VERDE_SUAVE,
)

# Colores de las esferas en los campos (pueden ser cualquiera)
GLOW_AZUL = "#60a5fa"
GLOW_MORADO = "#c084fc"
GLOW_VERDE = "#4ade80"

ANCHO_CELDA_ESFERA = 80


def _crear_blob(color: str, top: float, left: float, size: float) -> ft.Container:
    """
    Esfera grande de fondo con la misma difuminación que las esferas pequeñas de los inputs:
    foco pequeño + varias capas de BoxShadow (blur/spread) igual que en _input_con_titulo_y_glow.
    """
    # Misma técnica que el glow de los campos: foco pequeño + 3 sombras difuminadas (escaladas al tamaño)
    escala = max(size / 50, 1)
    foco = ft.Container(
        width=12,
        height=12,
        border_radius=6,
        bgcolor=ft.Colors.TRANSPARENT,
        shadow=[
            ft.BoxShadow(blur_radius=int(15 * escala), spread_radius=int(5 * escala), color=ft.Colors.with_opacity(0.9, color), offset=ft.Offset(0, 0)),
            ft.BoxShadow(blur_radius=int(30 * escala), spread_radius=int(10 * escala), color=ft.Colors.with_opacity(0.6, color), offset=ft.Offset(0, 0)),
            ft.BoxShadow(blur_radius=int(42 * escala), spread_radius=int(8 * escala), color=ft.Colors.with_opacity(0.3, color), offset=ft.Offset(0, 0)),
        ],
    )
    return ft.Container(
        content=foco,
        width=size,
        height=size,
        top=top,
        left=left,
        alignment=ft.Alignment(0.5, 0.5),
        clip_behavior=ft.ClipBehavior.NONE,
    )


def _crear_particula(color: str, top: float, left: float, size: float, blur: float = 0) -> ft.Container:
    """
    Micro-esfera decorativa con posición (solo para hijos directos del Stack).
    """
    c = ft.Container(
        width=size,
        height=size,
        border_radius=size / 2,
        bgcolor=ft.Colors.with_opacity(0.9, color),
        top=top,
        left=left,
    )
    if blur > 0:
        c.blur = ft.Blur(blur, blur)
    return c


def _crear_particula_visual(color: str, size: float, blur: float = 0) -> ft.Container:
    """
    Solo el círculo, sin top/left, para usar como content de FloatingElement.
    (En Flet, top/left solo son válidos en hijos directos de Stack.)
    """
    c = ft.Container(
        width=size,
        height=size,
        border_radius=size / 2,
        bgcolor=ft.Colors.with_opacity(0.9, color),
    )
    if blur > 0:
        c.blur = ft.Blur(blur, blur)
    return c


class FloatingElement(ft.Container):
    """Elemento que flota suavemente. step_top/step_left definen la dirección del movimiento."""

    def __init__(self, content, top, left, step_top=15, step_left=0, **kwargs):
        super().__init__(
            content=content,
            top=top,
            left=left,
            animate_position=ft.Animation(2000, ft.AnimationCurve.EASE_IN_OUT),
            **kwargs,
        )
        self.base_top = top
        self.base_left = left
        self.step_top = step_top
        self.step_left = step_left
        self.floating_phase = True  # True = suma, False = resta

    def animate_float(self):
        """Mueve en la dirección (step_top, step_left) y alterna."""
        if self.floating_phase:
            self.top = self.base_top + self.step_top
            self.left = self.base_left + self.step_left
        else:
            self.top = self.base_top - self.step_top
            self.left = self.base_left - self.step_left
        self.floating_phase = not self.floating_phase


def _input_con_titulo_y_glow(titulo: str, campo: ft.Control, color_glow: str, is_dropdown: bool = False) -> ft.Column:
    """Título arriba y debajo el input con glow (triple capa). Si is_dropdown, mismo tamaño que los campos (altura 56)."""
    if is_dropdown:
        # Mismo tamaño que los TextField: contenedor 56px con el dropdown centrado
        contenido_interno = ft.Container(content=campo, height=56, alignment=ft.Alignment(-1, 0), expand=True)
    else:
        foco_de_luz = ft.Container(
            width=10,
            height=10,
            bgcolor=ft.Colors.TRANSPARENT,
            shadow=[
                ft.BoxShadow(blur_radius=15, spread_radius=5, color=ft.Colors.with_opacity(0.9, color_glow), offset=ft.Offset(0, 0)),
                ft.BoxShadow(blur_radius=30, spread_radius=10, color=ft.Colors.with_opacity(0.6, color_glow), offset=ft.Offset(0, 0)),
                ft.BoxShadow(blur_radius=42, spread_radius=8, color=ft.Colors.with_opacity(0.3, color_glow), offset=ft.Offset(0, 0)),
            ],
        )
        celda_glow = ft.Container(
            content=foco_de_luz,
            width=60,
            height=50,
            alignment=ft.Alignment(0, 0),
            clip_behavior=ft.ClipBehavior.NONE,
        )
        contenido_interno = ft.Row(
            [celda_glow, ft.Container(content=campo, expand=True)],
            spacing=0,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
    input_container = ft.Container(
        content=contenido_interno,
        bgcolor="white",
        border_radius=16,
        border=ft.Border.all(1, "#E2E8F0"),
        padding=ft.Padding.only(left=0 if not is_dropdown else 15, right=15),
        height=56,
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        shadow=ft.BoxShadow(
            blur_radius=10,
            spread_radius=0,
            color=ft.Colors.with_opacity(0.05, "black"),
            offset=ft.Offset(0, 4),
        ),
    )
    return ft.Column(
        [
            ft.Text(titulo, size=13, weight="w600", color=COLOR_TEXTO),
            input_container,
        ],
        spacing=6,
    )


def build(page: ft.Page, on_login_success, on_go_register, on_go_recovery) -> ft.Control:
    # Lista de instituciones para el dropdown
    try:
        inst_opciones = [ft.dropdown.Option(str(i["idInstitucion"]), i["nombre_institucion"]) for i in listar_instituciones()]
    except Exception:
        inst_opciones = []

    dropdown_institucion = ft.Dropdown(
        hint_text="Seleccione su institución",
        options=inst_opciones,
        border=ft.InputBorder.NONE,
        text_style=ft.TextStyle(size=14, color="#334155"),
        hint_style=ft.TextStyle(size=14, color="#94A3B8"),
        content_padding=ft.Padding(0, 16),
        dense=True,
    )
    campo_usuario = ft.TextField(
        hint_text="Usuario",
        hint_style=ft.TextStyle(size=14, color="#94A3B8"),
        border=ft.InputBorder.NONE,
        text_style=ft.TextStyle(size=14, color="#334155"),
        cursor_color=COLOR_PRIMARIO,
    )
    campo_password = ft.TextField(
        hint_text="Ingrese su contraseña",
        password=True,
        can_reveal_password=True,
        hint_style=ft.TextStyle(size=14, color="#94A3B8"),
        border=ft.InputBorder.NONE,
        text_style=ft.TextStyle(size=14, color="#334155"),
        cursor_color=COLOR_PRIMARIO,
    )
    checkbox_profesor = ft.Checkbox(
        label="Soy profesor",
        value=False,
        fill_color=COLOR_PRIMARIO,
    )

    # Diálogo de error para login (modal, siempre visible)
    texto_error_login = ft.Text("", size=14)
    dialogo_error_login = ft.AlertDialog(
        modal=True,
        title=ft.Row([ft.Icon(ft.Icons.ERROR_OUTLINE, color="#ef4444"), ft.Text("Error")]),
        content=texto_error_login,
        actions=[ft.TextButton("Entendido", on_click=lambda e: _cerrar_error_login())],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def _cerrar_error_login():
        dialogo_error_login.open = False
        page.update()

    def _mostrar_error_login(mensaje: str):
        texto_error_login.value = mensaje
        dialogo_error_login.open = True
        page.update()

    if dialogo_error_login not in (page.overlay or []):
        page.overlay.append(dialogo_error_login)

    # Botón principal (se define antes de do_login para poder modificarlo)
    boton_iniciar_content = ft.Row(
        [
            ft.Text("Iniciar Sesión", size=15, weight="w600"),
            ft.Icon(ft.Icons.ARROW_FORWARD_ROUNDED, size=18),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
    )
    boton_iniciar = ft.FilledButton(
        content=boton_iniciar_content,
        style=ft.ButtonStyle(
            color="white",
            bgcolor=COLOR_PRIMARIO,
            shape=ft.RoundedRectangleBorder(radius=12),
            padding=ft.Padding.symmetric(vertical=18),
            elevation=8,
            shadow_color=ft.Colors.with_opacity(0.5, COLOR_PRIMARIO),
        ),
        width=320,
    )

    async def do_login(e):
        log("1. do_login: inicio")
        inst_id = (dropdown_institucion.value or "").strip()
        usuario_str = (campo_usuario.value or "").strip()
        password = (campo_password.value or "").strip()
        es_profesor = checkbox_profesor.value or False

        # Validar campos (mostrar en modal)
        if not inst_id:
            _mostrar_error_login("Seleccione su institución.")
            return
        if not usuario_str:
            campo_usuario.error_text = "Campo requerido"
            _mostrar_error_login("Ingrese su usuario.")
            page.update()
            return
        campo_usuario.error_text = None
        if not password:
            campo_password.error_text = "Campo requerido"
            _mostrar_error_login("Ingrese su contraseña.")
            page.update()
            return
        campo_password.error_text = None

        log("3. do_login: verificando...")
        boton_iniciar.disabled = True
        boton_iniciar.content = ft.ProgressRing(width=20, height=20, stroke_width=2, color="white")
        page.update()

        try:
            usuario = verificar_login_por_usuario_e_institucion(
                int(inst_id),
                usuario_str,
                password,
                es_profesor=es_profesor,
            )
            log(f"4. do_login: usuario={'sí' if usuario else 'no'}")
            if usuario:
                inst = obtener_institucion_por_usuario(usuario["idUsuario"])
                datos = {
                    "id": usuario["idUsuario"],
                    "nombre": usuario["nombre"],
                    "apellido": usuario["apellido"],
                    "email": usuario.get("email"),
                    "usuario": usuario.get("usuario"),
                    "rol": usuario["rol"],
                    "institucion_id": inst.get("idInstitucion") if inst else None,
                    "institucion_nombre": inst.get("nombre_institucion", "Institución") if inst else "Institución",
                    "institucion_logo_ruta": inst.get("logo_ruta") if inst else None,
                }
                prefs = ft.SharedPreferences()
                await prefs.set("usuario_actual", json.dumps(datos))
                if getattr(page, "data", None) is None:
                    page.data = {}
                page.data["usuario_actual"] = datos
                on_login_success()
                page.update()
            else:
                if es_profesor:
                    _mostrar_error_login("No hay un profesor con ese usuario en esta institución, o la contraseña es incorrecta.")
                else:
                    _mostrar_error_login("No hay un directivo/coordinador con ese usuario en esta institución, o la contraseña es incorrecta.")
        except Exception as err:
            log(f"ERROR do_login: {err}")
            _mostrar_error_login(f"Error de conexión: {err}")
        finally:
            boton_iniciar.disabled = False
            boton_iniciar.content = boton_iniciar_content
            page.update()

    boton_iniciar.on_click = lambda e: page.run_task(do_login, e)

    # Header: icono de reciclaje con anillo y sombra 3D (paleta verde)
    header = ft.Column(
        [
            ft.Container(
                content=ft.Icon(ft.Icons.RECYCLING, size=42, color="white"),
                width=80,
                height=80,
                border_radius=40,
                gradient=ft.LinearGradient(
                    colors=[COLOR_PRIMARIO_CLARO, COLOR_PRIMARIO],
                    begin=ft.Alignment.TOP_LEFT,
                    end=ft.Alignment.BOTTOM_RIGHT,
                ),
                shadow=[
                    ft.BoxShadow(blur_radius=20, color=ft.Colors.with_opacity(0.4, COLOR_PRIMARIO), offset=ft.Offset(0, 10)),
                    ft.BoxShadow(color="white", spread_radius=2, blur_radius=0, offset=ft.Offset(0, 0)),
                ],
                alignment=ft.Alignment.CENTER,
            ),
            ft.Container(height=20),
            ft.Text("Sistema de Brigadas", size=28, weight="w800", color=COLOR_TEXTO, font_family="Roboto"),
            ft.Text("Municipio Maracaibo", size=16, weight="w500", color=COLOR_TEXTO_SEC),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0,
    )

    # Tarjeta estilo Figma: glassmorphism, sombras de color, mucho aire (paleta verde)
    login_card = ft.Container(
        content=ft.Column(
            [
                ft.Container(height=10),
                _input_con_titulo_y_glow("Institución", dropdown_institucion, GLOW_AZUL, is_dropdown=True),
                ft.Container(height=20),
                _input_con_titulo_y_glow("Usuario", campo_usuario, GLOW_MORADO),
                ft.Container(height=20),
                _input_con_titulo_y_glow("Contraseña", campo_password, GLOW_VERDE),
                ft.Container(height=12),
                checkbox_profesor,
                ft.Container(height=20),
                boton_iniciar,
                ft.Container(height=20),
                ft.Container(
                    content=ft.Text("¿Olvidó su contraseña?", size=13, weight="w500", color=COLOR_PRIMARIO),
                    alignment=ft.Alignment.CENTER,
                    on_click=lambda e: on_go_recovery(),
                ),
                ft.Divider(height=40, color=COLOR_VERDE_SUAVE, thickness=1),
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text("¿No tienes cuenta?", size=13, color=COLOR_TEXTO_SEC),
                            ft.Text("Registrar Institución", size=13, weight="bold", color=COLOR_PRIMARIO),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    padding=12,
                    border_radius=12,
                    bgcolor="white",
                    border=ft.Border.all(1, COLOR_BORDE),
                    on_click=lambda e: on_go_register(),
                    shadow=[
                        ft.BoxShadow(
                            blur_radius=12,
                            spread_radius=-2,
                            color=ft.Colors.with_opacity(0.12, COLOR_TEXTO),
                            offset=ft.Offset(0, 4),
                        ),
                    ],
                ),
            ],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=ft.Colors.with_opacity(0.85, "white"),
        blur=ft.Blur(15, 15),
        padding=ft.Padding.all(40),
        border_radius=35,
        border=ft.Border.all(1.5, "white"),
        shadow=[
            ft.BoxShadow(
                blur_radius=60,
                spread_radius=-8,
                color=ft.Colors.with_opacity(0.2, COLOR_TEXTO),
                offset=ft.Offset(0, 28),
            ),
            ft.BoxShadow(
                blur_radius=16,
                spread_radius=0,
                color=ft.Colors.with_opacity(0.08, COLOR_TEXTO),
                offset=ft.Offset(0, 12),
            ),
        ],
        width=420,
    )

    # Blobs de fondo (misma difuminación que los glows: radial centro → transparente)
    background_blobs = [
        _crear_blob(GLOW_AZUL, 50, -50, 300),
        _crear_blob("#FCD34D", 100, 1100, 250),
        _crear_blob(GLOW_VERDE, 600, 100, 300),
        _crear_blob(GLOW_MORADO, 500, 1150, 250),
        _crear_blob(GLOW_MORADO, 700, 1100, 280),
    ]

    # Tonalidades de verde para las pelotitas (mismo tamaño, todas se mueven en distintas direcciones)
    VERDES_PARTICULAS = [
        "#065f46",  # Emerald-800
        "#047857",  # Emerald-700
        COLOR_PRIMARIO,
        COLOR_PRIMARIO_CLARO,
        "#34d399",  # Emerald-400
        "#6ee7b7",  # Emerald-300
        "#86efac",  # Green-300
        "#a7f3d0",  # Emerald-200
        COLOR_VERDE_SUAVE,
    ]
    TAMANO_PARTICULA = 14

    # Posiciones y dirección (step_top, step_left) para cada partícula
    config_particulas = [
        (200, 250, 12, 0),    # arriba/abajo
        (120, 150, 0, 14),    # izq/der
        (80, 1100, -10, 8),   # diagonal
        (150, 1250, 8, -10),
        (350, 350, -8, -8),
        (500, 1000, 10, 12),
        (650, 200, -12, 6),
        (700, 900, 6, -12),
        (600, 1300, -6, 10),
    ]
    particulas_animadas = []
    for i, (top, left, st, sl) in enumerate(config_particulas):
        color = VERDES_PARTICULAS[i % len(VERDES_PARTICULAS)]
        particulas_animadas.append(
            FloatingElement(
                content=_crear_particula_visual(color, TAMANO_PARTICULA, blur=0),
                top=top,
                left=left,
                step_top=st,
                step_left=sl,
            )
        )

    # Casa ~3x más grande y bien a la derecha; color verde
    icon_house = FloatingElement(
        content=ft.Icon(
            ft.Icons.HOUSE_ROUNDED,
            size=240,
            color=ft.Colors.with_opacity(0.2, COLOR_PRIMARIO),
        ),
        top=80,
        left=1150,
    )
    icon_people = FloatingElement(
        content=ft.Icon(
            ft.Icons.GROUPS_ROUNDED,
            size=60,
            color=ft.Colors.with_opacity(0.2, GLOW_MORADO),
        ),
        top=600,
        left=1100,
    )

    async def animate_background():
        while True:
            icon_house.animate_float()
            icon_people.animate_float()
            for p in particulas_animadas:
                p.animate_float()
            if page.controls:
                page.update()
            await asyncio.sleep(2.1)

    page.run_task(animate_background)

    return ft.Stack(
        [
            ft.Container(expand=True, bgcolor=COLOR_FONDO_VERDE),
            *background_blobs,
            icon_house,
            icon_people,
            *particulas_animadas,
            ft.Container(
                content=ft.Column(
                    [
                        ft.Container(height=50),
                        header,
                        ft.Container(height=30),
                        login_card,
                        ft.Container(height=40),
                        ft.Text("© 2026 Sistema de Brigadas Escolares", size=11, color=COLOR_TEXTO_SEC),
                        ft.Container(height=20),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.AUTO,
                ),
                alignment=ft.Alignment.CENTER,
                expand=True,
            ),
        ],
        expand=True,
    )
