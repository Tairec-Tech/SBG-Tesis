"""
Vistas del SGB — Estructura según Diagrama HIPO.
Módulos: 2.0 Instituciones, 3.0 Usuarios, 4.0 Brigadas, 5.0 Actividades,
         6.0 Reportes, 7.0 Indicadores ambientales, 8.0 Utilidades.
"""

import flet as ft

from forms import (
    abrir_form_actividad_consultar,
    abrir_form_actividad_eliminar,
    abrir_form_actividad_modificar,
    abrir_form_actividad_planificar,
    abrir_form_actividad_registrar,
    abrir_form_brigada_asignar,
    abrir_form_brigada_consultar,
    abrir_form_brigada_eliminar,
    abrir_form_brigada_miembros,
    abrir_form_brigada_modificar,
    abrir_form_brigada_registrar,
    abrir_form_indicador_consultar,
    abrir_form_indicador_eliminar,
    abrir_form_indicador_modificar,
    abrir_form_indicador_registrar,
    abrir_form_indicador_resumen,
    abrir_form_institucion_consultar,
    abrir_form_institucion_eliminar,
    abrir_form_institucion_modificar,
    abrir_form_institucion_registrar,
    abrir_form_reporte_consultar,
    abrir_form_reporte_eliminar,
    abrir_form_reporte_modificar,
    abrir_form_reporte_registrar,
    abrir_form_usuario_consultar,
    abrir_form_usuario_eliminar,
    abrir_form_usuario_modificar,
    abrir_form_usuario_registrar,
    abrir_dialogo_acerca_de,
    abrir_dialogo_importar_bd,
    abrir_dialogo_legal,
    abrir_dialogo_manual,
)

# Paleta y diseño (look profesional, inspirado en dashboards modernos)
COLOR_PRIMARIO = "#2563eb"
COLOR_TEXTO = "#1e293b"
COLOR_TEXTO_SEC = "#64748b"
COLOR_BORDE = "#e2e8f0"
COLOR_FONDO = "#f8fafc"
COLOR_CARD = "#ffffff"
RADIO = 14
PADDING = 24


def _sombra_suave():
    return ft.BoxShadow(
        blur_radius=20,
        spread_radius=-4,
        color=ft.Colors.with_opacity(0.06, "black"),
        offset=ft.Offset(0, 4),
    )


def _sombra_card():
    """Sombra más marcada para tarjetas principales."""
    return [
        ft.BoxShadow(blur_radius=24, spread_radius=-6, color=ft.Colors.with_opacity(0.08, "black"), offset=ft.Offset(0, 6)),
    ]


def _tarjeta_accion(icono, titulo, descripcion, page: ft.Page, on_acceder=None):
    """Tarjeta de acción para Registrar/Modificar/Consultar/Eliminar. on_acceder(page) abre el formulario."""
    return ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Icon(icono, color=COLOR_PRIMARIO, size=28),
                    width=52,
                    height=52,
                    border_radius=12,
                    bgcolor=ft.Colors.with_opacity(0.1, COLOR_PRIMARIO),
                    alignment=ft.Alignment.CENTER,
                ),
                ft.Container(height=16),
                ft.Text(titulo, size=16, weight="w600", color=COLOR_TEXTO),
                ft.Container(height=6),
                ft.Text(descripcion, size=13, color=COLOR_TEXTO_SEC),
                ft.Container(height=16),
                ft.FilledButton(
                    content=ft.Text("Acceder", size=14),
                    style=ft.ButtonStyle(
                        color="white",
                        bgcolor=COLOR_PRIMARIO,
                        padding=ft.Padding.symmetric(horizontal=20, vertical=12),
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                    on_click=(lambda p, fn: lambda e: fn(p))(page, on_acceder) if on_acceder else None,  # cierre por valor para que cada botón tenga su callback
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.START,
            spacing=0,
        ),
        bgcolor=COLOR_CARD,
        padding=PADDING,
        border_radius=RADIO,
        border=ft.Border.all(1, COLOR_BORDE),
        shadow=_sombra_suave(),
        width=280,
    )


def _tarjeta_estadistica(titulo, valor, icono, color_acento):
    """Tarjeta de estadística para el dashboard — estilo profesional."""
    return ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Icon(icono, color=color_acento, size=28),
                            width=48,
                            height=48,
                            border_radius=12,
                            bgcolor=ft.Colors.with_opacity(0.14, color_acento),
                            alignment=ft.Alignment.CENTER,
                        ),
                        ft.Container(width=16),
                        ft.Text(titulo, size=12, color=COLOR_TEXTO_SEC, weight="w500", no_wrap=False),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                ft.Container(height=12),
                ft.Text(str(valor), size=32, weight="bold", color=COLOR_TEXTO),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.START,
            spacing=0,
        ),
        bgcolor=COLOR_CARD,
        padding=20,
        border_radius=RADIO,
        border=ft.Border.all(1, COLOR_BORDE),
        shadow=_sombra_card(),
        width=260,
    )


def _encabezado_vista(titulo, subtitulo):
    """Encabezado estándar de cada vista de módulo."""
    return ft.Column(
        [
            ft.Text(titulo, size=24, weight="bold", color=COLOR_TEXTO),
            ft.Container(height=6),
            ft.Text(subtitulo, size=15, color=COLOR_TEXTO_SEC),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.START,
        spacing=0,
    )


def _fila_actividad(icono, texto, tiempo):
    """Una fila de actividad reciente."""
    return ft.Container(
        content=ft.Row(
            [
                ft.Container(
                    content=ft.Icon(icono, color=COLOR_PRIMARIO, size=20),
                    width=40,
                    height=40,
                    border_radius=8,
                    bgcolor=ft.Colors.with_opacity(0.1, COLOR_PRIMARIO),
                    alignment=ft.Alignment.CENTER,
                ),
                ft.Container(width=12),
                ft.Column(
                    [
                        ft.Text(texto, size=14, weight="w500", color=COLOR_TEXTO),
                        ft.Text(tiempo, size=12, color=COLOR_TEXTO_SEC),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                    spacing=2,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
        ),
        padding=ft.Padding.symmetric(vertical=12, horizontal=0),
        border=ft.Border(bottom=ft.BorderSide(1, COLOR_BORDE)),
    )


def _fila_informe(titulo, fecha):
    """Una fila de informe reciente."""
    return ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.DESCRIPTION_OUTLINED, color=COLOR_TEXTO_SEC, size=20),
                ft.Container(width=12),
                ft.Column(
                    [
                        ft.Text(titulo, size=14, weight="w500", color=COLOR_TEXTO),
                        ft.Text(fecha, size=12, color=COLOR_TEXTO_SEC),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                    spacing=2,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
        ),
        padding=ft.Padding.symmetric(vertical=12, horizontal=0),
        border=ft.Border(bottom=ft.BorderSide(1, COLOR_BORDE)),
    )


def _minicard_acceso(icono, etiqueta):
    """Mini-tarjeta de acceso rápido — estilo profesional con borde y sombra."""
    return ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Icon(icono, color=COLOR_PRIMARIO, size=26),
                    width=48,
                    height=48,
                    border_radius=12,
                    bgcolor=ft.Colors.with_opacity(0.1, COLOR_PRIMARIO),
                    alignment=ft.Alignment.CENTER,
                ),
                ft.Container(height=12),
                ft.Text(etiqueta, size=14, weight="w600", color=COLOR_TEXTO),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
        ),
        width=140,
        padding=20,
        bgcolor=COLOR_CARD,
        border_radius=RADIO,
        border=ft.Border.all(1, COLOR_BORDE),
        shadow=_sombra_suave(),
        alignment=ft.Alignment.CENTER,
    )


def _titulo_seccion(icono, texto):
    """Título de sección con icono — estilo dashboard profesional."""
    return ft.Row(
        [
            ft.Container(
                content=ft.Icon(icono, color=COLOR_PRIMARIO, size=20),
                width=36,
                height=36,
                border_radius=10,
                bgcolor=ft.Colors.with_opacity(0.1, COLOR_PRIMARIO),
                alignment=ft.Alignment.CENTER,
            ),
            ft.Container(width=12),
            ft.Text(texto, size=17, weight="w600", color=COLOR_TEXTO),
        ],
        alignment=ft.MainAxisAlignment.START,
    )


def _build_dashboard(page: ft.Page) -> ft.Control:
    """Vista inicial: bienvenida, estadísticas, actividad reciente, informes y accesos rápidos."""
    return ft.Container(
        content=ft.Column(
            [
                # Header tipo "Hola, Bienvenido" — limpio y profesional
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Container(
                                content=ft.Icon(ft.Icons.DASHBOARD_ROUNDED, color=COLOR_PRIMARIO, size=28),
                                width=52,
                                height=52,
                                border_radius=14,
                                bgcolor=ft.Colors.with_opacity(0.1, COLOR_PRIMARIO),
                                alignment=ft.Alignment.CENTER,
                            ),
                            ft.Container(width=20),
                            ft.Column(
                                [
                                    ft.Text("Hola, Bienvenido", size=15, color=COLOR_TEXTO_SEC, weight="w500"),
                                    ft.Container(height=4),
                                    ft.Text("Sistema de Brigadas Escolares — Municipio Maracaibo", size=20, weight="bold", color=COLOR_TEXTO),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.START,
                                spacing=0,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    padding=ft.Padding.symmetric(vertical=24, horizontal=28),
                    bgcolor=COLOR_CARD,
                    border_radius=RADIO,
                    border=ft.Border.all(1, COLOR_BORDE),
                    shadow=_sombra_card(),
                ),
                ft.Container(height=32),
                # Estadísticas generales
                _titulo_seccion(ft.Icons.ANALYTICS_OUTLINED, "Estadísticas generales"),
                ft.Container(height=16),
                ft.Container(
                    content=ft.Row(
                        [
                            _tarjeta_estadistica("Instituciones", "0", ft.Icons.SCHOOL_OUTLINED, COLOR_PRIMARIO),
                            _tarjeta_estadistica("Brigadas", "0", ft.Icons.GROUPS_OUTLINED, "#0ea5e9"),
                            _tarjeta_estadistica("Actividades pendientes", "0", ft.Icons.EVENT_NOTE_OUTLINED, "#f59e0b"),
                            _tarjeta_estadistica("Reportes este mes", "0", ft.Icons.ASSESSMENT_OUTLINED, "#10b981"),
                        ],
                        spacing=20,
                        wrap=True,
                    ),
                ),
                ft.Container(height=32),
                # Actividad reciente + Informes recientes
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Row(
                                        [
                                            ft.Icon(ft.Icons.HISTORY, color=COLOR_PRIMARIO, size=20),
                                            ft.Container(width=10),
                                            ft.Text("Actividad reciente", size=16, weight="w600", color=COLOR_TEXTO),
                                        ],
                                        alignment=ft.MainAxisAlignment.START,
                                    ),
                                    ft.Container(height=20),
                                    _fila_actividad(ft.Icons.SCHOOL_OUTLINED, "Ninguna institución registrada aún", "Conecte la BD para ver datos"),
                                    _fila_actividad(ft.Icons.GROUPS_OUTLINED, "Ninguna brigada creada aún", "Módulo Brigadas (4.0)"),
                                    _fila_actividad(ft.Icons.EVENT_NOTE_OUTLINED, "Sin actividades planificadas", "Módulo Actividades (5.0)"),
                                    _fila_actividad(ft.Icons.ASSESSMENT_OUTLINED, "Sin reportes generados", "Módulo Reportes (6.0)"),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.START,
                                spacing=0,
                            ),
                            padding=PADDING,
                            bgcolor=COLOR_CARD,
                            border_radius=RADIO,
                            border=ft.Border.all(1, COLOR_BORDE),
                            shadow=_sombra_card(),
                        ),
                        ft.Container(width=24),
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Row(
                                        [
                                            ft.Icon(ft.Icons.DESCRIPTION_OUTLINED, color=COLOR_PRIMARIO, size=20),
                                            ft.Container(width=10),
                                            ft.Text("Informes recientes", size=16, weight="w600", color=COLOR_TEXTO),
                                        ],
                                        alignment=ft.MainAxisAlignment.START,
                                    ),
                                    ft.Container(height=20),
                                    _fila_informe("No hay informes aún", "Genere reportes desde el módulo 6.0"),
                                    _fila_informe("Reportes de impacto", "Disponibles al registrar actividades"),
                                    _fila_informe("Resumen de indicadores", "Módulo Indicadores (7.0)"),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.START,
                                spacing=0,
                            ),
                            padding=PADDING,
                            bgcolor=COLOR_CARD,
                            border_radius=RADIO,
                            border=ft.Border.all(1, COLOR_BORDE),
                            shadow=_sombra_card(),
                        ),
                    ],
                    spacing=0,
                    wrap=True,
                ),
                ft.Container(height=32),
                # Accesos rápidos
                _titulo_seccion(ft.Icons.SPEED_OUTLINED, "Accesos rápidos"),
                ft.Container(height=16),
                ft.Row(
                    [
                        _minicard_acceso(ft.Icons.SCHOOL, "Instituciones"),
                        _minicard_acceso(ft.Icons.PEOPLE, "Usuarios"),
                        _minicard_acceso(ft.Icons.GROUPS, "Brigadas"),
                        _minicard_acceso(ft.Icons.ASSESSMENT, "Reportes"),
                    ],
                    spacing=16,
                    wrap=True,
                ),
                ft.Container(height=40),
            ],
            scroll=ft.ScrollMode.AUTO,
            spacing=0,
        ),
        padding=PADDING,
        bgcolor=COLOR_FONDO,
        alignment=ft.Alignment.TOP_LEFT,
    )


def _build_instituciones(page: ft.Page) -> ft.Control:
    """Gráfico 2.0 — TAB_INSTITUCIONES_EDUCATIVAS."""
    return ft.Container(
        content=ft.Column(
            [
                _encabezado_vista(
                    "Instituciones Educativas (2.0)",
                    "Gestión de instituciones. Entrada: TAB_INSTITUCIONES_EDUCATIVAS. Salida: Información actualizada del sistema.",
                ),
                ft.Container(height=32),
                ft.Row(
                    [
                        _tarjeta_accion(
                            ft.Icons.ADD_CIRCLE_OUTLINED,
                            "Registrar instituciones",
                            "Alta de nuevas instituciones educativas en el sistema.",
                            page,
                            abrir_form_institucion_registrar,
                        ),
                        _tarjeta_accion(
                            ft.Icons.EDIT_OUTLINED,
                            "Modificar instituciones",
                            "Editar datos de instituciones existentes.",
                            page,
                            abrir_form_institucion_modificar,
                        ),
                        _tarjeta_accion(
                            ft.Icons.SEARCH,
                            "Consultar instituciones",
                            "Búsqueda y visualización de instituciones.",
                            page,
                            abrir_form_institucion_consultar,
                        ),
                        _tarjeta_accion(
                            ft.Icons.DELETE_OUTLINED,
                            "Eliminar instituciones",
                            "Baja de instituciones del sistema (con validaciones).",
                            page,
                            abrir_form_institucion_eliminar,
                        ),
                    ],
                    spacing=20,
                    wrap=True,
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            spacing=0,
        ),
        padding=PADDING,
        expand=True,
        bgcolor=COLOR_FONDO,
    )


def _build_usuarios(page: ft.Page) -> ft.Control:
    """Gráfico 3.0 — TAB_USUARIOS. Salida: Información actualizada + Autentificación."""
    return ft.Container(
        content=ft.Column(
            [
                _encabezado_vista(
                    "Usuarios (3.0)",
                    "Gestión de usuarios y roles. Entrada: TAB_USUARIOS. Salida: Información actualizada y autentificación.",
                ),
                ft.Container(height=32),
                ft.Row(
                    [
                        _tarjeta_accion(ft.Icons.PERSON_ADD_OUTLINED, "Registrar usuarios", "Alta de nuevos usuarios.", page, abrir_form_usuario_registrar),
                        _tarjeta_accion(ft.Icons.EDIT_OUTLINED, "Modificar usuarios", "Editar datos y roles de usuarios.", page, abrir_form_usuario_modificar),
                        _tarjeta_accion(ft.Icons.SEARCH, "Consultar usuarios", "Búsqueda y listado de usuarios.", page, abrir_form_usuario_consultar),
                        _tarjeta_accion(ft.Icons.DELETE_OUTLINED, "Eliminar usuarios", "Baja de usuarios del sistema.", page, abrir_form_usuario_eliminar),
                    ],
                    spacing=20,
                    wrap=True,
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            spacing=0,
        ),
        padding=PADDING,
        expand=True,
        bgcolor=COLOR_FONDO,
    )


def _build_brigadas(page: ft.Page) -> ft.Control:
    """Gráfico 4.0 — TAB_BRIGADAS. Proceso: + Asignar. Salida: Información actualizada + Gestionar miembros."""
    return ft.Container(
        content=ft.Column(
            [
                _encabezado_vista(
                    "Brigadas (4.0)",
                    "Gestión de brigadas. Entrada: TAB_BRIGADAS. Salida: Información actualizada y gestión de miembros.",
                ),
                ft.Container(height=32),
                ft.Row(
                    [
                        _tarjeta_accion(ft.Icons.GROUP_ADD_OUTLINED, "Registrar brigadas", "Crear nuevas brigadas.", page, abrir_form_brigada_registrar),
                        _tarjeta_accion(ft.Icons.EDIT_OUTLINED, "Modificar brigadas", "Editar datos de brigadas.", page, abrir_form_brigada_modificar),
                        _tarjeta_accion(ft.Icons.SEARCH, "Consultar brigadas", "Listado y búsqueda de brigadas.", page, abrir_form_brigada_consultar),
                        _tarjeta_accion(ft.Icons.DELETE_OUTLINED, "Eliminar brigadas", "Baja de brigadas.", page, abrir_form_brigada_eliminar),
                        _tarjeta_accion(ft.Icons.ASSIGNMENT_OUTLINED, "Asignar brigadas", "Asignación a instituciones o actividades.", page, abrir_form_brigada_asignar),
                        _tarjeta_accion(ft.Icons.GROUPS_OUTLINED, "Gestionar miembros", "Administrar miembros de cada brigada.", page, abrir_form_brigada_miembros),
                    ],
                    spacing=20,
                    wrap=True,
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            spacing=0,
        ),
        padding=PADDING,
        expand=True,
        bgcolor=COLOR_FONDO,
    )


def _build_actividades(page: ft.Page) -> ft.Control:
    """Gráfico 5.0 — TAB_ACTIVIDAD. Salida: Planificar actividad."""
    return ft.Container(
        content=ft.Column(
            [
                _encabezado_vista(
                    "Actividades (5.0)",
                    "Gestión de actividades y proyectos. Entrada: TAB_ACTIVIDAD. Salida: Planificar actividad.",
                ),
                ft.Container(height=32),
                ft.Row(
                    [
                        _tarjeta_accion(ft.Icons.ADD_CIRCLE_OUTLINED, "Registrar actividad", "Alta de nuevas actividades.", page, abrir_form_actividad_registrar),
                        _tarjeta_accion(ft.Icons.EDIT_OUTLINED, "Modificar actividad", "Editar actividades existentes.", page, abrir_form_actividad_modificar),
                        _tarjeta_accion(ft.Icons.SEARCH, "Consultar actividad", "Búsqueda y detalle de actividades.", page, abrir_form_actividad_consultar),
                        _tarjeta_accion(ft.Icons.DELETE_OUTLINED, "Eliminar actividad", "Baja de actividades.", page, abrir_form_actividad_eliminar),
                        _tarjeta_accion(ft.Icons.CALENDAR_MONTH_OUTLINED, "Planificar actividad", "Planificación y asignación de brigada responsable.", page, abrir_form_actividad_planificar),
                    ],
                    spacing=20,
                    wrap=True,
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            spacing=0,
        ),
        padding=PADDING,
        expand=True,
        bgcolor=COLOR_FONDO,
    )


def _build_reportes(page: ft.Page) -> ft.Control:
    """Gráfico 6.0 — TAB_REPORTES. Salida: Información actualizada + Reportes de impacto."""
    return ft.Container(
        content=ft.Column(
            [
                _encabezado_vista(
                    "Reportes de impacto (6.0)",
                    "Redacción y gestión de reportes. Entrada: TAB_REPORTES. Salida: Información actualizada y reportes de impacto.",
                ),
                ft.Container(height=32),
                ft.Row(
                    [
                        _tarjeta_accion(ft.Icons.ADD_CHART_OUTLINED, "Registrar reportes", "Alta de nuevos reportes.", page, abrir_form_reporte_registrar),
                        _tarjeta_accion(ft.Icons.EDIT_OUTLINED, "Modificar reportes", "Editar reportes existentes.", page, abrir_form_reporte_modificar),
                        _tarjeta_accion(ft.Icons.SEARCH, "Consultar reportes", "Búsqueda y visualización de reportes.", page, abrir_form_reporte_consultar),
                        _tarjeta_accion(ft.Icons.DELETE_OUTLINED, "Eliminar reportes", "Baja de reportes.", page, abrir_form_reporte_eliminar),
                    ],
                    spacing=20,
                    wrap=True,
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            spacing=0,
        ),
        padding=PADDING,
        expand=True,
        bgcolor=COLOR_FONDO,
    )


def _build_indicadores(page: ft.Page) -> ft.Control:
    """Gráfico 7.0 — TAB_INDICADORES_AMBIENTALES. Salida: Resumen total."""
    return ft.Container(
        content=ft.Column(
            [
                _encabezado_vista(
                    "Indicadores ambientales (7.0)",
                    "Gestión de indicadores ambientales. Entrada: TAB_INDICADORES_AMBIENTALES. Salida: Resumen total.",
                ),
                ft.Container(height=32),
                ft.Row(
                    [
                        _tarjeta_accion(ft.Icons.ECO_OUTLINED, "Registrar indicadores", "Alta de indicadores ambientales.", page, abrir_form_indicador_registrar),
                        _tarjeta_accion(ft.Icons.EDIT_OUTLINED, "Modificar indicadores", "Editar indicadores existentes.", page, abrir_form_indicador_modificar),
                        _tarjeta_accion(ft.Icons.SEARCH, "Consultar indicadores", "Búsqueda por actividad o tipo.", page, abrir_form_indicador_consultar),
                        _tarjeta_accion(ft.Icons.DELETE_OUTLINED, "Eliminar indicadores", "Baja de indicadores.", page, abrir_form_indicador_eliminar),
                        _tarjeta_accion(ft.Icons.SUMMARIZE_OUTLINED, "Resumen total", "Vista consolidada y totales.", page, abrir_form_indicador_resumen),
                    ],
                    spacing=20,
                    wrap=True,
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            spacing=0,
        ),
        padding=PADDING,
        expand=True,
        bgcolor=COLOR_FONDO,
    )


def _build_utilidades(page: ft.Page) -> ft.Control:
    """Gráfico 8.0 — TAB_UTILIDADES. Proceso: Acerca de, Manual, Info legal, Importar/restaurar BD."""
    return ft.Container(
        content=ft.Column(
            [
                _encabezado_vista(
                    "Utilidades (8.0)",
                    "Herramientas para el usuario. Entrada: TAB_UTILIDADES. Salida: Información general del sistema.",
                ),
                ft.Container(height=32),
                ft.Row(
                    [
                        _tarjeta_accion(ft.Icons.INFO_OUTLINED, "Acerca de", "Información de la aplicación y versión.", page, abrir_dialogo_acerca_de),
                        _tarjeta_accion(ft.Icons.MENU_BOOK_OUTLINED, "Manual de usuario", "Documentación y guía de uso.", page, abrir_dialogo_manual),
                        _tarjeta_accion(ft.Icons.GAVEL_OUTLINED, "Información legal", "Términos, licencias y créditos.", page, abrir_dialogo_legal),
                        _tarjeta_accion(ft.Icons.RESTORE_OUTLINED, "Importar / restaurar BD", "Respaldo y restauración de base de datos.", page, abrir_dialogo_importar_bd),
                    ],
                    spacing=20,
                    wrap=True,
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            spacing=0,
        ),
        padding=PADDING,
        expand=True,
        bgcolor=COLOR_FONDO,
    )


def _item_menu(icono, etiqueta, seleccionado, on_click):
    """Un ítem del menú lateral."""
    bg = ft.Colors.with_opacity(0.08, COLOR_PRIMARIO) if seleccionado else "transparent"
    borde_izq = ft.BorderSide(3, COLOR_PRIMARIO) if seleccionado else ft.BorderSide(0, "transparent")
    color_txt = COLOR_PRIMARIO if seleccionado else COLOR_TEXTO
    return ft.Container(
        content=ft.Row(
            [
                ft.Icon(icono, color=color_txt, size=22),
                ft.Container(width=12),
                ft.Text(etiqueta, size=14, weight="w500" if seleccionado else "w400", color=color_txt),
            ],
            alignment=ft.MainAxisAlignment.START,
        ),
        padding=ft.Padding.symmetric(vertical=14, horizontal=20),
        border_radius=ft.BorderRadius.only(top_right=8, bottom_right=8),
        border=ft.Border(left=borde_izq),
        bgcolor=bg,
        on_click=on_click,
        data=etiqueta,
    )


def _build_sidebar(
    page: ft.Page,
    contenido_area: ft.Container,
    barra_lateral: ft.Container,
    vista_actual: list,
    on_logout,
):
    """Construye el contenido del menú lateral (para actualizar selección)."""
    def ir(vista_nombre, builder):
        def _(e):
            vista_actual[0] = vista_nombre
            contenido_area.content = builder(page)
            barra_lateral.content = _build_sidebar(page, contenido_area, barra_lateral, vista_actual, on_logout)
            page.update()
        return _

    sel = vista_actual[0]
    items = [
        ("Inicio", ft.Icons.DASHBOARD_OUTLINED, _build_dashboard),
        ("Instituciones (2.0)", ft.Icons.SCHOOL_OUTLINED, _build_instituciones),
        ("Usuarios (3.0)", ft.Icons.PEOPLE_OUTLINED, _build_usuarios),
        ("Brigadas (4.0)", ft.Icons.GROUPS_OUTLINED, _build_brigadas),
        ("Actividades (5.0)", ft.Icons.EVENT_NOTE_OUTLINED, _build_actividades),
        ("Reportes (6.0)", ft.Icons.ASSESSMENT_OUTLINED, _build_reportes),
        ("Indicadores (7.0)", ft.Icons.ECO_OUTLINED, _build_indicadores),
        ("Utilidades (8.0)", ft.Icons.SETTINGS_OUTLINED, _build_utilidades),
    ]
    return ft.Column(
        [
            ft.Container(height=20),
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.SHIELD_ROUNDED, color=COLOR_PRIMARIO, size=28),
                            ft.Container(width=10),
                            ft.Text("SGB", size=18, weight="bold", color=COLOR_TEXTO),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Container(height=6),
                    ft.Text("Brigadas Maracaibo", size=12, color=COLOR_TEXTO_SEC),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
            ),
            ft.Container(height=28),
            ft.Divider(height=1, color=COLOR_BORDE),
            ft.Container(height=16),
        ]
        + [_item_menu(ico, lbl, sel == lbl, ir(lbl, fn)) for lbl, ico, fn in items]
        + [
            ft.Container(expand=True),
            ft.Divider(height=1, color=COLOR_BORDE),
            ft.Container(height=12),
            ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.LOGOUT, color="#dc2626", size=22),
                        ft.Container(width=12),
                        ft.Text("Cerrar sesión", size=14, weight="w500", color="#dc2626"),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                padding=ft.Padding.symmetric(vertical=14, horizontal=20),
                border_radius=8,
                on_click=lambda e: on_logout(),
            ),
            ft.Container(height=20),
        ],
        spacing=0,
        expand=True,
    )


def build_views_content(page: ft.Page, on_logout) -> ft.Control:
    """
    Construye el layout principal post-login: barra lateral HIPO + área de contenido.
    on_logout: callable sin argumentos para volver a la pantalla de login.
    """
    vista_actual = ["Inicio"]
    contenido_area = ft.Container(expand=True, content=_build_dashboard(page), bgcolor=COLOR_FONDO)
    barra_lateral = ft.Container(
        width=260,
        bgcolor=COLOR_CARD,
        border=ft.Border(right=ft.BorderSide(1, COLOR_BORDE)),
        border_radius=ft.BorderRadius.only(top_right=16, bottom_right=16),
        shadow=ft.BoxShadow(
            blur_radius=8,
            spread_radius=0,
            color=ft.Colors.with_opacity(0.06, "black"),
            offset=ft.Offset(2, 0),
        ),
    )
    barra_lateral.content = _build_sidebar(page, contenido_area, barra_lateral, vista_actual, on_logout)

    return ft.Row(
        [
            barra_lateral,
            contenido_area,
        ],
        expand=True,
        spacing=0,
    )
