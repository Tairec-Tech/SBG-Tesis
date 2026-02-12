"""
Formularios CRUD del SGB — brigadas ambientales (tonos verdes).
"""

import flet as ft

from database.crud_brigada import insertar_brigada, actualizar_brigada, eliminar_brigada, obtener_brigada, listar_brigadas
from database.crud_usuario import (
    crear_usuario, email_ya_existe, listar_brigadistas, actualizar_usuario, 
    eliminar_usuario, obtener_usuario, es_admin, es_profesor, listar_profesores_institucion
)
from theme import (
    COLOR_PRIMARIO,
    COLOR_PRIMARIO_CLARO,
    COLOR_TEXTO,
    COLOR_TEXTO_SEC,
    COLOR_BORDE,
    COLOR_CARD,
    COLOR_CANCELAR,
)
RADIO = 12
PADDING = 20
# Dimensiones del contenedor del formulario (modal)
ANCHO_FORM = 520
ALTURA_MAX_FORM = 480
# Nueva Brigada: contenedor más compacto, alineado a la imagen
ANCHO_FORM_NUEVA_BRIGADA = 400
PADDING_NUEVA_BRIGADA = 20
ALTURA_BOTON_NUEVA_BRIGADA = 52
# Estilo común para campos (alineado a Figma)
_CAMPO_PADDING = ft.Padding(14, 16)
_CAMPO_BASE = dict(
    border_color=COLOR_BORDE,
    focused_border_color=COLOR_PRIMARIO,
    border_radius=RADIO,
    text_size=14,
    color=COLOR_TEXTO,
    cursor_color=COLOR_PRIMARIO,
    content_padding=_CAMPO_PADDING,
)


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


def _campo_con_titulo(titulo: str, control: ft.Control, espaciado_abajo: int = 16) -> ft.Column:
    """Título visible sobre el control; se usa en todos los formularios tipo Figma."""
    return ft.Column(
        [
            ft.Text(titulo, size=14, weight="w500", color=COLOR_TEXTO),
            ft.Container(height=8),
            control,
            ft.Container(height=espaciado_abajo),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.START,
        spacing=0,
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
    ancho: float = None,
    on_guardar=None,
    texto_guardar: str = "Guardar",
    on_cancelar=None,
) -> ft.AlertDialog:
    """Crea un AlertDialog con contenido de formulario y botones Guardar/Cancelar."""
    w = ancho if ancho is not None else ANCHO_FORM
    dialogo = ft.AlertDialog(
        modal=True,
        bgcolor=COLOR_CARD,
        title=ft.Text(titulo, size=18, weight="w600", color=COLOR_TEXTO),
        content=ft.Container(
            content=ft.Column([contenido], scroll=ft.ScrollMode.AUTO, tight=True),
            width=w,
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
    nombre = _campo_texto("Nombre de la institución", "Nombre de la institución")
    direccion = _campo_texto("Dirección", "Dirección completa", multiline=True)
    telefono = _campo_texto("Teléfono", "Teléfono")

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
    email = _campo_texto("Correo electrónico", "Correo electrónico")
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
# Figma "Nueva Brigada": Nombre, Descripción, Coordinador, Color Identificador; Cancelar / Crear


def abrir_form_brigada_registrar(page: ft.Page, on_success=None, usuario_actual=None):
    """
    Formulario 'Nueva Brigada': contenedor compacto.
    - Si es profesor: asigna automáticamente profesor_id
    - Si es admin: muestra selector de profesor (opcional)
    """
    usuario_actual = usuario_actual or {}
    rol_usuario = usuario_actual.get("rol", "")
    id_usuario = usuario_actual.get("id")
    
    pad = PADDING_NUEVA_BRIGADA
    nombre = ft.TextField(
        hint_text="Nombre de la brigada",
        expand=True,
        **_CAMPO_BASE,
    )
    descripcion = ft.TextField(
        hint_text="Descripción de las funciones de la brigada",
        multiline=True,
        min_lines=4,
        max_lines=6,
        expand=True,
        content_padding=ft.Padding(14, 20),
        border_color=COLOR_BORDE,
        focused_border_color=COLOR_PRIMARIO,
        border_radius=RADIO,
        text_size=14,
        color=COLOR_TEXTO,
        cursor_color=COLOR_PRIMARIO,
    )
    coordinador = ft.TextField(
        hint_text="Nombre del coordinador",
        expand=True,
        **_CAMPO_BASE,
    )
    
    # Selector de profesor (solo para admins)
    selector_profesor = None
    if es_admin(rol_usuario):
        try:
            profesores = listar_profesores_institucion(1)  # TODO: obtener institucion_id del usuario
            if profesores:
                selector_profesor = ft.Dropdown(
                    hint_text="Seleccione un profesor (opcional)",
                    options=[ft.dropdown.Option(key=str(p["idUsuario"]), text=f"{p['nombre']} {p['apellido']}") for p in profesores],
                    border_color=COLOR_BORDE,
                    focused_border_color=COLOR_PRIMARIO,
                    text_size=14,
                    color=COLOR_TEXTO,
                    content_padding=ft.Padding(12, 14),
                    border_radius=RADIO,
                    dense=True,
                )
        except Exception:
            pass

    # Color identificador: swatches más anchos (80x48), 2 filas x 4 columnas
    colores_figma = [
        "#2563eb", "#f97316", "#22c55e", "#a855f7",
        "#ec4899", "#eab308", "#06b6d4", "#64748b",
    ]
    color_seleccionado = {"value": colores_figma[0]}
    contenedores_color = []
    ANCHO_SWATCH = 80
    ALTO_SWATCH = 48
    ESP_SWATCH = 10

    def make_click_color(idx, c):
        def _(e):
            color_seleccionado["value"] = c
            for i, cc in enumerate(contenedores_color):
                cc.border = ft.Border.all(3, COLOR_PRIMARIO if i == idx else COLOR_BORDE)
            page.update()
        return _

    for i, c in enumerate(colores_figma):
        contenedores_color.append(
            ft.Container(
                width=ANCHO_SWATCH,
                height=ALTO_SWATCH,
                border_radius=10,
                bgcolor=c,
                border=ft.Border.all(3, COLOR_PRIMARIO if i == 0 else COLOR_BORDE),
                on_click=make_click_color(i, c),
            )
        )
    fila1 = ft.Row(contenedores_color[0:4], spacing=ESP_SWATCH)
    fila2 = ft.Row(contenedores_color[4:8], spacing=ESP_SWATCH)
    grid_colores = ft.Column([fila1, ft.Container(height=ESP_SWATCH), fila2], spacing=0)

    def on_crear(_):
        # Validar nombre obligatorio
        if not nombre.value or not nombre.value.strip():
            page.snack_bar = ft.SnackBar(ft.Text("El nombre de la brigada es obligatorio"), bgcolor="#ef4444")
            page.snack_bar.open = True
            page.update()
            return
        
        # Determinar profesor_id
        profesor_id = None
        if es_profesor(rol_usuario) and id_usuario:
            # Profesor crea su propia brigada
            profesor_id = id_usuario
        elif es_admin(rol_usuario) and selector_profesor and selector_profesor.value:
            # Admin asigna a un profesor
            profesor_id = int(selector_profesor.value)
        
        try:
            insertar_brigada(
                nombre=nombre.value.strip(),
                descripcion=descripcion.value or None,
                coordinador=coordinador.value or None,
                color_identificador=color_seleccionado["value"],
                profesor_id=profesor_id,
            )
            _cerrar_dialogo(page)
            page.snack_bar = ft.SnackBar(ft.Text("¡Brigada creada correctamente!"), bgcolor="#22c55e")
            page.snack_bar.open = True
            if on_success:
                on_success()
        except Exception as ex:
            msg = str(ex)
            if "Unknown column" in msg or "descripcion" in msg:
                msg = "Ejecuta antes: database/migrate_brigada_campos.sql"
            page.snack_bar = ft.SnackBar(ft.Text(f"Error al crear brigada: {msg}"), bgcolor="#ef4444")
            page.snack_bar.open = True
        page.update()

    fila_titulo = ft.Row(
        [
            ft.Text("Nueva Brigada", size=18, weight="w600", color=COLOR_TEXTO),
            ft.Icon(ft.Icons.ADD, size=18, color=COLOR_PRIMARIO),
            ft.Container(expand=True),
            ft.IconButton(
                icon=ft.Icons.CLOSE,
                icon_size=20,
                icon_color=COLOR_TEXTO_SEC,
                on_click=lambda e: _cerrar_dialogo(e.page),
                style=ft.ButtonStyle(padding=4),
                width=32,
                height=32,
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    campos_formulario = [
        fila_titulo,
        ft.Container(height=16),
        _campo_con_titulo("Nombre de la Brigada *", nombre),
        _campo_con_titulo("Descripción", descripcion),
        _campo_con_titulo("Coordinador", coordinador),
    ]
    
    # Agregar selector de profesor solo si es admin y hay profesores disponibles
    if selector_profesor:
        campos_formulario.append(_campo_con_titulo("Asignar a Profesor (opcional)", selector_profesor))
    
    campos_formulario.extend([
        ft.Text("Color Identificador", size=14, weight="w500", color=COLOR_TEXTO),
        ft.Container(height=8),
        grid_colores,
    ])
    
    inner_column = ft.Column(campos_formulario, spacing=0)
    contenido = ft.Container(
        content=inner_column,
        padding=pad,
        width=ANCHO_FORM_NUEVA_BRIGADA,
    )

    # Botones normales redondeados, “gorditos”, ancho mínimo (toque final tipo Figma)
    estilo_cancelar = ft.ButtonStyle(
        color=COLOR_CANCELAR,
        padding=ft.Padding(24, 20),
        shape=ft.RoundedRectangleBorder(radius=16),
    )
    estilo_crear = ft.ButtonStyle(
        bgcolor=COLOR_PRIMARIO_CLARO,
        color="white",
        padding=ft.Padding(24, 20),
        shape=ft.RoundedRectangleBorder(radius=16),
    )
    btn_cancelar = ft.OutlinedButton(
        "Cancelar",
        style=estilo_cancelar,
        width=140,
        on_click=lambda e: _cerrar_dialogo(e.page),
    )
    btn_crear = ft.FilledButton(
        "Crear",
        style=estilo_crear,
        width=140,
        on_click=on_crear,
    )

    dialogo = ft.AlertDialog(
        modal=True,
        bgcolor=COLOR_CARD,
        title=None,
        content=ft.Container(
            content=ft.Column([contenido], scroll=ft.ScrollMode.AUTO, tight=True),
            width=ANCHO_FORM_NUEVA_BRIGADA,
            bgcolor=COLOR_CARD,
        ),
        actions=[btn_cancelar, btn_crear],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    _abrir_dialogo(page, dialogo)


def abrir_form_brigada_modificar(page: ft.Page, brigada=None, on_success=None):
    """Abre el formulario de modificar brigada. Si brigada (dict) se pasa, precarga datos y al guardar actualiza en BD y llama on_success()."""
    id_brigada_val = brigada.get("idBrigada") if brigada else None
    nombre = ft.TextField(
        label="Nombre",
        hint_text="Nombre de la brigada",
        value=brigada.get("nombre_brigada", "") if brigada else "",
        **_CAMPO_BASE,
    )
    area_accion = ft.TextField(
        label="Área de acción",
        hint_text="Área de acción",
        value=brigada.get("area_accion", "") if brigada else "",
        **_CAMPO_BASE,
    )
    descripcion = ft.TextField(
        label="Descripción",
        hint_text="Descripción (opcional)",
        value=brigada.get("descripcion") or "" if brigada else "",
        multiline=True,
        min_lines=2,
        **_CAMPO_BASE,
    )
    coordinador = ft.TextField(
        label="Coordinador",
        hint_text="Nombre del coordinador",
        value=brigada.get("coordinador") or "" if brigada else "",
        **_CAMPO_BASE,
    )

    def on_guardar(_):
        if not id_brigada_val:
            page.snack_bar = ft.SnackBar(ft.Text("Error: no se identificó la brigada"))
            page.snack_bar.open = True
            page.update()
            return
        nom = (nombre.value or "").strip()
        if not nom:
            page.snack_bar = ft.SnackBar(ft.Text("El nombre es obligatorio"), bgcolor="#ef4444")
            page.snack_bar.open = True
            page.update()
            return
        try:
            actualizar_brigada(
                id_brigada=id_brigada_val,
                nombre=nom,
                area_accion=(area_accion.value or "").strip() or None,
                descripcion=(descripcion.value or "").strip() or None,
                coordinador=(coordinador.value or "").strip() or None,
            )
            _cerrar_dialogo(page)
            page.snack_bar = ft.SnackBar(ft.Text("¡Brigada actualizada correctamente!"), bgcolor="#22c55e")
            page.snack_bar.open = True
            if on_success:
                on_success()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"), bgcolor="#ef4444")
            page.snack_bar.open = True
        page.update()

    contenido = ft.Column(
        [
            ft.Text(f"ID Brigada: {id_brigada_val}", size=13, color=COLOR_TEXTO_SEC),
            ft.Container(height=12),
            nombre,
            ft.Container(height=12),
            area_accion,
            ft.Container(height=12),
            descripcion,
            ft.Container(height=12),
            coordinador,
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


def abrir_form_brigada_eliminar(page: ft.Page, brigada=None, on_success=None):
    """Abre el diálogo de confirmación para eliminar. Si brigada (dict) se pasa, muestra nombre y al confirmar elimina en BD y llama on_success()."""
    id_brigada_val = brigada.get("idBrigada") if brigada else None
    nombre_brigada = (brigada.get("nombre_brigada") or "esta brigada") if brigada else ""

    def on_eliminar(_):
        if not id_brigada_val:
            page.snack_bar = ft.SnackBar(ft.Text("Error: no se identificó la brigada"))
            page.snack_bar.open = True
            page.update()
            return
        err = eliminar_brigada(id_brigada_val)
        if err:
            page.snack_bar = ft.SnackBar(ft.Text(err))
            page.snack_bar.open = True
            page.update()
            return
        _cerrar_dialogo(page)
        page.snack_bar = ft.SnackBar(ft.Text("Brigada eliminada correctamente"), bgcolor="#22c55e")
        page.snack_bar.open = True
        if on_success:
            on_success()
        page.update()

    contenido = ft.Column(
        [
            ft.Text("Eliminar una brigada puede afectar actividades y usuarios asociados. Solo se puede eliminar si no tiene usuarios asignados.", size=13, color=COLOR_TEXTO_SEC),
            ft.Container(height=16),
            ft.Text(f"¿Eliminar la brigada «{nombre_brigada}» (ID {id_brigada_val})?", size=14, weight="w600", color=COLOR_TEXTO),
        ],
        spacing=0,
    )
    dialogo = _dialogo_formulario(page, "Eliminar brigada", contenido, on_guardar=on_eliminar, texto_guardar="Eliminar")
    _abrir_dialogo(page, dialogo)


def abrir_form_brigada_agregar_miembros(page: ft.Page, brigada=None, on_success=None):
    """Abre el diálogo para agregar miembros a una brigada. Lista usuarios de otras brigadas y permite asignarlos a esta."""
    if not brigada:
        page.snack_bar = ft.SnackBar(ft.Text("Error: no se especificó la brigada"))
        page.snack_bar.open = True
        page.update()
        return
    id_brigada = brigada.get("idBrigada")
    nombre_brigada = brigada.get("nombre_brigada") or f"Brigada {id_brigada}"
    try:
        todos = listar_brigadistas()
    except Exception:
        todos = []
    miembros_actuales = [u for u in todos if (u.get("Brigada_idBrigada") or 0) == id_brigada]
    disponibles = [u for u in todos if (u.get("Brigada_idBrigada") or 0) != id_brigada]
    opciones_dropdown = [
        ft.dropdown.Option(
            str(u["idUsuario"]),
            f"{u.get('nombre', '')} {u.get('apellido', '')} — {u.get('nombre_brigada') or 'Sin brigada'}",
        )
        for u in disponibles
    ]
    selector_usuario = ft.Dropdown(
        hint_text="Seleccione un usuario para agregar a esta brigada",
        options=opciones_dropdown,
        border_color=COLOR_BORDE,
        focused_border_color=COLOR_PRIMARIO,
        border_radius=RADIO,
        text_size=14,
        color=COLOR_TEXTO,
        content_padding=_CAMPO_PADDING,
    )

    def on_agregar(_):
        val = selector_usuario.value
        if not val:
            page.snack_bar = ft.SnackBar(ft.Text("Seleccione un usuario"), bgcolor="#ef4444")
            page.snack_bar.open = True
            page.update()
            return
        id_usuario = int(val)
        usuario = obtener_usuario(id_usuario)
        if not usuario:
            page.snack_bar = ft.SnackBar(ft.Text("Usuario no encontrado"), bgcolor="#ef4444")
            page.snack_bar.open = True
            page.update()
            return
        try:
            actualizar_usuario(
                id_usuario,
                nombre=usuario.get("nombre") or "",
                apellido=usuario.get("apellido") or "",
                email=usuario.get("email") or "",
                rol=usuario.get("rol") or "Brigadista",
                brigada_id=id_brigada,
            )
            _cerrar_dialogo(page)
            page.snack_bar = ft.SnackBar(ft.Text("¡Miembro agregado a la brigada!"), bgcolor="#22c55e")
            page.snack_bar.open = True
            if on_success:
                on_success()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"), bgcolor="#ef4444")
            page.snack_bar.open = True
        page.update()

    lista_actuales = ft.Column(
        [
            ft.Text("Miembros actuales", size=14, weight="w600", color=COLOR_TEXTO),
            ft.Container(height=8),
            *(
                [
                    ft.Container(
                        content=ft.Text(f"• {u.get('nombre', '')} {u.get('apellido', '')} ({u.get('email', '')})", size=13, color=COLOR_TEXTO_SEC),
                        padding=ft.Padding(0, 4),
                    )
                    for u in miembros_actuales
                ]
                if miembros_actuales
                else [ft.Text("Ninguno aún.", size=13, color=COLOR_TEXTO_SEC)]
            ),
        ],
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.START,
    )
    bloques_agregar = [
        ft.Text("Usuario a agregar", size=14, weight="w500", color=COLOR_TEXTO),
        ft.Container(height=8),
        selector_usuario,
        ft.Container(height=16),
        ft.Row(
            [
                ft.FilledButton(
                    "Agregar a esta brigada",
                    style=ft.ButtonStyle(bgcolor=COLOR_PRIMARIO, shape=ft.RoundedRectangleBorder(radius=RADIO)),
                    on_click=on_agregar,
                ),
            ],
            alignment=ft.MainAxisAlignment.END,
        ),
    ]
    if not disponibles:
        bloques_agregar = [
            ft.Text("No hay usuarios de otras brigadas para agregar. Cree brigadistas en otras brigadas o regístrelos desde «Brigadistas».", size=13, color=COLOR_TEXTO_SEC),
        ]
    contenido = ft.Column(
        [
            ft.Text(f"Agregar miembros a «{nombre_brigada}». Los usuarios de otras brigadas pueden reasignarse aquí.", size=13, color=COLOR_TEXTO_SEC),
            ft.Container(height=16),
            lista_actuales,
            ft.Container(height=20),
            *bloques_agregar,
        ],
        spacing=0,
    )
    dialogo = ft.AlertDialog(
        modal=True,
        bgcolor=COLOR_CARD,
        title=ft.Text("Agregar miembros", size=18, weight="w600", color=COLOR_TEXTO),
        content=ft.Container(content=contenido, width=440, bgcolor=COLOR_CARD),
        actions=[
            ft.TextButton(
                content=ft.Text("Cerrar", color=COLOR_CANCELAR, weight=ft.FontWeight.W_500),
                style=ft.ButtonStyle(color=COLOR_CANCELAR),
                on_click=lambda e: _cerrar_dialogo(e.page),
            ),
        ],
    )
    _abrir_dialogo(page, dialogo)


# ---------- Nuevo Brigadista (Figma) ----------
def abrir_form_brigadista_registrar(page: ft.Page, on_success=None):
    """Formulario 'Nuevo Brigadista': conectado a BD (Usuario + Brigada)."""
    nombre = ft.TextField(hint_text="Nombre completo", **_CAMPO_BASE)
    grado = ft.TextField(hint_text="Grado (opcional)", **_CAMPO_BASE)
    seccion = ft.TextField(hint_text="Sección (opcional)", **_CAMPO_BASE)
    
    # Selector de rol de brigadista
    rol_brigadista = ft.Dropdown(
        hint_text="Seleccione el rol",
        options=[
            ft.dropdown.Option("Brigadista Jefe", "Jefe de Brigada"),
            ft.dropdown.Option("Brigadista", "Brigadista"),
        ],
        value="Brigadista",  # Por defecto es brigadista normal
        border_color=COLOR_BORDE,
        focused_border_color=COLOR_PRIMARIO,
        border_radius=RADIO,
        text_size=14,
        color=COLOR_TEXTO,
        content_padding=_CAMPO_PADDING,
    )
    
    brigadas_opciones = []
    try:
        for b in listar_brigadas():
            brigadas_opciones.append(ft.dropdown.Option(str(b["idBrigada"]), b["nombre_brigada"] or f"Brigada {b['idBrigada']}"))
    except Exception:
        pass
    brigada = ft.Dropdown(
        hint_text="Seleccione una brigada",
        options=brigadas_opciones,
        border_color=COLOR_BORDE,
        focused_border_color=COLOR_PRIMARIO,
        border_radius=RADIO,
        text_size=14,
        color=COLOR_TEXTO,
        content_padding=_CAMPO_PADDING,
    )
    telefono = ft.TextField(hint_text="Teléfono (opcional)", **_CAMPO_BASE)
    correo = ft.TextField(hint_text="Correo electrónico", **_CAMPO_BASE)
    contrasena = ft.TextField(hint_text="Contraseña (mín. 6 caracteres)", password=True, **_CAMPO_BASE)

    fila_grado_seccion = ft.Row(
        [
            ft.Container(content=grado, expand=True),
            ft.Container(width=16),
            ft.Container(content=seccion, expand=True),
        ],
        spacing=0,
    )

    contenido = ft.Column(
        [
            _campo_con_titulo("Nombre Completo", nombre),
            ft.Row(
                [
                    ft.Column(
                        [ft.Text("Grado", size=14, weight="w500", color=COLOR_TEXTO), ft.Container(height=8), grado],
                        spacing=0,
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        expand=True,
                    ),
                    ft.Container(width=16),
                    ft.Column(
                        [ft.Text("Sección", size=14, weight="w500", color=COLOR_TEXTO), ft.Container(height=8), seccion],
                        spacing=0,
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        expand=True,
                    ),
                ],
                spacing=0,
            ),
            ft.Container(height=16),
            _campo_con_titulo("Rol en la Brigada", rol_brigadista),
            _campo_con_titulo("Brigada", brigada),
            _campo_con_titulo("Teléfono", telefono),
            _campo_con_titulo("Correo Electrónico", correo),
            _campo_con_titulo("Contraseña", contrasena, espaciado_abajo=0),
        ],
        spacing=0,
    )

    def on_agregar(_):
        nom = (nombre.value or "").strip()
        email_val = (correo.value or "").strip().lower()
        pwd = (contrasena.value or "").strip()
        brigada_id_val = brigada.value
        if not nom:
            page.snack_bar = ft.SnackBar(ft.Text("Nombre completo es obligatorio"), bgcolor="#ef4444")
            page.snack_bar.open = True
            page.update()
            return
        if not email_val:
            page.snack_bar = ft.SnackBar(ft.Text("Correo electrónico es obligatorio"), bgcolor="#ef4444")
            page.snack_bar.open = True
            page.update()
            return
        if not pwd or len(pwd) < 6:
            page.snack_bar = ft.SnackBar(ft.Text("La contraseña debe tener al menos 6 caracteres"), bgcolor="#ef4444")
            page.snack_bar.open = True
            page.update()
            return
        if not brigada_id_val:
            page.snack_bar = ft.SnackBar(ft.Text("Seleccione una brigada"), bgcolor="#ef4444")
            page.snack_bar.open = True
            page.update()
            return
        if email_ya_existe(email_val):
            page.snack_bar = ft.SnackBar(ft.Text("Ese correo ya está registrado"), bgcolor="#ef4444")
            page.snack_bar.open = True
            page.update()
            return
        try:
            partes = nom.split(None, 1)
            nombre_parte = partes[0] if partes else "Usuario"
            apellido_parte = partes[1] if len(partes) > 1 else ""
            # Usar el rol seleccionado (Brigadista Jefe o Brigadista)
            rol_seleccionado = rol_brigadista.value or "Brigadista"
            crear_usuario(
                nombre=nombre_parte,
                apellido=apellido_parte,
                email=email_val,
                contrasena_plana=pwd,
                rol=rol_seleccionado,
                brigada_id=int(brigada_id_val),
            )
            _cerrar_dialogo(page)
            page.snack_bar = ft.SnackBar(ft.Text("¡Brigadista registrado correctamente!"), bgcolor="#22c55e")
            page.snack_bar.open = True
            if on_success:
                on_success()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"), bgcolor="#ef4444")
            page.snack_bar.open = True
        page.update()

    dialogo = ft.AlertDialog(
        modal=True,
        bgcolor=COLOR_CARD,
        title=ft.Text("Nuevo Brigadista", size=18, weight="w600", color=COLOR_TEXTO),
        content=ft.Container(
            content=ft.Column([contenido], scroll=ft.ScrollMode.AUTO, tight=True),
            width=ANCHO_FORM,
            height=ALTURA_MAX_FORM,
            bgcolor=COLOR_CARD,
        ),
        actions=[
            ft.TextButton(content=ft.Text("Cancelar", color=COLOR_CANCELAR), on_click=lambda e: _cerrar_dialogo(e.page)),
            ft.FilledButton("Agregar Brigadista", style=ft.ButtonStyle(bgcolor=COLOR_PRIMARIO), on_click=on_agregar),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    page.show_dialog(dialogo)


def abrir_form_brigadista_modificar(page: ft.Page, brigadista=None, on_success=None):
    """Abre el formulario para editar un brigadista (Usuario). Precarga datos y actualiza en BD."""
    if not brigadista:
        page.snack_bar = ft.SnackBar(ft.Text("Error: no se pasó el brigadista"))
        page.snack_bar.open = True
        page.update()
        return
    id_val = brigadista.get("idUsuario")
    nombre = ft.TextField(label="Nombre", value=brigadista.get("nombre") or "", **_CAMPO_BASE)
    apellido = ft.TextField(label="Apellido", value=brigadista.get("apellido") or "", **_CAMPO_BASE)
    correo = ft.TextField(label="Correo electrónico", value=brigadista.get("email") or "", **_CAMPO_BASE)
    rol = ft.Dropdown(
        label="Rol",
        value=brigadista.get("rol") or "Brigadista",
        options=[
            ft.dropdown.Option("Brigadista Jefe", "Jefe de Brigada"),
            ft.dropdown.Option("Brigadista", "Brigadista"),
            ft.dropdown.Option("Profesor", "Profesor"),
            ft.dropdown.Option("Coordinador", "Coordinador"),
            ft.dropdown.Option("Directivo", "Directivo"),
        ],
        **_CAMPO_BASE,
    )
    brigadas_opciones = []
    try:
        for b in listar_brigadas():
            brigadas_opciones.append(ft.dropdown.Option(str(b["idBrigada"]), b["nombre_brigada"] or f"Brigada {b['idBrigada']}"))
    except Exception:
        pass
    brigada = ft.Dropdown(
        label="Brigada",
        value=str(brigadista.get("Brigada_idBrigada") or ""),
        options=brigadas_opciones,
        **_CAMPO_BASE,
    )

    def on_guardar(_):
        nom = (nombre.value or "").strip()
        ape = (apellido.value or "").strip()
        email_val = (correo.value or "").strip().lower()
        if not nom:
            page.snack_bar = ft.SnackBar(ft.Text("El nombre es obligatorio"), bgcolor="#ef4444")
            page.snack_bar.open = True
            page.update()
            return
        if not email_val:
            page.snack_bar = ft.SnackBar(ft.Text("El correo es obligatorio"), bgcolor="#ef4444")
            page.snack_bar.open = True
            page.update()
            return
        brigada_id_val = brigada.value
        if not brigada_id_val:
            page.snack_bar = ft.SnackBar(ft.Text("Seleccione una brigada"), bgcolor="#ef4444")
            page.snack_bar.open = True
            page.update()
            return
        try:
            actualizar_usuario(
                id_usuario=id_val,
                nombre=nom,
                apellido=ape,
                email=email_val,
                rol=(rol.value or "Brigadista"),
                brigada_id=int(brigada_id_val),
            )
            _cerrar_dialogo(page)
            page.snack_bar = ft.SnackBar(ft.Text("¡Brigadista actualizado correctamente!"), bgcolor="#22c55e")
            page.snack_bar.open = True
            if on_success:
                on_success()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"), bgcolor="#ef4444")
            page.snack_bar.open = True
        page.update()

    contenido = ft.Column(
        [ft.Text(f"ID: {id_val}", size=13, color=COLOR_TEXTO_SEC), ft.Container(height=12), nombre, apellido, correo, rol, brigada],
        spacing=12,
    )
    dialogo = _dialogo_formulario(page, "Modificar brigadista", contenido, on_guardar=on_guardar)
    _abrir_dialogo(page, dialogo)


def abrir_form_brigadista_eliminar(page: ft.Page, brigadista=None, on_success=None):
    """Confirmación para eliminar un brigadista (Usuario)."""
    if not brigadista:
        page.snack_bar = ft.SnackBar(ft.Text("Error: no se pasó el brigadista"))
        page.snack_bar.open = True
        page.update()
        return
    id_val = brigadista.get("idUsuario")
    nombre_completo = f"{brigadista.get('nombre') or ''} {brigadista.get('apellido') or ''}".strip() or brigadista.get("email") or "este usuario"

    def on_eliminar(_):
        err = eliminar_usuario(id_val)
        if err:
            page.snack_bar = ft.SnackBar(ft.Text(err))
            page.snack_bar.open = True
            page.update()
            return
        _cerrar_dialogo(page)
        page.snack_bar = ft.SnackBar(ft.Text("Brigadista eliminado correctamente"), bgcolor="#22c55e")
        page.snack_bar.open = True
        if on_success:
            on_success()
        page.update()

    contenido = ft.Column(
        [
            ft.Text(f"¿Eliminar a {nombre_completo} (ID {id_val})? Esta acción no se puede deshacer.", size=14, color=COLOR_TEXTO),
        ],
        spacing=0,
    )
    dialogo = _dialogo_formulario(page, "Eliminar brigadista", contenido, on_guardar=on_eliminar, texto_guardar="Eliminar")
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
    valor = _campo_texto("Valor", "Valor numérico")
    tipo = _campo_texto("Tipo de indicador", "Tipo de indicador")
    unidad = _campo_texto("Unidad", "Unidad de medida")
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


# ---------- Nuevo Turno (Figma) ----------
def abrir_form_turno(page: ft.Page):
    """Cada campo con su título visible."""
    brigada = ft.Dropdown(
        hint_text="Seleccione una brigada",
        options=[ft.dropdown.Option("Brigada Ambiental")],
        border_color=COLOR_BORDE,
        focused_border_color=COLOR_PRIMARIO,
        border_radius=RADIO,
        content_padding=_CAMPO_PADDING,
    )
    fecha = ft.TextField(hint_text="dd/mm/aaaa", **_CAMPO_BASE)
    hora_ini = ft.TextField(hint_text="--:--", **_CAMPO_BASE)
    hora_fin = ft.TextField(hint_text="--:--", **_CAMPO_BASE)
    ubicacion = ft.TextField(hint_text="Ubicación del turno", **_CAMPO_BASE)
    notas = ft.TextField(
        hint_text="Detalles adicionales del turno...",
        multiline=True,
        min_lines=3,
        max_lines=5,
        **_CAMPO_BASE,
    )

    fila_horas = ft.Row(
        [
            ft.Column([ft.Text("Hora Inicio", size=14, weight="w500", color=COLOR_TEXTO), ft.Container(height=8), hora_ini], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.START, expand=True),
            ft.Container(width=16),
            ft.Column([ft.Text("Hora Fin", size=14, weight="w500", color=COLOR_TEXTO), ft.Container(height=8), hora_fin], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.START, expand=True),
        ],
        spacing=0,
    )

    contenido = ft.Column(
        [
            _campo_con_titulo("Brigada", brigada),
            _campo_con_titulo("Fecha", fecha),
            fila_horas,
            ft.Container(height=16),
            _campo_con_titulo("Ubicación", ubicacion),
            _campo_con_titulo("Notas", notas, espaciado_abajo=0),
        ],
        spacing=0,
    )

    def on_crear(_):
        page.pop_dialog()
        page.snack_bar = ft.SnackBar(ft.Text("Turno creado (pendiente conectar BD)"))
        page.snack_bar.open = True
        page.update()

    dialogo = ft.AlertDialog(
        modal=True,
        bgcolor=COLOR_CARD,
        title=ft.Row(
            [
                ft.Text("Nuevo Turno", size=18, weight="w600", color=COLOR_TEXTO),
                ft.Container(expand=True),
                ft.IconButton(icon=ft.Icons.CLOSE, on_click=lambda e: _cerrar_dialogo(e.page)),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        content=ft.Container(
            content=ft.Column([contenido], scroll=ft.ScrollMode.AUTO, tight=True),
            width=ANCHO_FORM,
            height=ALTURA_MAX_FORM,
            bgcolor=COLOR_CARD,
        ),
        actions=[
            ft.TextButton(content=ft.Text("Cancelar", color=COLOR_CANCELAR), on_click=lambda e: _cerrar_dialogo(e.page)),
            ft.FilledButton("Crear Turno", style=ft.ButtonStyle(bgcolor=COLOR_PRIMARIO), on_click=on_crear),
        ],
    )
    page.show_dialog(dialogo)


# ---------- Nuevo Reporte de Incidente (Figma) ----------
def abrir_form_nuevo_reporte(page: ft.Page):
    """Cada campo con su título visible."""
    titulo_inc = ft.TextField(hint_text="Resumen breve del incidente", **_CAMPO_BASE)
    desc = ft.TextField(
        hint_text="Describe lo sucedido con detalle...",
        multiline=True,
        min_lines=3,
        max_lines=6,
        content_padding=ft.Padding(14, 20),
        border_color=COLOR_BORDE,
        focused_border_color=COLOR_PRIMARIO,
        border_radius=RADIO,
        text_size=14,
        color=COLOR_TEXTO,
        cursor_color=COLOR_PRIMARIO,
    )
    brigada = ft.Dropdown(
        hint_text="Seleccione una brigada",
        options=[ft.dropdown.Option("Brigada Ambiental")],
        border_color=COLOR_BORDE,
        focused_border_color=COLOR_PRIMARIO,
        border_radius=RADIO,
        content_padding=_CAMPO_PADDING,
    )
    ubicacion = ft.TextField(hint_text="Lugar donde ocurrió el incidente", **_CAMPO_BASE)
    prioridad = ft.Dropdown(
        hint_text="Seleccione prioridad",
        options=[
            ft.dropdown.Option("Baja - Situación menor"),
            ft.dropdown.Option("Media"),
            ft.dropdown.Option("Alta - Requiere atención inmediata"),
        ],
        border_color=COLOR_BORDE,
        focused_border_color=COLOR_PRIMARIO,
        border_radius=RADIO,
        content_padding=_CAMPO_PADDING,
    )

    contenido = ft.Column(
        [
            _campo_con_titulo("Título del Incidente", titulo_inc),
            _campo_con_titulo("Descripción Detallada", desc),
            _campo_con_titulo("Brigada Involucrada", brigada),
            _campo_con_titulo("Ubicación", ubicacion),
            _campo_con_titulo("Nivel de Prioridad", prioridad, espaciado_abajo=0),
        ],
        spacing=0,
    )

    def on_crear(_):
        page.pop_dialog()
        page.snack_bar = ft.SnackBar(ft.Text("Reporte creado (pendiente conectar BD)"))
        page.snack_bar.open = True
        page.update()

    dialogo = ft.AlertDialog(
        modal=True,
        bgcolor=COLOR_CARD,
        title=ft.Text("Nuevo Reporte de Incidente", size=18, weight="w600", color=COLOR_TEXTO),
        content=ft.Container(
            content=ft.Column([contenido], scroll=ft.ScrollMode.AUTO, tight=True),
            width=ANCHO_FORM,
            height=ALTURA_MAX_FORM,
            bgcolor=COLOR_CARD,
        ),
        actions=[
            ft.TextButton(content=ft.Text("Cancelar", color=COLOR_CANCELAR), on_click=lambda e: _cerrar_dialogo(e.page)),
            ft.FilledButton("Crear Reporte", style=ft.ButtonStyle(bgcolor=COLOR_PRIMARIO), on_click=on_crear),
        ],
    )
    page.show_dialog(dialogo)
