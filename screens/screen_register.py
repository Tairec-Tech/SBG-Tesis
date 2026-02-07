"""Registro de Nueva Institución — 3 secciones estilo Figma: Datos Institución, Administrador, Credenciales."""

import flet as ft

from database.crud_usuario import (
    crear_institucion,
    crear_brigada,
    crear_usuario,
    email_ya_existe,
)
from theme import (
    COLOR_PRIMARIO,
    COLOR_TEXTO,
    COLOR_TEXTO_SEC,
    COLOR_CARD,
    COLOR_BORDE,
    COLOR_CANCELAR,
)


def build(page: ft.Page, on_back_to_login) -> ft.Control:
    estilo_campo = dict(
        border_color=COLOR_BORDE,
        focused_border_color=COLOR_PRIMARIO,
        border_radius=12,
        width=280,
    )

    # Sección 1: Datos de la Institución
    nom_inst = ft.TextField(label="Nombre de la Institución *", hint_text="Nombre de la institución", **estilo_campo)
    nivel = ft.Dropdown(label="Nivel Educativo *", hint_text="Seleccione el nivel", options=[ft.dropdown.Option("Primaria"), ft.dropdown.Option("Secundaria"), ft.dropdown.Option("Ambos")], **estilo_campo)
    tel_inst = ft.TextField(label="Teléfono de la Institución *", hint_text="Teléfono de la institución", **estilo_campo)
    direccion = ft.TextField(label="Dirección *", hint_text="Dirección completa de la institución", multiline=True, **estilo_campo)

    # Sección 2: Datos del Administrador
    nombre_completo = ft.TextField(label="Nombre Completo *", hint_text="Nombre del directivo", **estilo_campo)
    cargo = ft.Dropdown(label="Cargo *", hint_text="Directivo", options=[ft.dropdown.Option("Directivo"), ft.dropdown.Option("Coordinador")], **estilo_campo)
    correo = ft.TextField(label="Correo Electrónico *", hint_text="Ingrese su correo", **estilo_campo)
    tel_personal = ft.TextField(label="Teléfono Personal *", hint_text="Teléfono personal", **estilo_campo)

    # Sección 3: Credenciales
    usuario = ft.TextField(label="Usuario *", hint_text="Nombre de usuario para acceder", **estilo_campo)
    contrasena = ft.TextField(label="Contraseña *", hint_text="Mínimo 8 caracteres", password=True, **estilo_campo)
    confirmar = ft.TextField(label="Confirmar Contraseña *", hint_text="Repita la contraseña", password=True, **estilo_campo)

    def on_cancel(_):
        on_back_to_login()

    def on_registrar(_):
        # Validar campos obligatorios
        if not (nom_inst.value and direccion.value and tel_inst.value):
            page.snack_bar = ft.SnackBar(ft.Text("Complete los datos de la institución"))
            page.snack_bar.open = True
            page.update()
            return
        if not (nombre_completo.value and correo.value):
            page.snack_bar = ft.SnackBar(ft.Text("Complete nombre y correo del administrador"))
            page.snack_bar.open = True
            page.update()
            return
        if not (usuario.value and contrasena.value and confirmar.value):
            page.snack_bar = ft.SnackBar(ft.Text("Complete usuario y contraseña"))
            page.snack_bar.open = True
            page.update()
            return
        if contrasena.value != confirmar.value:
            page.snack_bar = ft.SnackBar(ft.Text("Las contraseñas no coinciden"))
            page.snack_bar.open = True
            page.update()
            return
        if len(contrasena.value) < 6:
            page.snack_bar = ft.SnackBar(ft.Text("La contraseña debe tener al menos 6 caracteres"))
            page.snack_bar.open = True
            page.update()
            return
        if email_ya_existe(correo.value.strip()):
            page.snack_bar = ft.SnackBar(ft.Text("Ese correo ya está registrado. Use otro o inicie sesión."))
            page.snack_bar.open = True
            page.update()
            return
        try:
            id_inst = crear_institucion(
                nombre=nom_inst.value.strip(),
                direccion=direccion.value.strip(),
                telefono=tel_inst.value.strip(),
            )
            id_brigada = crear_brigada(
                nombre_brigada="Brigada General",
                area_accion="General",
                institucion_id=id_inst,
            )
            partes = (nombre_completo.value or "").strip().split(None, 1)
            nombre = partes[0] if partes else "Usuario"
            apellido = partes[1] if len(partes) > 1 else ""
            rol = cargo.value if cargo.value else "Directivo"
            crear_usuario(
                nombre=nombre,
                apellido=apellido,
                email=correo.value.strip(),
                contrasena_plana=contrasena.value,
                rol=rol,
                brigada_id=id_brigada,
            )
            page.snack_bar = ft.SnackBar(ft.Text("Institución y usuario registrados. Ya puede iniciar sesión."))
            page.snack_bar.open = True
            on_back_to_login()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error al registrar: {ex}"))
            page.snack_bar.open = True
        page.update()

    seccion = lambda titulo, icono, campos: ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [ft.Icon(icono, color=COLOR_PRIMARIO, size=22), ft.Text(titulo, size=16, weight="bold", color=COLOR_TEXTO)],
                    spacing=10,
                ),
                ft.Container(height=16),
                *campos,
            ],
            spacing=12,
            horizontal_alignment=ft.CrossAxisAlignment.START,
        ),
        padding=20,
    )

    contenido = ft.Column(
        [
            ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.SHIELD_ROUNDED, color=COLOR_PRIMARIO, size=40),
                        ft.Column(
                            [
                                ft.Text("Registro de Nueva Institución", size=22, weight="bold", color=COLOR_TEXTO),
                                ft.Text("Sistema de Brigadas Escolares - Municipio Maracaibo", size=14, color=COLOR_TEXTO_SEC),
                            ],
                            spacing=4,
                            horizontal_alignment=ft.CrossAxisAlignment.START,
                        ),
                    ],
                    spacing=16,
                ),
                padding=24,
            ),
            ft.Divider(height=1, color=COLOR_BORDE),
            seccion("Datos de la Institución", ft.Icons.SCHOOL_OUTLINED, [nom_inst, ft.Row([nivel, tel_inst], spacing=16), direccion]),
            seccion("Datos del Administrador/Directivo", ft.Icons.PERSON_OUTLINED, [nombre_completo, cargo, correo, tel_personal]),
            seccion("Credenciales de Acceso", ft.Icons.LOCK_OUTLINED, [usuario, contrasena, confirmar]),
            ft.Container(height=32),
            ft.Row(
                [
                    ft.OutlinedButton(
                        content=ft.Text("Cancelar", color=COLOR_CANCELAR),
                        style=ft.ButtonStyle(side=ft.BorderSide(1, COLOR_BORDE), shape=ft.RoundedRectangleBorder(radius=12)),
                        on_click=on_cancel,
                    ),
                    ft.FilledButton(
                        content=ft.Text("Registrar Institución"),
                        style=ft.ButtonStyle(bgcolor=COLOR_PRIMARIO, shape=ft.RoundedRectangleBorder(radius=12)),
                        on_click=on_registrar,
                    ),
                ],
                alignment=ft.MainAxisAlignment.END,
                spacing=16,
            ),
            ft.Container(height=40),
        ],
        scroll=ft.ScrollMode.AUTO,
        spacing=0,
    )

    return ft.Container(
        content=ft.Container(
            content=contenido,
            bgcolor=COLOR_CARD,
            border_radius=24,
            shadow=ft.BoxShadow(blur_radius=32, spread_radius=-4, color=ft.Colors.with_opacity(0.08, "black"), offset=ft.Offset(0, 12)),
            border=ft.Border.all(1, COLOR_BORDE),
        ),
        padding=48,
        expand=True,
        alignment=ft.Alignment.CENTER,
    )
