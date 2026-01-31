"""
Formularios CRUD del SGB — alineados con db_brigadas_maracaibo.
Cada formulario se abre en un diálogo al pulsar "Acceder" en las tarjetas de acción.
"""

import flet as ft

# Reutilizar paleta de views
COLOR_PRIMARIO = "#2563eb"
COLOR_TEXTO = "#1e293b"
COLOR_TEXTO_SEC = "#64748b"
COLOR_BORDE = "#e2e8f0"
COLOR_CARD = "#ffffff"
COLOR_CANCELAR = "#64748b"  # Gris slate — identifica Cancelar/Cerrar
RADIO = 10
PADDING = 16


def _etiqueta(texto: str) -> ft.Control:
    return ft.Text(texto, size=13, weight="w500", color=COLOR_TEXTO_SEC)


def _campo_texto(label: str, hint: str = "", password: bool = False, multiline: bool = False, value: str = "") -> ft.TextField:
    return ft.TextField(
        label=label,
        hint_text=hint,
        value=value or None,
        password=password,
        multiline=multiline,
        min_lines=1,
        max_lines=4 if multiline else 1,
        border_color=COLOR_BORDE,
        focused_border_color=COLOR_PRIMARIO,
        text_size=14,
        color=COLOR_TEXTO,
        cursor_color=COLOR_PRIMARIO,
        content_padding=ft.Padding(12, 14),
        border_radius=RADIO,
        dense=True,
    )


def _campo_numero(label: str, hint: str = "", value: str = "") -> ft.TextField:
    return ft.TextField(
        label=label,
        hint_text=hint,
        value=value or None,
        keyboard_type=ft.KeyboardType.NUMBER,
        border_color=COLOR_BORDE,
        focused_border_color=COLOR_PRIMARIO,
        text_size=14,
        color=COLOR_TEXTO,
        cursor_color=COLOR_PRIMARIO,
        content_padding=ft.Padding(12, 14),
        border_radius=RADIO,
        dense=True,
    )


def _selector(label: str, opciones: list, value: str = "") -> ft.Dropdown:
    return ft.Dropdown(
        label=label,
        options=[ft.dropdown.Option(str(o)) for o in opciones],
        value=value or (opciones[0] if opciones else None),
        border_color=COLOR_BORDE,
        focused_border_color=COLOR_PRIMARIO,
        text_size=14,
        color=COLOR_TEXTO,
        content_padding=ft.Padding(12, 14),
        border_radius=RADIO,
        dense=True,
    )


def _bloque_campo(label: str, control: ft.Control) -> ft.Column:
    return ft.Column(
        [ft.Container(content=_etiqueta(label), padding=ft.Padding(0, 0, 0, 6)), control],
        horizontal_alignment=ft.CrossAxisAlignment.START,
        spacing=4,
    )


def _cerrar_dialogo(page: ft.Page, _dialogo=None):
    """Cierra el diálogo activo usando la API de Flet (pop_dialog)."""
    page.pop_dialog()


def _on_cancelar(e: ft.ControlEvent, _dialogo=None):
    """Callback del botón Cancelar: cierra el diálogo activo."""
    _cerrar_dialogo(e.page)


def _dialogo_formulario(
    page: ft.Page,
    titulo: str,
    contenido: ft.Control,
    ancho: float = 480,
    on_guardar=None,
    texto_guardar: str = "Guardar",
    on_cancelar=None,
) -> ft.AlertDialog:
    """Crea un AlertDialog con contenido de formulario y botones Guardar/Cancelar."""
    dialogo = ft.AlertDialog(
        modal=True,
        bgcolor=COLOR_CARD,
        title=ft.Text(titulo, size=18, weight="w600", color=COLOR_TEXTO),
        content=ft.Container(
            content=ft.Column([contenido], scroll=ft.ScrollMode.AUTO, tight=True),
            width=ancho,
            bgcolor=COLOR_CARD,
        ),
        actions=[
            ft.TextButton(
                content=ft.Text("Cancelar", color=COLOR_CANCELAR, weight=ft.FontWeight.W_500),
                style=ft.ButtonStyle(color=COLOR_CANCELAR),
                on_click=lambda e: _on_cancelar(e),
            ),
            ft.FilledButton(
                texto_guardar,
                style=ft.ButtonStyle(bgcolor=COLOR_PRIMARIO),
                on_click=lambda e: (on_guardar(e) if on_guardar else None, _cerrar_dialogo(e.page)),
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    return dialogo


def _abrir_dialogo(page: ft.Page, dialogo: ft.AlertDialog):
    """Abre el diálogo usando la API de Flet (show_dialog)."""
    page.show_dialog(dialogo)


# ---------- Instituciones (2.0) ----------
# Institucion_Educativa: nombre_institucion, direccion, telefono


def abrir_form_institucion_registrar(page: ft.Page):
    nombre = _campo_texto("Nombre de la institución", "Ej: U.E. Nacional")
    direccion = _campo_texto("Dirección", "Dirección completa", multiline=True)
    telefono = _campo_texto("Teléfono", "Ej: 0261-1234567")

    def on_guardar(_):
        # TODO: conectar con BD
        page.snack_bar = ft.SnackBar(ft.Text("Institución registrada (pendiente conectar BD)"))
        page.snack_bar.open = True
        page.update()

    contenido = ft.Column(
        [
            _bloque_campo("Nombre de la institución", nombre),
            ft.Container(height=16),
            _bloque_campo("Dirección", direccion),
            ft.Container(height=16),
            _bloque_campo("Teléfono", telefono),
        ],
        spacing=0,
    )
    dialogo = _dialogo_formulario(page, "Registrar institución educativa", contenido, on_guardar=on_guardar)
    _abrir_dialogo(page, dialogo)


def abrir_form_institucion_modificar(page: ft.Page):
    id_inst = _campo_numero("ID institución", "Número de institución a modificar")
    nombre = _campo_texto("Nombre", "Nombre actualizado")
    direccion = _campo_texto("Dirección", "Dirección", multiline=True)
    telefono = _campo_texto("Teléfono", "Teléfono")

    def on_guardar(_):
        page.snack_bar = ft.SnackBar(ft.Text("Institución actualizada (pendiente conectar BD)"))
        page.snack_bar.open = True
        page.update()

    contenido = ft.Column(
        [
            _bloque_campo("ID institución", id_inst),
            ft.Container(height=16),
            _bloque_campo("Nombre", nombre),
            ft.Container(height=16),
            _bloque_campo("Dirección", direccion),
            ft.Container(height=16),
            _bloque_campo("Teléfono", telefono),
        ],
        spacing=0,
    )
    dialogo = _dialogo_formulario(page, "Modificar institución", contenido, on_guardar=on_guardar)
    _abrir_dialogo(page, dialogo)


def abrir_form_institucion_consultar(page: ft.Page):
    id_inst = _campo_numero("ID institución", "Consultar por ID")
    resultado = ft.Text("Ingrese ID y pulse Buscar.", size=13, color=COLOR_TEXTO_SEC)

    def on_buscar(_):
        resultado.value = f"Consulta para ID {id_inst.value or '(vacío)'} (pendiente conectar BD)."
        page.update()

    contenido = ft.Column(
        [
            _bloque_campo("ID institución", id_inst),
            ft.Container(height=16),
            ft.ElevatedButton("Buscar", on_click=on_buscar, style=ft.ButtonStyle(bgcolor=COLOR_PRIMARIO)),
            ft.Container(height=12),
            resultado,
        ],
        spacing=0,
    )
    dialogo = ft.AlertDialog(
        modal=True,
        bgcolor=COLOR_CARD,
        title=ft.Text("Consultar institución", size=18, weight="w600", color=COLOR_TEXTO),
        content=ft.Container(content=contenido, width=420, bgcolor=COLOR_CARD),
        actions=[ft.TextButton(content=ft.Text("Cerrar", color=COLOR_CANCELAR, weight=ft.FontWeight.W_500), style=ft.ButtonStyle(color=COLOR_CANCELAR), on_click=lambda e: _cerrar_dialogo(e.page))],
    )
    _abrir_dialogo(page, dialogo)


def abrir_form_institucion_eliminar(page: ft.Page):
    id_inst = _campo_numero("ID institución", "Número de institución a eliminar")

    def on_eliminar(_):
        page.snack_bar = ft.SnackBar(ft.Text("Institución eliminada (pendiente conectar BD)"))
        page.snack_bar.open = True
        page.update()

    contenido = ft.Column(
        [
            ft.Text("Eliminar una institución puede afectar brigadas asociadas. Confirme el ID.", size=13, color=COLOR_TEXTO_SEC),
            ft.Container(height=16),
            _bloque_campo("ID institución", id_inst),
        ],
        spacing=0,
    )
    dialogo = _dialogo_formulario(
        page, "Eliminar institución", contenido, on_guardar=on_eliminar, texto_guardar="Eliminar"
    )
    _abrir_dialogo(page, dialogo)


# ---------- Usuarios (3.0) ----------
# Usuario: nombre, apellido, email, contrasena, rol, Brigada_idBrigada


def abrir_form_usuario_registrar(page: ft.Page):
    nombre = _campo_texto("Nombre", "Nombre")
    apellido = _campo_texto("Apellido", "Apellido")
    email = _campo_texto("Correo electrónico", "email@ejemplo.com")
    contrasena = _campo_texto("Contraseña", "Mínimo 6 caracteres", password=True)
    rol = _selector("Rol", ["Administrador", "Coordinador", "Brigadista"])
    id_brigada = _campo_numero("ID Brigada", "Número de brigada asignada")

    def on_guardar(_):
        page.snack_bar = ft.SnackBar(ft.Text("Usuario registrado (pendiente conectar BD)"))
        page.snack_bar.open = True
        page.update()

    contenido = ft.Column(
        [
            _bloque_campo("Nombre", nombre),
            ft.Container(height=12),
            _bloque_campo("Apellido", apellido),
            ft.Container(height=12),
            _bloque_campo("Correo electrónico", email),
            ft.Container(height=12),
            _bloque_campo("Contraseña", contrasena),
            ft.Container(height=12),
            _bloque_campo("Rol", rol),
            ft.Container(height=12),
            _bloque_campo("ID Brigada", id_brigada),
        ],
        spacing=0,
    )
    dialogo = _dialogo_formulario(page, "Registrar usuario", contenido, on_guardar=on_guardar)
    _abrir_dialogo(page, dialogo)


def abrir_form_usuario_modificar(page: ft.Page):
    id_usuario = _campo_numero("ID Usuario", "Usuario a modificar")
    nombre = _campo_texto("Nombre", "")
    apellido = _campo_texto("Apellido", "")
    email = _campo_texto("Correo", "")
    rol = _selector("Rol", ["Administrador", "Coordinador", "Brigadista"])

    def on_guardar(_):
        page.snack_bar = ft.SnackBar(ft.Text("Usuario actualizado (pendiente conectar BD)"))
        page.snack_bar.open = True
        page.update()

    contenido = ft.Column(
        [
            _bloque_campo("ID Usuario", id_usuario),
            ft.Container(height=12),
            _bloque_campo("Nombre", nombre),
            ft.Container(height=12),
            _bloque_campo("Apellido", apellido),
            ft.Container(height=12),
            _bloque_campo("Correo", email),
            ft.Container(height=12),
            _bloque_campo("Rol", rol),
        ],
        spacing=0,
    )
    dialogo = _dialogo_formulario(page, "Modificar usuario", contenido, on_guardar=on_guardar)
    _abrir_dialogo(page, dialogo)


def abrir_form_usuario_consultar(page: ft.Page):
    id_usuario = _campo_numero("ID Usuario", "Consultar por ID")
    resultado = ft.Text("Ingrese ID y pulse Buscar.", size=13, color=COLOR_TEXTO_SEC)

    def on_buscar(_):
        resultado.value = f"Consulta usuario ID {id_usuario.value or '(vacío)'} (pendiente conectar BD)."
        page.update()

    contenido = ft.Column(
        [
            _bloque_campo("ID Usuario", id_usuario),
            ft.Container(height=12),
            ft.ElevatedButton("Buscar", on_click=on_buscar, style=ft.ButtonStyle(bgcolor=COLOR_PRIMARIO)),
            ft.Container(height=12),
            resultado,
        ],
        spacing=0,
    )
    dialogo = ft.AlertDialog(
        modal=True,
        bgcolor=COLOR_CARD,
        title=ft.Text("Consultar usuario", size=18, weight="w600", color=COLOR_TEXTO),
        content=ft.Container(content=contenido, width=420, bgcolor=COLOR_CARD),
        actions=[ft.TextButton(content=ft.Text("Cerrar", color=COLOR_CANCELAR, weight=ft.FontWeight.W_500), style=ft.ButtonStyle(color=COLOR_CANCELAR), on_click=lambda e: _cerrar_dialogo(e.page))],
    )
    _abrir_dialogo(page, dialogo)


def abrir_form_usuario_eliminar(page: ft.Page):
    id_usuario = _campo_numero("ID Usuario", "Usuario a eliminar")

    def on_eliminar(_):
        page.snack_bar = ft.SnackBar(ft.Text("Usuario eliminado (pendiente conectar BD)"))
        page.snack_bar.open = True
        page.update()

    contenido = ft.Column(
        [
            ft.Text("Confirme el ID del usuario a dar de baja.", size=13, color=COLOR_TEXTO_SEC),
            ft.Container(height=16),
            _bloque_campo("ID Usuario", id_usuario),
        ],
        spacing=0,
    )
    dialogo = _dialogo_formulario(page, "Eliminar usuario", contenido, on_guardar=on_eliminar, texto_guardar="Eliminar")
    _abrir_dialogo(page, dialogo)


# ---------- Brigadas (4.0) ----------
# Brigada: nombre_brigada, area_accion, fecha_creacion, Institucion_Educativa_idInstitucion


def abrir_form_brigada_registrar(page: ft.Page):
    nombre = _campo_texto("Nombre de la brigada", "Ej: Brigada Ambiental")
    area_accion = _campo_texto("Área de acción", "Ej: Reforestación, Reciclaje")
    id_institucion = _campo_numero("ID Institución", "Institución a la que pertenece")

    def on_guardar(_):
        page.snack_bar = ft.SnackBar(ft.Text("Brigada registrada (pendiente conectar BD)"))
        page.snack_bar.open = True
        page.update()

    contenido = ft.Column(
        [
            _bloque_campo("Nombre de la brigada", nombre),
            ft.Container(height=12),
            _bloque_campo("Área de acción", area_accion),
            ft.Container(height=12),
            _bloque_campo("ID Institución", id_institucion),
        ],
        spacing=0,
    )
    dialogo = _dialogo_formulario(page, "Registrar brigada", contenido, on_guardar=on_guardar)
    _abrir_dialogo(page, dialogo)


def abrir_form_brigada_modificar(page: ft.Page):
    id_brigada = _campo_numero("ID Brigada", "Brigada a modificar")
    nombre = _campo_texto("Nombre", "")
    area_accion = _campo_texto("Área de acción", "")
    id_institucion = _campo_numero("ID Institución", "")

    def on_guardar(_):
        page.snack_bar = ft.SnackBar(ft.Text("Brigada actualizada (pendiente conectar BD)"))
        page.snack_bar.open = True
        page.update()

    contenido = ft.Column(
        [
            _bloque_campo("ID Brigada", id_brigada),
            ft.Container(height=12),
            _bloque_campo("Nombre", nombre),
            ft.Container(height=12),
            _bloque_campo("Área de acción", area_accion),
            ft.Container(height=12),
            _bloque_campo("ID Institución", id_institucion),
        ],
        spacing=0,
    )
    dialogo = _dialogo_formulario(page, "Modificar brigada", contenido, on_guardar=on_guardar)
    _abrir_dialogo(page, dialogo)


def abrir_form_brigada_consultar(page: ft.Page):
    id_brigada = _campo_numero("ID Brigada", "Consultar por ID")
    resultado = ft.Text("Ingrese ID y pulse Buscar.", size=13, color=COLOR_TEXTO_SEC)

    def on_buscar(_):
        resultado.value = f"Consulta brigada ID {id_brigada.value or '(vacío)'} (pendiente conectar BD)."
        page.update()

    contenido = ft.Column(
        [
            _bloque_campo("ID Brigada", id_brigada),
            ft.Container(height=12),
            ft.ElevatedButton("Buscar", on_click=on_buscar, style=ft.ButtonStyle(bgcolor=COLOR_PRIMARIO)),
            ft.Container(height=12),
            resultado,
        ],
        spacing=0,
    )
    dialogo = ft.AlertDialog(
        modal=True,
        bgcolor=COLOR_CARD,
        title=ft.Text("Consultar brigada", size=18, weight="w600", color=COLOR_TEXTO),
        content=ft.Container(content=contenido, width=420, bgcolor=COLOR_CARD),
        actions=[ft.TextButton(content=ft.Text("Cerrar", color=COLOR_CANCELAR, weight=ft.FontWeight.W_500), style=ft.ButtonStyle(color=COLOR_CANCELAR), on_click=lambda e: _cerrar_dialogo(e.page))],
    )
    _abrir_dialogo(page, dialogo)


def abrir_form_brigada_eliminar(page: ft.Page):
    id_brigada = _campo_numero("ID Brigada", "Brigada a eliminar")

    def on_eliminar(_):
        page.snack_bar = ft.SnackBar(ft.Text("Brigada eliminada (pendiente conectar BD)"))
        page.snack_bar.open = True
        page.update()

    contenido = ft.Column(
        [
            ft.Text("Eliminar una brigada puede afectar actividades y usuarios asociados.", size=13, color=COLOR_TEXTO_SEC),
            ft.Container(height=16),
            _bloque_campo("ID Brigada", id_brigada),
        ],
        spacing=0,
    )
    dialogo = _dialogo_formulario(page, "Eliminar brigada", contenido, on_guardar=on_eliminar, texto_guardar="Eliminar")
    _abrir_dialogo(page, dialogo)


def abrir_form_brigada_asignar(page: ft.Page):
    id_brigada = _campo_numero("ID Brigada", "")
    id_actividad = _campo_numero("ID Actividad", "Actividad a asignar (opcional)")
    id_institucion = _campo_numero("ID Institución", "Institución (opcional)")

    def on_guardar(_):
        page.snack_bar = ft.SnackBar(ft.Text("Asignación registrada (pendiente conectar BD)"))
        page.snack_bar.open = True
        page.update()

    contenido = ft.Column(
        [
            ft.Text("Asignar brigada a actividad o institución.", size=13, color=COLOR_TEXTO_SEC),
            ft.Container(height=16),
            _bloque_campo("ID Brigada", id_brigada),
            ft.Container(height=12),
            _bloque_campo("ID Actividad", id_actividad),
            ft.Container(height=12),
            _bloque_campo("ID Institución", id_institucion),
        ],
        spacing=0,
    )
    dialogo = _dialogo_formulario(page, "Asignar brigada", contenido, on_guardar=on_guardar)
    _abrir_dialogo(page, dialogo)


def abrir_form_brigada_miembros(page: ft.Page):
    id_brigada = _campo_numero("ID Brigada", "Ver o gestionar miembros")

    def on_buscar(_):
        page.snack_bar = ft.SnackBar(ft.Text("Listado de miembros (pendiente conectar BD)"))
        page.snack_bar.open = True
        page.update()

    contenido = ft.Column(
        [
            _bloque_campo("ID Brigada", id_brigada),
            ft.Container(height=12),
            ft.ElevatedButton("Ver miembros", on_click=on_buscar, style=ft.ButtonStyle(bgcolor=COLOR_PRIMARIO)),
        ],
        spacing=0,
    )
    dialogo = ft.AlertDialog(
        modal=True,
        bgcolor=COLOR_CARD,
        title=ft.Text("Gestionar miembros de brigada", size=18, weight="w600", color=COLOR_TEXTO),
        content=ft.Container(content=contenido, width=420, bgcolor=COLOR_CARD),
        actions=[ft.TextButton(content=ft.Text("Cerrar", color=COLOR_CANCELAR, weight=ft.FontWeight.W_500), style=ft.ButtonStyle(color=COLOR_CANCELAR), on_click=lambda e: _cerrar_dialogo(e.page))],
    )
    _abrir_dialogo(page, dialogo)


# ---------- Actividades (5.0) ----------
# Actividad: estado, titulo, descripcion, fecha_inicio, fecha_fin, Brigada_idBrigada


def abrir_form_actividad_registrar(page: ft.Page):
    titulo = _campo_texto("Título", "Nombre de la actividad")
    descripcion = _campo_texto("Descripción", "Detalle", multiline=True)
    estado = _selector("Estado", ["Planificada", "En curso", "Finalizada"])
    fecha_inicio = _campo_texto("Fecha inicio", "YYYY-MM-DD")
    fecha_fin = _campo_texto("Fecha fin", "YYYY-MM-DD")
    id_brigada = _campo_numero("ID Brigada", "Brigada responsable")

    def on_guardar(_):
        page.snack_bar = ft.SnackBar(ft.Text("Actividad registrada (pendiente conectar BD)"))
        page.snack_bar.open = True
        page.update()

    contenido = ft.Column(
        [
            _bloque_campo("Título", titulo),
            ft.Container(height=12),
            _bloque_campo("Descripción", descripcion),
            ft.Container(height=12),
            _bloque_campo("Estado", estado),
            ft.Container(height=12),
            _bloque_campo("Fecha inicio", fecha_inicio),
            ft.Container(height=12),
            _bloque_campo("Fecha fin", fecha_fin),
            ft.Container(height=12),
            _bloque_campo("ID Brigada", id_brigada),
        ],
        spacing=0,
    )
    dialogo = _dialogo_formulario(page, "Registrar actividad", contenido, on_guardar=on_guardar)
    _abrir_dialogo(page, dialogo)


def abrir_form_actividad_modificar(page: ft.Page):
    id_act = _campo_numero("ID Actividad", "Actividad a modificar")
    titulo = _campo_texto("Título", "")
    descripcion = _campo_texto("Descripción", "", multiline=True)
    estado = _selector("Estado", ["Planificada", "En curso", "Finalizada"])
    fecha_inicio = _campo_texto("Fecha inicio", "YYYY-MM-DD")
    fecha_fin = _campo_texto("Fecha fin", "YYYY-MM-DD")
    id_brigada = _campo_numero("ID Brigada", "")

    def on_guardar(_):
        page.snack_bar = ft.SnackBar(ft.Text("Actividad actualizada (pendiente conectar BD)"))
        page.snack_bar.open = True
        page.update()

    contenido = ft.Column(
        [
            _bloque_campo("ID Actividad", id_act),
            ft.Container(height=12),
            _bloque_campo("Título", titulo),
            ft.Container(height=12),
            _bloque_campo("Descripción", descripcion),
            ft.Container(height=12),
            _bloque_campo("Estado", estado),
            ft.Container(height=12),
            _bloque_campo("Fecha inicio", fecha_inicio),
            ft.Container(height=12),
            _bloque_campo("Fecha fin", fecha_fin),
            ft.Container(height=12),
            _bloque_campo("ID Brigada", id_brigada),
        ],
        spacing=0,
    )
    dialogo = _dialogo_formulario(page, "Modificar actividad", contenido, on_guardar=on_guardar)
    _abrir_dialogo(page, dialogo)


def abrir_form_actividad_consultar(page: ft.Page):
    id_act = _campo_numero("ID Actividad", "Consultar por ID")
    resultado = ft.Text("Ingrese ID y pulse Buscar.", size=13, color=COLOR_TEXTO_SEC)

    def on_buscar(_):
        resultado.value = f"Consulta actividad ID {id_act.value or '(vacío)'} (pendiente conectar BD)."
        page.update()

    contenido = ft.Column(
        [
            _bloque_campo("ID Actividad", id_act),
            ft.Container(height=12),
            ft.ElevatedButton("Buscar", on_click=on_buscar, style=ft.ButtonStyle(bgcolor=COLOR_PRIMARIO)),
            ft.Container(height=12),
            resultado,
        ],
        spacing=0,
    )
    dialogo = ft.AlertDialog(
        modal=True,
        bgcolor=COLOR_CARD,
        title=ft.Text("Consultar actividad", size=18, weight="w600", color=COLOR_TEXTO),
        content=ft.Container(content=contenido, width=420, bgcolor=COLOR_CARD),
        actions=[ft.TextButton(content=ft.Text("Cerrar", color=COLOR_CANCELAR, weight=ft.FontWeight.W_500), style=ft.ButtonStyle(color=COLOR_CANCELAR), on_click=lambda e: _cerrar_dialogo(e.page))],
    )
    _abrir_dialogo(page, dialogo)


def abrir_form_actividad_eliminar(page: ft.Page):
    id_act = _campo_numero("ID Actividad", "Actividad a eliminar")

    def on_eliminar(_):
        page.snack_bar = ft.SnackBar(ft.Text("Actividad eliminada (pendiente conectar BD)"))
        page.snack_bar.open = True
        page.update()

    contenido = ft.Column(
        [
            ft.Text("Eliminar una actividad puede afectar indicadores y reportes asociados.", size=13, color=COLOR_TEXTO_SEC),
            ft.Container(height=16),
            _bloque_campo("ID Actividad", id_act),
        ],
        spacing=0,
    )
    dialogo = _dialogo_formulario(page, "Eliminar actividad", contenido, on_guardar=on_eliminar, texto_guardar="Eliminar")
    _abrir_dialogo(page, dialogo)


def abrir_form_actividad_planificar(page: ft.Page):
    id_act = _campo_numero("ID Actividad", "Actividad a planificar")
    id_brigada = _campo_numero("ID Brigada", "Brigada responsable")
    fecha_inicio = _campo_texto("Fecha inicio", "YYYY-MM-DD")
    fecha_fin = _campo_texto("Fecha fin", "YYYY-MM-DD")

    def on_guardar(_):
        page.snack_bar = ft.SnackBar(ft.Text("Planificación registrada (pendiente conectar BD)"))
        page.snack_bar.open = True
        page.update()

    contenido = ft.Column(
        [
            _bloque_campo("ID Actividad", id_act),
            ft.Container(height=12),
            _bloque_campo("ID Brigada", id_brigada),
            ft.Container(height=12),
            _bloque_campo("Fecha inicio", fecha_inicio),
            ft.Container(height=12),
            _bloque_campo("Fecha fin", fecha_fin),
        ],
        spacing=0,
    )
    dialogo = _dialogo_formulario(page, "Planificar actividad", contenido, on_guardar=on_guardar)
    _abrir_dialogo(page, dialogo)


# ---------- Reportes (6.0) ----------
# Reporte_de_impacto: contenido, fecha_generacion, Actividad_idActividad, Usuario_idUsuario


def abrir_form_reporte_registrar(page: ft.Page):
    contenido = _campo_texto("Contenido del reporte", "Redacte el reporte de impacto", multiline=True)
    id_actividad = _campo_numero("ID Actividad", "Actividad relacionada")
    id_usuario = _campo_numero("ID Usuario", "Usuario que genera el reporte")

    def on_guardar(_):
        page.snack_bar = ft.SnackBar(ft.Text("Reporte registrado (pendiente conectar BD)"))
        page.snack_bar.open = True
        page.update()

    c = ft.Column(
        [
            _bloque_campo("Contenido del reporte", contenido),
            ft.Container(height=12),
            _bloque_campo("ID Actividad", id_actividad),
            ft.Container(height=12),
            _bloque_campo("ID Usuario", id_usuario),
        ],
        spacing=0,
    )
    dialogo = _dialogo_formulario(page, "Registrar reporte de impacto", c, on_guardar=on_guardar)
    _abrir_dialogo(page, dialogo)


def abrir_form_reporte_modificar(page: ft.Page):
    id_reporte = _campo_numero("ID Reporte", "Reporte a modificar")
    contenido = _campo_texto("Contenido", "", multiline=True)

    def on_guardar(_):
        page.snack_bar = ft.SnackBar(ft.Text("Reporte actualizado (pendiente conectar BD)"))
        page.snack_bar.open = True
        page.update()

    c = ft.Column(
        [_bloque_campo("ID Reporte", id_reporte), ft.Container(height=12), _bloque_campo("Contenido", contenido)],
        spacing=0,
    )
    dialogo = _dialogo_formulario(page, "Modificar reporte", c, on_guardar=on_guardar)
    _abrir_dialogo(page, dialogo)


def abrir_form_reporte_consultar(page: ft.Page):
    id_reporte = _campo_numero("ID Reporte", "Consultar por ID")
    resultado = ft.Text("Ingrese ID y pulse Buscar.", size=13, color=COLOR_TEXTO_SEC)

    def on_buscar(_):
        resultado.value = f"Consulta reporte ID {id_reporte.value or '(vacío)'} (pendiente conectar BD)."
        page.update()

    contenido = ft.Column(
        [
            _bloque_campo("ID Reporte", id_reporte),
            ft.Container(height=12),
            ft.ElevatedButton("Buscar", on_click=on_buscar, style=ft.ButtonStyle(bgcolor=COLOR_PRIMARIO)),
            ft.Container(height=12),
            resultado,
        ],
        spacing=0,
    )
    dialogo = ft.AlertDialog(
        modal=True,
        bgcolor=COLOR_CARD,
        title=ft.Text("Consultar reporte", size=18, weight="w600", color=COLOR_TEXTO),
        content=ft.Container(content=contenido, width=420, bgcolor=COLOR_CARD),
        actions=[ft.TextButton(content=ft.Text("Cerrar", color=COLOR_CANCELAR, weight=ft.FontWeight.W_500), style=ft.ButtonStyle(color=COLOR_CANCELAR), on_click=lambda e: _cerrar_dialogo(e.page))],
    )
    _abrir_dialogo(page, dialogo)


def abrir_form_reporte_eliminar(page: ft.Page):
    id_reporte = _campo_numero("ID Reporte", "Reporte a eliminar")

    def on_eliminar(_):
        page.snack_bar = ft.SnackBar(ft.Text("Reporte eliminado (pendiente conectar BD)"))
        page.snack_bar.open = True
        page.update()

    contenido = ft.Column(
        [
            ft.Text("Confirme el ID del reporte a eliminar.", size=13, color=COLOR_TEXTO_SEC),
            ft.Container(height=16),
            _bloque_campo("ID Reporte", id_reporte),
        ],
        spacing=0,
    )
    dialogo = _dialogo_formulario(page, "Eliminar reporte", contenido, on_guardar=on_eliminar, texto_guardar="Eliminar")
    _abrir_dialogo(page, dialogo)


# ---------- Indicadores (7.0) ----------
# Indicador_ambiental: valor, tipo_indicador, unidad, Actividad_idActividad


def abrir_form_indicador_registrar(page: ft.Page):
    valor = _campo_texto("Valor", "Ej: 15.5")
    tipo = _campo_texto("Tipo de indicador", "Ej: Árboles plantados")
    unidad = _campo_texto("Unidad", "Ej: unidades, kg, %")
    id_actividad = _campo_numero("ID Actividad", "Actividad asociada")

    def on_guardar(_):
        page.snack_bar = ft.SnackBar(ft.Text("Indicador registrado (pendiente conectar BD)"))
        page.snack_bar.open = True
        page.update()

    contenido = ft.Column(
        [
            _bloque_campo("Valor", valor),
            ft.Container(height=12),
            _bloque_campo("Tipo de indicador", tipo),
            ft.Container(height=12),
            _bloque_campo("Unidad", unidad),
            ft.Container(height=12),
            _bloque_campo("ID Actividad", id_actividad),
        ],
        spacing=0,
    )
    dialogo = _dialogo_formulario(page, "Registrar indicador ambiental", contenido, on_guardar=on_guardar)
    _abrir_dialogo(page, dialogo)


def abrir_form_indicador_modificar(page: ft.Page):
    id_ind = _campo_numero("ID Indicador", "Indicador a modificar")
    valor = _campo_texto("Valor", "")
    tipo = _campo_texto("Tipo", "")
    unidad = _campo_texto("Unidad", "")
    id_actividad = _campo_numero("ID Actividad", "")

    def on_guardar(_):
        page.snack_bar = ft.SnackBar(ft.Text("Indicador actualizado (pendiente conectar BD)"))
        page.snack_bar.open = True
        page.update()

    contenido = ft.Column(
        [
            _bloque_campo("ID Indicador", id_ind),
            ft.Container(height=12),
            _bloque_campo("Valor", valor),
            ft.Container(height=12),
            _bloque_campo("Tipo", tipo),
            ft.Container(height=12),
            _bloque_campo("Unidad", unidad),
            ft.Container(height=12),
            _bloque_campo("ID Actividad", id_actividad),
        ],
        spacing=0,
    )
    dialogo = _dialogo_formulario(page, "Modificar indicador", contenido, on_guardar=on_guardar)
    _abrir_dialogo(page, dialogo)


def abrir_form_indicador_consultar(page: ft.Page):
    id_ind = _campo_numero("ID Indicador", "Consultar por ID")
    resultado = ft.Text("Ingrese ID y pulse Buscar.", size=13, color=COLOR_TEXTO_SEC)

    def on_buscar(_):
        resultado.value = f"Consulta indicador ID {id_ind.value or '(vacío)'} (pendiente conectar BD)."
        page.update()

    contenido = ft.Column(
        [
            _bloque_campo("ID Indicador", id_ind),
            ft.Container(height=12),
            ft.ElevatedButton("Buscar", on_click=on_buscar, style=ft.ButtonStyle(bgcolor=COLOR_PRIMARIO)),
            ft.Container(height=12),
            resultado,
        ],
        spacing=0,
    )
    dialogo = ft.AlertDialog(
        modal=True,
        bgcolor=COLOR_CARD,
        title=ft.Text("Consultar indicador", size=18, weight="w600", color=COLOR_TEXTO),
        content=ft.Container(content=contenido, width=420, bgcolor=COLOR_CARD),
        actions=[ft.TextButton(content=ft.Text("Cerrar", color=COLOR_CANCELAR, weight=ft.FontWeight.W_500), style=ft.ButtonStyle(color=COLOR_CANCELAR), on_click=lambda e: _cerrar_dialogo(e.page))],
    )
    _abrir_dialogo(page, dialogo)


def abrir_form_indicador_eliminar(page: ft.Page):
    id_ind = _campo_numero("ID Indicador", "Indicador a eliminar")

    def on_eliminar(_):
        page.snack_bar = ft.SnackBar(ft.Text("Indicador eliminado (pendiente conectar BD)"))
        page.snack_bar.open = True
        page.update()

    contenido = ft.Column(
        [
            ft.Text("Confirme el ID del indicador a eliminar.", size=13, color=COLOR_TEXTO_SEC),
            ft.Container(height=16),
            _bloque_campo("ID Indicador", id_ind),
        ],
        spacing=0,
    )
    dialogo = _dialogo_formulario(page, "Eliminar indicador", contenido, on_guardar=on_eliminar, texto_guardar="Eliminar")
    _abrir_dialogo(page, dialogo)


def abrir_form_indicador_resumen(page: ft.Page):
    def on_generar(_):
        page.snack_bar = ft.SnackBar(ft.Text("Resumen (pendiente conectar BD)"))
        page.snack_bar.open = True
        page.update()

    contenido = ft.Column(
        [
            ft.Text("Vista consolidada de indicadores ambientales por actividad o período.", size=13, color=COLOR_TEXTO_SEC),
            ft.Container(height=16),
            ft.ElevatedButton("Generar resumen", style=ft.ButtonStyle(bgcolor=COLOR_PRIMARIO), on_click=on_generar),
        ],
        spacing=0,
    )
    dialogo = ft.AlertDialog(
        modal=True,
        bgcolor=COLOR_CARD,
        title=ft.Text("Resumen total de indicadores", size=18, weight="w600", color=COLOR_TEXTO),
        content=ft.Container(content=contenido, width=420, bgcolor=COLOR_CARD),
        actions=[ft.TextButton(content=ft.Text("Cerrar", color=COLOR_CANCELAR, weight=ft.FontWeight.W_500), style=ft.ButtonStyle(color=COLOR_CANCELAR), on_click=lambda e: _cerrar_dialogo(e.page))],
    )
    _abrir_dialogo(page, dialogo)


# ---------- Utilidades (8.0) ----------


def abrir_dialogo_acerca_de(page: ft.Page):
    contenido = ft.Column(
        [
            ft.Text("Sistema de Brigadas Escolares (SGB)", size=16, weight="w600", color=COLOR_TEXTO),
            ft.Container(height=8),
            ft.Text("Municipio Maracaibo — Gestión de brigadas ambientales.", size=13, color=COLOR_TEXTO_SEC),
            ft.Container(height=12),
            ft.Text("Versión 1.0", size=12, color=COLOR_TEXTO_SEC),
        ],
        spacing=0,
    )
    dialogo = ft.AlertDialog(
        modal=True,
        bgcolor=COLOR_CARD,
        title=ft.Text("Acerca de", size=18, weight="w600", color=COLOR_TEXTO),
        content=ft.Container(content=contenido, width=380, bgcolor=COLOR_CARD),
        actions=[ft.TextButton(content=ft.Text("Cerrar", color=COLOR_CANCELAR, weight=ft.FontWeight.W_500), style=ft.ButtonStyle(color=COLOR_CANCELAR), on_click=lambda e: _cerrar_dialogo(e.page))],
    )
    _abrir_dialogo(page, dialogo)


def abrir_dialogo_manual(page: ft.Page):
    contenido = ft.Column(
        [
            ft.Text("Manual de usuario y documentación del sistema.", size=13, color=COLOR_TEXTO_SEC),
            ft.Container(height=12),
            ft.Text("Consulte la documentación incluida en el proyecto o con el administrador.", size=13, color=COLOR_TEXTO_SEC),
        ],
        spacing=0,
    )
    dialogo = ft.AlertDialog(
        modal=True,
        bgcolor=COLOR_CARD,
        title=ft.Text("Manual de usuario", size=18, weight="w600", color=COLOR_TEXTO),
        content=ft.Container(content=contenido, width=400, bgcolor=COLOR_CARD),
        actions=[ft.TextButton(content=ft.Text("Cerrar", color=COLOR_CANCELAR, weight=ft.FontWeight.W_500), style=ft.ButtonStyle(color=COLOR_CANCELAR), on_click=lambda e: _cerrar_dialogo(e.page))],
    )
    _abrir_dialogo(page, dialogo)


def abrir_dialogo_legal(page: ft.Page):
    contenido = ft.Column(
        [
            ft.Text("Términos de uso, licencias y créditos del sistema.", size=13, color=COLOR_TEXTO_SEC),
            ft.Container(height=12),
            ft.Text("SGB — Uso institucional. Consulte con la entidad responsable.", size=13, color=COLOR_TEXTO_SEC),
        ],
        spacing=0,
    )
    dialogo = ft.AlertDialog(
        modal=True,
        bgcolor=COLOR_CARD,
        title=ft.Text("Información legal", size=18, weight="w600", color=COLOR_TEXTO),
        content=ft.Container(content=contenido, width=400, bgcolor=COLOR_CARD),
        actions=[ft.TextButton(content=ft.Text("Cerrar", color=COLOR_CANCELAR, weight=ft.FontWeight.W_500), style=ft.ButtonStyle(color=COLOR_CANCELAR), on_click=lambda e: _cerrar_dialogo(e.page))],
    )
    _abrir_dialogo(page, dialogo)


def abrir_dialogo_importar_bd(page: ft.Page):
    contenido = ft.Column(
        [
            ft.Text("Importar o restaurar la base de datos desde un archivo de respaldo.", size=13, color=COLOR_TEXTO_SEC),
            ft.Container(height=16),
            ft.Text("Funcionalidad de respaldo/restauración (pendiente conectar con BD).", size=12, color=COLOR_TEXTO_SEC),
        ],
        spacing=0,
    )
    dialogo = ft.AlertDialog(
        modal=True,
        bgcolor=COLOR_CARD,
        title=ft.Text("Importar / restaurar BD", size=18, weight="w600", color=COLOR_TEXTO),
        content=ft.Container(content=contenido, width=400, bgcolor=COLOR_CARD),
        actions=[ft.TextButton(content=ft.Text("Cerrar", color=COLOR_CANCELAR, weight=ft.FontWeight.W_500), style=ft.ButtonStyle(color=COLOR_CANCELAR), on_click=lambda e: _cerrar_dialogo(e.page))],
    )
    _abrir_dialogo(page, dialogo)
