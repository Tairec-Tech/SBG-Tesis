"""Registro de Nueva Institución — Mismo fondo que Login (sin casa), glassmorphism, inputs con glow, paleta verde."""

import asyncio
import os
import re
import shutil
import flet as ft

from auth_theme_toggle import create_auth_theme_toggle

try:
    from tkinter import Tk, filedialog
    _TK_AVAILABLE = True
except Exception:
    _TK_AVAILABLE = False

from database.crud_usuario import (
    crear_institucion,
    crear_usuario,
    email_ya_existe,
    usuario_ya_existe,
    listar_instituciones,
    actualizar_logo_institucion,
)
try:
    from mysql.connector import errors as mysql_errors
except ImportError:
    mysql_errors = None

# Carpeta para logos de instituciones (relativa al proyecto)
DIR_LOGOS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploads", "logos")


def _es_email_valido(email: str) -> bool:
    """Valida que el email tenga formato básico: algo@algo.algo"""
    if not email:
        return False
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email))
from theme import (
    COLOR_PRIMARIO,
    COLOR_PRIMARIO_CLARO,
    COLOR_TEXTO,
    COLOR_TEXTO_SEC,
    COLOR_FONDO_VERDE,
    COLOR_VERDE_SUAVE,
    COLOR_BORDE,
    COLOR_CARD,
)

# Mismos colores de glow que el login (azul/morado/verde por sección)
GLOW_AZUL = "#60a5fa"
GLOW_MORADO = "#c084fc"
GLOW_VERDE = "#4ade80"


def _crear_blob(color: str, top: float, left: float, size: float) -> ft.Container:
    """Esfera grande de fondo (misma técnica que login)."""
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


def _crear_particula_visual(color: str, size: float, blur: float = 0) -> ft.Container:
    """Círculo sin top/left para usar como content de FloatingElement."""
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
    """Elemento que flota en una dirección (step_top, step_left)."""

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
        self.floating_phase = True

    def animate_float(self):
        if self.floating_phase:
            self.top = self.base_top + self.step_top
            self.left = self.base_left + self.step_left
        else:
            self.top = self.base_top - self.step_top
            self.left = self.base_left - self.step_left
        self.floating_phase = not self.floating_phase


def _input_con_titulo_y_glow(titulo: str, campo: ft.Control, color_glow: str, is_dropdown: bool = False) -> ft.Column:
    """Input o dropdown con glow (igual que login). Si es dropdown, no se pone el glow para no tapar la flecha."""
    
    # Asegurar que el campo se adapte al tema oscuro
    campo.color = COLOR_TEXTO
    if hasattr(campo, 'dropdown_color'):
        campo.dropdown_color = COLOR_CARD
    if isinstance(campo, ft.Dropdown):
        # Asegurar icono de dropdown visible
        campo.icon_content = ft.Icon(ft.Icons.ARROW_DROP_DOWN, color=COLOR_TEXTO_SEC)

    if is_dropdown:
        contenido_interno = campo
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
        contenido_interno = ft.Row(
            [
                ft.Container(content=foco_de_luz, width=60, height=50, alignment=ft.Alignment(0, 0), clip_behavior=ft.ClipBehavior.NONE),
                ft.Container(content=campo, expand=True),
            ],
            spacing=0,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
    input_container = ft.Container(
        content=contenido_interno,
        bgcolor=COLOR_CARD,
        border_radius=16,
        border=ft.Border.all(1, COLOR_BORDE),
        padding=ft.Padding.only(left=0 if not is_dropdown else 15, right=15),
        height=56,
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        shadow=ft.BoxShadow(blur_radius=10, spread_radius=0, color=ft.Colors.with_opacity(0.05, "black"), offset=ft.Offset(0, 4)),
    )
    return ft.Column(
        [
            ft.Text(titulo, size=13, weight="w600", color=COLOR_TEXTO),
            input_container,
        ],
        spacing=6,
    )


def _titulo_seccion(texto: str, icono) -> ft.Container:
    """Título de sección con icono en verde."""
    return ft.Container(
        content=ft.Row(
            [
                ft.Icon(icono, size=20, color=COLOR_PRIMARIO),
                ft.Text(texto, size=16, weight="bold", color=COLOR_TEXTO),
            ],
            spacing=10,
        ),
        padding=ft.Padding.only(top=10, bottom=10),
    )


def build(page: ft.Page, on_back_to_login) -> ft.Control:
    # --- Diálogo de error (para que siempre se vea el mensaje) ---
    texto_error = ft.Text("", size=14)
    dialogo_error = ft.AlertDialog(
        modal=True,
        title=ft.Row([ft.Icon(ft.Icons.ERROR_OUTLINE, color="#ef4444"), ft.Text("Error de validación")]),
        content=texto_error,
        actions=[ft.TextButton("Entendido", on_click=lambda e: _cerrar_error())],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def _cerrar_error():
        dialogo_error.open = False
        page.update()

    def _mostrar_error(mensaje: str):
        texto_error.value = mensaje
        dialogo_error.open = True
        page.update()

    if dialogo_error not in (page.overlay or []):
        page.overlay.append(dialogo_error)

    # --- Tipo de cuenta (se actualiza después de crear formularios) ---
    tipo_cuenta = {"value": "admin"}

    # --- Campos (admin) ---
    nom_inst = ft.TextField(
        hint_text="Nombre de la institución",
        hint_style=ft.TextStyle(size=14, color=COLOR_TEXTO_SEC),
        border=ft.InputBorder.NONE,
        text_style=ft.TextStyle(size=14, color=COLOR_TEXTO),
        cursor_color=COLOR_PRIMARIO,
    )
    tel_inst = ft.TextField(
        hint_text="Teléfono oficial",
        hint_style=ft.TextStyle(size=14, color=COLOR_TEXTO_SEC),
        border=ft.InputBorder.NONE,
        text_style=ft.TextStyle(size=14, color=COLOR_TEXTO),
        cursor_color=COLOR_PRIMARIO,
    )
    direccion = ft.TextField(
        hint_text="Dirección completa",
        hint_style=ft.TextStyle(size=14, color=COLOR_TEXTO_SEC),
        border=ft.InputBorder.NONE,
        text_style=ft.TextStyle(size=14, color=COLOR_TEXTO),
        cursor_color=COLOR_PRIMARIO,
    )
    nivel = ft.Dropdown(
        hint_text="Seleccione nivel",
        hint_style=ft.TextStyle(size=14, color=COLOR_TEXTO_SEC),
        border=ft.InputBorder.NONE,
        text_style=ft.TextStyle(size=14, color=COLOR_TEXTO),
        options=[
            ft.dropdown.Option("Primaria"),
            ft.dropdown.Option("Secundaria"),
            ft.dropdown.Option("Ambos"),
        ],
    )

    opciones_cdce = [
        ft.dropdown.Option("CDCE - Antonio Borjas Romero"),
        ft.dropdown.Option("CDCE - Coquivacoa"),
        ft.dropdown.Option("CDCE - Cristo de Aranza"),
        ft.dropdown.Option("CDCE - Francisco Eugenio Bustamante"),
        ft.dropdown.Option("CDCE - Idelfonso Vásquez"),
        ft.dropdown.Option("CDCE - Juana de Ávila"),
        ft.dropdown.Option("CDCE - Olegario Villalobos"),
        ft.dropdown.Option("CDCE - Venancio Pulgar"),
        ft.dropdown.Option("Otro / Por Asignar")
    ]
    cdce_dropdown = ft.Dropdown(
        hint_text="Seleccione el CDCE / Parroquia",
        border=ft.InputBorder.NONE,
        text_style=ft.TextStyle(size=14, color=COLOR_TEXTO),
        options=opciones_cdce
    )

    # Logo de institución (solo para admin)
    campo_ruta_logo = ft.TextField(
        hint_text="Ruta del logo (opcional)",
        hint_style=ft.TextStyle(size=14, color=COLOR_TEXTO_SEC),
        border=ft.InputBorder.NONE,
        text_style=ft.TextStyle(size=14, color=COLOR_TEXTO),
        cursor_color=COLOR_PRIMARIO,
        expand=True,
    )

    def abrir_selector_archivo(_):
        """Abre el diálogo nativo de Windows para elegir una imagen (tkinter)."""
        if not _TK_AVAILABLE:
            _mostrar_error("El selector de archivos no está disponible en este entorno.")
            return
        try:
            root = Tk()
            root.withdraw()
            root.attributes("-topmost", True)
            ruta = filedialog.askopenfilename(
                title="Seleccionar logo de la institución",
                filetypes=[("Imágenes (PNG, JPG)", "*.png *.jpg *.jpeg"), ("Todos", "*.*")],
            )
            root.destroy()
            if ruta:
                campo_ruta_logo.value = ruta
                page.update()
        except Exception as ex:
            _mostrar_error(f"No se pudo abrir el selector: {ex}")

    nombre_completo = ft.TextField(
        hint_text="Nombre del Director/Enlace",
        hint_style=ft.TextStyle(size=14, color=COLOR_TEXTO_SEC),
        border=ft.InputBorder.NONE,
        text_style=ft.TextStyle(size=14, color=COLOR_TEXTO),
        cursor_color=COLOR_PRIMARIO,
    )
    cargo = ft.Dropdown(
        hint_text="Cargo (ej. Director, Coord.)",
        hint_style=ft.TextStyle(size=14, color=COLOR_TEXTO_SEC),
        border=ft.InputBorder.NONE,
        text_style=ft.TextStyle(size=14, color=COLOR_TEXTO),
        options=[
            ft.dropdown.Option("Directivo"),
            ft.dropdown.Option("Coordinador"),
        ],
    )
    correo = ft.TextField(
        hint_text="Correo electrónico",
        hint_style=ft.TextStyle(size=14, color=COLOR_TEXTO_SEC),
        border=ft.InputBorder.NONE,
        text_style=ft.TextStyle(size=14, color=COLOR_TEXTO),
        cursor_color=COLOR_PRIMARIO,
    )
    tel_personal = ft.TextField(
        hint_text="Teléfono móvil",
        hint_style=ft.TextStyle(size=14, color=COLOR_TEXTO_SEC),
        border=ft.InputBorder.NONE,
        text_style=ft.TextStyle(size=14, color=COLOR_TEXTO),
        cursor_color=COLOR_PRIMARIO,
    )

    cedula_admin = ft.TextField(
        hint_text="Cédula",
        hint_style=ft.TextStyle(size=14, color=COLOR_TEXTO_SEC),
        border=ft.InputBorder.NONE,
        text_style=ft.TextStyle(size=14, color=COLOR_TEXTO),
        cursor_color=COLOR_PRIMARIO,
    )
    usuario = ft.TextField(
        hint_text="Usuario deseado",
        hint_style=ft.TextStyle(size=14, color=COLOR_TEXTO_SEC),
        border=ft.InputBorder.NONE,
        text_style=ft.TextStyle(size=14, color=COLOR_TEXTO),
        cursor_color=COLOR_PRIMARIO,
    )
    contrasena = ft.TextField(
        hint_text="Contraseña",
        hint_style=ft.TextStyle(size=14, color=COLOR_TEXTO_SEC),
        password=True,
        can_reveal_password=True,
        border=ft.InputBorder.NONE,
        text_style=ft.TextStyle(size=14, color=COLOR_TEXTO),
        cursor_color=COLOR_PRIMARIO,
    )
    confirmar = ft.TextField(
        hint_text="Confirmar contraseña",
        hint_style=ft.TextStyle(size=14, color=COLOR_TEXTO_SEC),
        password=True,
        can_reveal_password=True,
        border=ft.InputBorder.NONE,
        text_style=ft.TextStyle(size=14, color=COLOR_TEXTO),
        cursor_color=COLOR_PRIMARIO,
    )

    # --- Campos (profesor) ---
    try:
        inst_opciones = [ft.dropdown.Option(str(i["idInstitucion"]), i["nombre_institucion"]) for i in listar_instituciones()]
    except Exception:
        inst_opciones = []
    dropdown_inst = ft.Dropdown(
        hint_text="Seleccione la institución donde trabaja",
        options=inst_opciones,
        border=ft.InputBorder.NONE,
        text_style=ft.TextStyle(size=14, color=COLOR_TEXTO),
    )
    nombre_prof = ft.TextField(
        hint_text="Nombre completo",
        hint_style=ft.TextStyle(size=14, color=COLOR_TEXTO_SEC),
        border=ft.InputBorder.NONE,
        text_style=ft.TextStyle(size=14, color=COLOR_TEXTO),
        cursor_color=COLOR_PRIMARIO,
    )
    cedula_prof = ft.TextField(
        hint_text="Cédula",
        hint_style=ft.TextStyle(size=14, color=COLOR_TEXTO_SEC),
        border=ft.InputBorder.NONE,
        text_style=ft.TextStyle(size=14, color=COLOR_TEXTO),
        cursor_color=COLOR_PRIMARIO,
    )
    usuario_prof = ft.TextField(
        hint_text="Usuario para iniciar sesión",
        hint_style=ft.TextStyle(size=14, color=COLOR_TEXTO_SEC),
        border=ft.InputBorder.NONE,
        text_style=ft.TextStyle(size=14, color=COLOR_TEXTO),
        cursor_color=COLOR_PRIMARIO,
    )
    correo_prof = ft.TextField(
        hint_text="Correo electrónico",
        border=ft.InputBorder.NONE,
        text_style=ft.TextStyle(size=14, color=COLOR_TEXTO),
        cursor_color=COLOR_PRIMARIO,
    )
    contrasena_prof = ft.TextField(
        hint_text="Contraseña (mín. 6 caracteres)",
        hint_style=ft.TextStyle(size=14, color=COLOR_TEXTO_SEC),
        password=True,
        can_reveal_password=True,
        border=ft.InputBorder.NONE,
        text_style=ft.TextStyle(size=14, color=COLOR_TEXTO),
        cursor_color=COLOR_PRIMARIO,
    )
    confirmar_prof = ft.TextField(
        hint_text="Confirmar contraseña",
        password=True,
        can_reveal_password=True,
        border=ft.InputBorder.NONE,
        text_style=ft.TextStyle(size=14, color="#334155"),
        cursor_color=COLOR_PRIMARIO,
    )

    # --- Botón Registrar (referencia para on_registrar) ---
    btn_registrar = ft.FilledButton(
        content=ft.Text("Registrar Institución", size=15, weight="w600"),
        style=ft.ButtonStyle(
            color="white",
            bgcolor=COLOR_PRIMARIO,
            shape=ft.RoundedRectangleBorder(radius=12),
            padding=ft.Padding.symmetric(vertical=18),
            elevation=8,
            shadow_color=ft.Colors.with_opacity(0.5, COLOR_PRIMARIO),
        ),
        width=300,
    )

    def _reset_btn():
        btn_registrar.content = ft.Text("Registrar Institución", size=15, weight="w600")
        btn_registrar.disabled = False

    async def on_registrar(e):
        btn_registrar.content = ft.ProgressRing(width=20, height=20, stroke_width=2, color="white")
        btn_registrar.disabled = True
        page.update()
        await asyncio.sleep(0.5)

        def _es_error_conexion(err):
            s = str(err).lower()
            return (
                "connect" in s or "mysql" in s or "2003" in s or "10061" in s
                or (mysql_errors and isinstance(err, mysql_errors.DatabaseError))
            )

        try:
            # ---------- Registro como PROFESOR ----------
            if tipo_cuenta["value"] == "profesor":
                if not dropdown_inst.value:
                    _mostrar_error("Seleccione la institución donde trabaja.")
                    _reset_btn()
                    return
                if not nombre_prof.value or not nombre_prof.value.strip():
                    _mostrar_error("Ingrese su nombre completo.")
                    _reset_btn()
                    return
                if not usuario_prof.value or not usuario_prof.value.strip():
                    _mostrar_error("Ingrese un usuario para iniciar sesión.")
                    _reset_btn()
                    return
                if usuario_ya_existe(usuario_prof.value.strip().lower()):
                    _mostrar_error("Ese nombre de usuario ya está en uso. Elija otro.")
                    _reset_btn()
                    return
                if not correo_prof.value or not correo_prof.value.strip():
                    _mostrar_error("Ingrese su correo electrónico.")
                    _reset_btn()
                    return
                if not _es_email_valido(correo_prof.value.strip()):
                    _mostrar_error("El correo debe tener un formato válido (ejemplo: nombre@dominio.com).")
                    _reset_btn()
                    return
                if email_ya_existe(correo_prof.value.strip().lower()):
                    _mostrar_error("Ese correo ya está registrado. Use otro o inicie sesión.")
                    _reset_btn()
                    return
                if not contrasena_prof.value or len(contrasena_prof.value) < 6:
                    _mostrar_error("La contraseña debe tener al menos 6 caracteres.")
                    _reset_btn()
                    return
                if contrasena_prof.value != confirmar_prof.value:
                    _mostrar_error("Las contraseñas no coinciden.")
                    _reset_btn()
                    return
                try:
                    id_inst = int(dropdown_inst.value)
                    # El profesor se vincula a la institución; las brigadas las crea después.
                    partes = nombre_prof.value.strip().split(None, 1)
                    nombre_p = partes[0] if partes else "Usuario"
                    apellido_p = partes[1] if len(partes) > 1 else ""
                    crear_usuario(
                        nombre=nombre_p,
                        apellido=apellido_p,
                        email=correo_prof.value.strip().lower(),
                        contrasena_plana=contrasena_prof.value,
                        rol="Profesor",
                        brigada_id=None,
                        institucion_id=id_inst,
                        usuario=usuario_prof.value.strip().lower(),
                        cedula=(cedula_prof.value or "").strip() or None,
                    )
                    page.snack_bar = ft.SnackBar(ft.Text("¡Registro exitoso! Ahora inicie sesión."), bgcolor="#22c55e")
                    page.snack_bar.open = True
                    on_back_to_login()
                except Exception as err:
                    _mostrar_error(f"Error al registrar: {err}")
                _reset_btn()
                page.update()
                return

            # ---------- Registro como DIRECTIVO / COORDINADOR ----------
            # Validar campos obligatorios
            if not nom_inst.value or not nom_inst.value.strip():
                _mostrar_error("Ingrese el nombre de la institución.")
                _reset_btn()
                return

            if not nombre_completo.value or not nombre_completo.value.strip():
                _mostrar_error("Ingrese el nombre completo del administrador.")
                _reset_btn()
                return

            if not correo.value or not correo.value.strip():
                _mostrar_error("Ingrese el correo electrónico.")
                _reset_btn()
                return

            # Validar formato de email (mostrar en diálogo para que siempre se vea)
            if not _es_email_valido(correo.value.strip()):
                _mostrar_error("El correo debe tener un formato válido (ejemplo: nombre@dominio.com).")
                _reset_btn()
                return

            if not contrasena.value or not contrasena.value.strip():
                _mostrar_error("Ingrese una contraseña.")
                _reset_btn()
                return

            if contrasena.value != confirmar.value:
                _mostrar_error("Las contraseñas no coinciden.")
                _reset_btn()
                return

            if len(contrasena.value) < 6:
                _mostrar_error("La contraseña debe tener al menos 6 caracteres.")
                _reset_btn()
                return

            if email_ya_existe(correo.value.strip().lower()):
                _mostrar_error("El correo ya está registrado. Use otro o inicie sesión.")
                _reset_btn()
                return

            usuario_str = (usuario.value or "").strip()
            if not usuario_str:
                _mostrar_error("Ingrese un usuario para iniciar sesión.")
                _reset_btn()
                return
            if usuario_ya_existe(usuario_str.lower()):
                _mostrar_error("Ese nombre de usuario ya está en uso. Elija otro.")
                _reset_btn()
                return

            try:
                id_inst = crear_institucion(
                    nombre=nom_inst.value.strip(),
                    direccion=(direccion.value or "").strip(),
                    telefono=(tel_inst.value or "").strip(),
                    cdce=(cdce_dropdown.value or "").strip() or None,
                )
                # No se crea brigada: directivos/coordinadores no tienen brigada; las brigadas las crean los profesores.
                partes = (nombre_completo.value or "").strip().split(None, 1)
                nombre = partes[0] if partes else "Usuario"
                apellido = partes[1] if len(partes) > 1 else ""
                rol = (cargo.value or "Directivo").strip()
                crear_usuario(
                    nombre=nombre,
                    apellido=apellido,
                    email=(correo.value or "").strip().lower(),
                    contrasena_plana=contrasena.value,
                    rol=rol,
                    brigada_id=None,
                    institucion_id=id_inst,
                    usuario=usuario_str.lower(),
                    cedula=(cedula_admin.value or "").strip() or None,
                )
                # Guardar logo si se indicó una ruta válida
                ruta_logo = (campo_ruta_logo.value or "").strip()
                if ruta_logo and os.path.isfile(ruta_logo):
                    try:
                        ext = os.path.splitext(ruta_logo)[1].lower()
                        if ext not in (".png", ".jpg", ".jpeg"):
                            ext = ".png"
                        os.makedirs(DIR_LOGOS, exist_ok=True)
                        dest = os.path.join(DIR_LOGOS, f"{id_inst}{ext}")
                        shutil.copy2(ruta_logo, dest)
                        actualizar_logo_institucion(id_inst, f"{id_inst}{ext}")
                    except Exception:
                        pass
                page.snack_bar = ft.SnackBar(ft.Text("¡Registro exitoso! Ahora inicie sesión."), bgcolor="#22c55e")
                page.snack_bar.open = True
                on_back_to_login()
            except Exception as err:
                _mostrar_error(f"Error al registrar: {err}")
            _reset_btn()
            page.update()
        except (RuntimeError, Exception) as err:
            if _es_error_conexion(err):
                _mostrar_error("No se pudo conectar a la base de datos. Verifique que MySQL esté en ejecución (localhost:3306).")
            else:
                _mostrar_error(f"Error: {err}")
            _reset_btn()
            page.update()

    btn_registrar.on_click = lambda e: page.run_task(on_registrar, e)

    btn_cancelar = ft.TextButton(
        "Cancelar y Volver",
        style=ft.ButtonStyle(color=COLOR_TEXTO_SEC),
        on_click=lambda e: on_back_to_login(),
    )

    # --- Formulario ADMIN (Directivo/Coordinador) ---
    form_admin = ft.Column(
        [
            _titulo_seccion("Datos de la Institución", ft.Icons.SCHOOL_ROUNDED),
            ft.Row(
                [
                    ft.Container(content=_input_con_titulo_y_glow("Nombre de la Institución *", nom_inst, GLOW_AZUL), expand=True),
                    ft.Container(width=16),
                    ft.Container(content=_input_con_titulo_y_glow("Nivel Educativo *", nivel, GLOW_AZUL, is_dropdown=True), expand=True),
                ],
                spacing=0,
            ),
            ft.Container(height=10),
            ft.Row(
                [
                    ft.Container(content=_input_con_titulo_y_glow("Territorio Escolar (CDCE) *", cdce_dropdown, GLOW_AZUL, is_dropdown=True), expand=True),
                    ft.Container(width=16),
                    ft.Container(content=_input_con_titulo_y_glow("Teléfono Institución", tel_inst, GLOW_AZUL), expand=True),
                ],
                spacing=0,
            ),
            ft.Container(height=10),
            _input_con_titulo_y_glow("Dirección", direccion, GLOW_AZUL),
            ft.Container(height=16),
            _titulo_seccion("Logo de la institución (opcional)", ft.Icons.IMAGE_OUTLINED),
            ft.Row(
                [
                    ft.Container(content=_input_con_titulo_y_glow("Ruta del logo", campo_ruta_logo, GLOW_AZUL), expand=True),
                    ft.Container(width=12),
                    ft.Container(
                        content=ft.OutlinedButton(
                            content=ft.Row([ft.Icon(ft.Icons.FOLDER_OPEN, size=18), ft.Text("Seleccionar archivo")], spacing=6),
                            on_click=abrir_selector_archivo,
                        ),
                        alignment=ft.Alignment(-1, 0),
                    ),
                ],
                spacing=0,
            ),
            ft.Text("Use el botón para elegir una imagen PNG o JPG desde su equipo.", size=12, color=COLOR_TEXTO_SEC),
            ft.Divider(height=30, color=COLOR_VERDE_SUAVE),
            _titulo_seccion("Datos del Administrador/Directivo", ft.Icons.PERSON_ROUNDED),
            ft.Row(
                [
                    ft.Container(content=_input_con_titulo_y_glow("Nombre Completo *", nombre_completo, GLOW_MORADO), expand=True),
                    ft.Container(width=16),
                    ft.Container(content=_input_con_titulo_y_glow("Cargo *", cargo, GLOW_MORADO, is_dropdown=True), expand=True),
                ],
                spacing=0,
            ),
            ft.Container(height=10),
            ft.Row(
                [
                    ft.Container(content=_input_con_titulo_y_glow("Correo Electrónico *", correo, GLOW_MORADO), expand=True),
                    ft.Container(width=16),
                    ft.Container(content=_input_con_titulo_y_glow("Teléfono Personal", tel_personal, GLOW_MORADO), expand=True),
                ],
                spacing=0,
            ),
            ft.Divider(height=30, color=COLOR_VERDE_SUAVE),
            _input_con_titulo_y_glow("Cédula", cedula_admin, GLOW_MORADO),
            ft.Container(height=10),
            _titulo_seccion("Credenciales de Acceso", ft.Icons.LOCK_ROUNDED),
            _input_con_titulo_y_glow("Usuario *", usuario, GLOW_VERDE),
            ft.Container(height=10),
            _input_con_titulo_y_glow("Contraseña *", contrasena, GLOW_VERDE),
            ft.Container(height=10),
            _input_con_titulo_y_glow("Confirmar Contraseña *", confirmar, GLOW_VERDE),
            ft.Container(height=30),
            ft.Row([btn_registrar], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(height=12),
            ft.Row([btn_cancelar], alignment=ft.MainAxisAlignment.CENTER),
        ],
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
    )

    # --- Formulario PROFESOR ---
    form_profesor = ft.Column(
        [
            _titulo_seccion("Institución y datos personales", ft.Icons.SCHOOL_ROUNDED),
            _input_con_titulo_y_glow("Institución donde trabaja *", dropdown_inst, GLOW_AZUL, is_dropdown=True),
            ft.Container(height=16),
            _input_con_titulo_y_glow("Nombre completo *", nombre_prof, GLOW_MORADO),
            ft.Container(height=16),
            _input_con_titulo_y_glow("Cédula", cedula_prof, GLOW_MORADO),
            ft.Container(height=16),
            _titulo_seccion("Credenciales de acceso", ft.Icons.LOCK_ROUNDED),
            _input_con_titulo_y_glow("Usuario *", usuario_prof, GLOW_VERDE),
            ft.Container(height=10),
            _input_con_titulo_y_glow("Correo electrónico *", correo_prof, GLOW_VERDE),
            ft.Container(height=10),
            _input_con_titulo_y_glow("Contraseña *", contrasena_prof, GLOW_VERDE),
            ft.Container(height=10),
            _input_con_titulo_y_glow("Confirmar contraseña *", confirmar_prof, GLOW_VERDE),
            ft.Container(height=24),
            ft.Row([btn_registrar], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(height=12),
            ft.Row([btn_cancelar], alignment=ft.MainAxisAlignment.CENTER),
        ],
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
    )

    # --- Contenedor que alterna entre form_admin y form_profesor ---
    formulario_contenedor = ft.Container(content=form_admin)

    def _actualizar_formulario_visible():
        if tipo_cuenta["value"] == "profesor":
            formulario_contenedor.content = form_profesor
            btn_registrar.content = ft.Text("Registrarme como profesor", size=15, weight="w600")
        else:
            formulario_contenedor.content = form_admin
            btn_registrar.content = ft.Text("Registrar Institución", size=15, weight="w600")
        page.update()

    # Selector de tipo de cuenta con RadioGroup
    radio_admin = ft.Radio(value="admin", label="Directivo / Coordinador", fill_color=COLOR_PRIMARIO)
    radio_prof = ft.Radio(value="profesor", label="Profesor", fill_color=COLOR_PRIMARIO)

    def _on_radio_change(e):
        tipo_cuenta["value"] = e.control.value or "admin"
        _actualizar_formulario_visible()

    radio_group = ft.RadioGroup(
        content=ft.Row([radio_admin, radio_prof], spacing=24),
        value="admin",
        on_change=_on_radio_change,
    )

    selector_tipo = ft.Container(
        content=ft.Column(
            [
                ft.Text("Tipo de cuenta", size=16, weight="bold", color=COLOR_TEXTO),
                ft.Container(height=8),
                radio_group,
            ],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.START,
        ),
        padding=ft.Padding.only(bottom=16),
    )

    # --- Tarjeta glassmorphism (igual que login) ---
    register_card = ft.Container(
        content=ft.Column(
            [
                selector_tipo,
                formulario_contenedor,
            ],
            spacing=0,
        ),
        bgcolor=ft.Colors.with_opacity(0.85, COLOR_CARD),
        blur=ft.Blur(15, 15),
        padding=ft.Padding.all(40),
        border_radius=35,
        border=ft.Border.all(1.5, ft.Colors.with_opacity(0.3, COLOR_BORDE)),
        shadow=[
            ft.BoxShadow(blur_radius=60, spread_radius=-8, color=ft.Colors.with_opacity(0.2, COLOR_TEXTO), offset=ft.Offset(0, 28)),
            ft.BoxShadow(blur_radius=16, spread_radius=0, color=ft.Colors.with_opacity(0.08, COLOR_TEXTO), offset=ft.Offset(0, 12)),
        ],
        width=560,
    )

    # --- Fondo igual que login: blobs + partículas verdes, SIN casa ni icono gente ---
    background_blobs = [
        _crear_blob(GLOW_AZUL, 50, -50, 300),
        _crear_blob("#FCD34D", 100, 1100, 250),
        _crear_blob(GLOW_VERDE, 600, 100, 300),
        _crear_blob(GLOW_MORADO, 500, 1150, 250),
        _crear_blob(GLOW_MORADO, 700, 1100, 280),
    ]
    VERDES_PARTICULAS = [
        "#065f46",
        "#047857",
        COLOR_PRIMARIO,
        COLOR_PRIMARIO_CLARO,
        "#34d399",
        "#6ee7b7",
        "#86efac",
        "#a7f3d0",
        COLOR_VERDE_SUAVE,
    ]
    TAMANO_PARTICULA = 14
    config_particulas = [
        (200, 250, 12, 0),
        (120, 150, 0, 14),
        (80, 1100, -10, 8),
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

    async def animate_background():
        while True:
            for p in particulas_animadas:
                p.animate_float()
            if page.controls:
                page.update()
            await asyncio.sleep(2.1)

    page.run_task(animate_background)

    # --- Header (escudo verde + títulos) ---
    header = ft.Column(
        [
            ft.Container(
                content=ft.Icon(ft.Icons.SHIELD_ROUNDED, size=40, color="white"),
                width=70,
                height=70,
                border_radius=20,
                gradient=ft.LinearGradient(
                    colors=[COLOR_PRIMARIO_CLARO, COLOR_PRIMARIO],
                    begin=ft.Alignment.TOP_LEFT,
                    end=ft.Alignment.BOTTOM_RIGHT,
                ),
                shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.with_opacity(0.4, COLOR_PRIMARIO), offset=ft.Offset(0, 6)),
                alignment=ft.Alignment.CENTER,
            ),
            ft.Container(height=12),
            ft.Text("Registro de Nueva Institución", size=22, weight="bold", color=COLOR_TEXTO, text_align=ft.TextAlign.CENTER),
            ft.Text("Sistema de Brigadas Escolares - Municipio Maracaibo", size=14, color=COLOR_TEXTO_SEC, text_align=ft.TextAlign.CENTER),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0,
    )

    btn_theme_toggle = create_auth_theme_toggle(page)

    # --- Stack: fondo + blobs + partículas + contenido central ---
    return ft.Stack(
        [
            ft.Container(expand=True, bgcolor=COLOR_FONDO_VERDE),
            *background_blobs,
            *particulas_animadas,
            ft.Container(
                content=ft.Column(
                    [
                        ft.Container(height=30),
                        header,
                        ft.Container(height=20),
                        register_card,
                        ft.Container(height=24),
                        ft.Text("© 2026 Sistema de Brigadas Escolares - Municipio Maracaibo", size=11, color=COLOR_TEXTO_SEC),
                        ft.Container(height=20),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.AUTO,
                ),
                alignment=ft.Alignment.CENTER,
                expand=True,
            ),
            btn_theme_toggle,
        ],
        expand=True,
    )
