"""Contenido Educativo — guías y recursos ampliadas por rol de servicio."""

import flet as ft
from theme import (
    COLOR_PRIMARIO,
    COLOR_TEXTO,
    COLOR_TEXTO_SEC,
    COLOR_CARD,
    COLOR_BORDE,
    COLOR_FONDO_VERDE,
    get_sombra_card,
)
from components import titulo_pagina, card_principal

GUIAS_BRIGADAS = [
    {
        "titulo": "Brigada de Convivencia y Paz (Armonía Escolar)",
        "tab_name": "Convivencia y Paz",
        "icon": ft.Icons.HANDSHAKE_OUTLINED,
        "color_base": "#64748b",
        "color_dark": "#475569",
        "proposito": "Erradicar de manera permanente el hostigamiento, el acoso escolar (bullying) y la intolerancia, promoviendo una cultura de igualdad y respeto mutuo.",
        "identificacion": "Brazalete de color BLANCO.",
        "fundamento_legal": "Ley Constitucional Contra el Odio y artículo 32-A de la LOPNNA, referente al derecho al buen trato, convivencia sana y protección integral en el entorno escolar.",
        "mision": "Actuar como una brigada de acompañamiento y prevención que favorece el buen clima escolar, detecta señales tempranas de conflicto, promueve el respeto entre pares y canaliza situaciones reales.",
        "uso_plataforma": "Registrar actividades de convivencia, reportes de incidencias relevantes, seguimiento de situaciones y evidencias de campañas, charlas o mediaciones.",
        "actividad_sugerida": "Círculos de diálogo semanales o quincenales sobre tolerancia, empatía, resolución pacífica de conflictos y comunicación asertiva.",
        "objetivo_formativo": "Desarrollar habilidades de escucha activa, mediación básica, identificación de señales de conflicto y responsabilidad ética en el trato cotidiano.",
        "recomendaciones": [
            "Escuchar primero y emitir juicios después. No tomar partido sin conocer los hechos.",
            "Proteger la dignidad de las personas involucradas.",
            "Escalar oportunamente casos graves, de violencia o amenazas.",
            "Registrar únicamente hechos observables y no opiniones personales en la plataforma."
        ],
        "secciones": [
            {
                "titulo": "Protocolo de actuación",
                "items": [
                    "Detección: Observar señales tempranas de aislamiento o agresiones.",
                    "Abordaje Primario: Aplicar la técnica 'Yo siento, yo necesito'.",
                    "Mediación entre Pares: Actuar como puente de diálogo sin imponer soluciones.",
                    "Reporte: Escalar y registrar eventos que requieran intervención institucional."
                ]
            }
        ]
    },
    {
        "titulo": "Brigada Ecológica (Sustentabilidad en mi Escuela)",
        "tab_name": "Ecológica",
        "icon": ft.Icons.ECO_OUTLINED,
        "color_base": "#059669",
        "color_dark": "#047857",
        "proposito": "Transformar la institución en un modelo de gestión ambiental, promoviendo hábitos de consumo responsable y la soberanía alimentaria desde el aula.",
        "identificacion": "Brazalete de color VERDE.",
        "fundamento_legal": "Marco orientador institucional de educación ambiental y participación estudiantil.",
        "mision": "Ser guardianes de los recursos naturales del plantel y motores de una cultura ambiental sostenible en el tiempo.",
        "uso_plataforma": "Mantener una 'Bitácora Verde' con registros de material reciclado, auditorías de ecoeficiencia, impacto del conuco escolar y evidencias de campañas.",
        "actividad_sugerida": "'Mi Escuela, Mi Primer Ecosistema': diagnosticar un área común, formular e implementar mejoras, registrando los resultados progresivamente.",
        "objetivo_formativo": "Desarrollar hábitos de trabajo colaborativo, cuidado ambiental y medición básica de resultados, aprendiendo la sostenibilidad desde la práctica activa.",
        "recomendaciones": [
            "Evitar limitarse a solo la limpieza; aportar valor organizando y educando.",
            "Traducir las acciones en indicadores simples (kilos de material, aulas auditadas).",
            "Dar continuidad semanal a las acciones, porque el impacto es sumativo.",
            "Involucrar a docentes mediante retos por secciones."
        ],
        "secciones": [
            {
                "titulo": "Funciones detalladas",
                "items": [
                    "Puntos limpios: Supervisar la correcta separación de estaciones de reciclaje.",
                    "Conuco escolar: Liderar y mantener los semilleros y áreas de siembra.",
                    "Patrulla de ecoeficiencia: Detectar y reportar botes de agua o luces encendidas.",
                    "Vocería ambiental: Difundir efemérides ambientales con sentido educativo."
                ]
            }
        ]
    },
    {
        "titulo": "Brigada de Gestión de Riesgos (Seguridad Integral)",
        "tab_name": "Gestión de Riesgos",
        "icon": ft.Icons.HEALTH_AND_SAFETY_OUTLINED,
        "color_base": "#dc2626",
        "color_dark": "#b91c1c",
        "proposito": "Capacitar a la comunidad escolar para actuar de manera resiliente antes, durante y después de una emergencia (sismos, incendios o lluvias).",
        "identificacion": "Chaleco o distintivo de seguridad escolar.",
        "fundamento_legal": "Protocolos institucionales de seguridad, prevención y resguardo.",
        "mision": "Fortalecer la cultura preventiva del plantel y apoyar la preparación institucional para lograr una respuesta ordenada, informada y segura.",
        "uso_plataforma": "Registrar inventario de seguridad activa (extintores, botiquines), mapas de riesgo digital y reportes de simulacros e incidencias.",
        "actividad_sugerida": "'Detectives de Riesgos con Mapas Digitales': recorrer e identificar vulnerabilidades e instalaciones deficientes en la estructura de la escuela.",
        "objetivo_formativo": "Desarrollar firmeza, conciencia preventiva, disciplina en emergencias y la aptitud básica para dirigir protocolos ordenados en colectivo.",
        "recomendaciones": [
            "Evitar la improvisación mediante apego estricto y riguroso a roles y rutas.",
            "Priorizar en todo caso la calma y la claridad vocal en las instrucciones.",
            "Informar regularmente las fechas de vencimiento o defectos de los inventarios físicos.",
            "Confeccionar reportes rigurosos y formativos tras culminar cualquier incidente."
        ],
        "secciones": [
            {
                "titulo": "Fases de acción",
                "items": [
                    "Prevención (Antes): Actualización regular del mapa de riesgos y revisión física de salidas.",
                    "Respuesta (Durante): Liderar con calma la evacuación organizada de las aulas.",
                    "Recuperación (Después): Chequear el punto de encuentro y verificar personas vulnerables."
                ]
            }
        ]
    },
    {
        "titulo": "Brigada de Patrulla Escolar (Vigilancia Vial)",
        "tab_name": "Patrulla Escolar",
        "icon": ft.Icons.DIRECTIONS_WALK_OUTLINED,
        "color_base": "#ea580c",
        "color_dark": "#c2410c",
        "proposito": "Garantizar el ordenamiento vial pacífico para el resguardo físico general educando al transeúnte sobre un comportamiento civil impecable.",
        "identificacion": "Uniforme regular portando brazalete tricolor, boina azul y símbolo de PARE manual.",
        "fundamento_legal": "Normativas civiles de corresponsabilidad y orden vial estudiantil.",
        "mision": "Promover los desplazamientos seguros de los alumnos y representantes estableciendo un cordón perimetral y una cultura de seguridad en calle.",
        "uso_plataforma": "Roster de turnos digital interactivo para la distribución equitativa de patrullajes y seguimiento y registro de anomalías vehiculares.",
        "actividad_sugerida": "'El Pasaporte del Transeúnte Responsable': Prácticas interactivas de las normativas de paso y señales frente a la vía real en zonas protegidas.",
        "objetivo_formativo": "Formar a los patrulleros en el discernimiento del tráfico, las señales manuales reglamentarias y el control del flujo peatonal civil.",
        "recomendaciones": [
            "Ubicarse con margen de anticipación en el nivel perimetral correcto y seguro.",
            "Solo realizar gestos al confirmar mediante observación panorámica previa las áreas.",
            "Proyectar firmeza civil asertiva y formalidad al ejercer sus labores comunicativas."
        ],
        "secciones": [
            {
                "titulo": "Protocolo de guardia vial",
                "items": [
                    "Ubicación: Permanecer un paso detrás del borde de la acera.",
                    "Observación: Validar estrictamente velocidad de vehículos antes de dar paso.",
                    "Acción: Señal de PARE de frente a vehículos y señal de paso a peatones.",
                    "Normas Clave: No usar pitos ni distractores; saludo marcial y formalidad."
                ]
            }
        ]
    }
]


def build(page: ft.Page, **kwargs) -> ft.Control:
    MAPA_GUIAS = {
        "ecologica": "Ecológica",
        "convivencia": "Convivencia y Paz",
        "riesgo": "Gestión de Riesgos",
        "patrulla": "Patrulla Escolar",
    }
    _tb = (page.data or {}).get("brigada_activa")
    tab_name_objetivo = MAPA_GUIAS.get(_tb)

    guia_activa = next(
        (g for g in GUIAS_BRIGADAS if g["tab_name"] == tab_name_objetivo),
        None
    )

    if guia_activa:
        contenido_guia = ft.Container(
            content=ft.Column(
                [
                    _build_guia_card(page, guia_activa),
                ],
                scroll=None,
            ),
            padding=ft.Padding(0, 16, 0, 0),
        )
    else:
        contenido_guia = ft.Container(
            content=card_principal(
                ft.Column(
                    [
                        ft.Icon(ft.Icons.INFO_OUTLINE, color=COLOR_PRIMARIO, size=48),
                        ft.Container(height=16),
                        ft.Text("Selecciona una Brigada Escolar activa para ver su guía académica extendida.", color=COLOR_TEXTO_SEC, size=16),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            ),
            padding=16,
            alignment=ft.alignment.center
        )

    contenido = ft.Column(
        [
            titulo_pagina(
                "Módulo Educativo y Protocolos",
                "Consulta los fundamentos y directrices operativas de tu Brigada",
            ),
            ft.Container(height=32),
            _build_hero_card(),
            ft.Container(height=16),
            contenido_guia,
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        spacing=0,
    )
    return ft.Container(
        content=contenido,
        padding=24,
        bgcolor=COLOR_FONDO_VERDE,
        expand=True,
    )


def _build_hero_card():
    return card_principal(
        ft.Row(
            [
                ft.Icon(ft.Icons.MENU_BOOK_OUTLINED, color=COLOR_PRIMARIO, size=48),
                ft.Container(width=24),
                ft.Column(
                    [
                        ft.Text("Guía Académica y Operativa Oficial", size=18, weight="bold", color=COLOR_TEXTO),
                        ft.Text("Manual en línea permanente sobre las directrices y pedagogía institucional.", size=14, color=COLOR_TEXTO_SEC),
                    ],
                    spacing=4,
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
        ),
    )


def _build_guia_card(page: ft.Page, guia: dict):
    secciones_gui = []

    def _agregar_seccion(icono: str, titulo: str, contenido=None, es_lista=False):
        # Título de la sección
        secciones_gui.append(
            ft.Row(
                [ft.Icon(icono, color=guia["color_base"], size=20), ft.Text(titulo, size=15, weight="w700", color=COLOR_TEXTO)],
                spacing=8,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        secciones_gui.append(ft.Container(height=6))

        # Contenido
        if contenido:
            if es_lista and isinstance(contenido, list):
                for item in contenido:
                    secciones_gui.append(
                        ft.Row(
                            [
                                ft.Container(width=6, height=6, border_radius=3, bgcolor=guia["color_base"], margin=ft.margin.only(top=6, right=8)),
                                ft.Text(item, size=14, color=COLOR_TEXTO_SEC, expand=True)
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            vertical_alignment=ft.CrossAxisAlignment.START
                        )
                    )
                    secciones_gui.append(ft.Container(height=4))
            else:
                secciones_gui.append(ft.Text(str(contenido), size=14, color=COLOR_TEXTO_SEC))
        
        secciones_gui.append(ft.Container(height=24))

    # Construir UI dinámica según orden institucional
    _agregar_seccion(ft.Icons.STARS_OUTLINED, "Propósito Principal", guia.get("proposito"))
    _agregar_seccion(ft.Icons.BADGE_OUTLINED, "Identificación Visual", guia.get("identificacion"))
    
    if guia.get("fundamento_legal"):
        _agregar_seccion(ft.Icons.GAVEL_OUTLINED, "Marco Orientador Legal", guia.get("fundamento_legal"))
        
    _agregar_seccion(ft.Icons.FLAG_OUTLINED, "Misión de la Brigada", guia.get("mision"))
    
    if "secciones" in guia:
        for sec in guia["secciones"]:
            _agregar_seccion(ft.Icons.FORMAT_LIST_NUMBERED, sec.get("titulo", "Protocolos"), sec.get("items"), es_lista=True)

    _agregar_seccion(ft.Icons.PHONE_IPHONE_OUTLINED, "Uso de la Plataforma Digital SBE", guia.get("uso_plataforma"))
    _agregar_seccion(ft.Icons.LIGHTBULB_OUTLINED, "Actividad Pedagógica Sugerida", guia.get("actividad_sugerida"))
    _agregar_seccion(ft.Icons.SCHOOL_OUTLINED, "Objetivo Formativo Institucional", guia.get("objetivo_formativo"))
    
    if "recomendaciones" in guia:
        _agregar_seccion(ft.Icons.VERIFIED_OUTLINED, "Recomendaciones Operativas", guia.get("recomendaciones"), es_lista=True)

    # Eliminar el botón "Ver más detalles" y espaciado final final
    secciones_gui.append(ft.Container(height=8))

    return ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Container(
                                content=ft.Icon(guia["icon"], color="white", size=48),
                                width=72,
                                height=72,
                                border_radius=16,
                                bgcolor=ft.Colors.with_opacity(0.2, "white"),
                                alignment=ft.Alignment.CENTER,
                            ),
                            ft.Container(width=20),
                            ft.Column(
                                [
                                    ft.Text(guia["titulo"], size=22, weight="bold", color="white"),
                                    ft.Text("Manual Operativo Completo", size=14, color=ft.Colors.with_opacity(0.9, "white")),
                                ],
                                spacing=4,
                                horizontal_alignment=ft.CrossAxisAlignment.START,
                                expand=True,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    padding=24,
                    border_radius=ft.BorderRadius.only(top_left=16, top_right=16),
                    gradient=ft.LinearGradient(
                        begin=ft.Alignment.TOP_LEFT,
                        end=ft.Alignment.BOTTOM_RIGHT,
                        colors=[guia["color_base"], guia["color_dark"]],
                    ),
                ),
                ft.Container(
                    content=ft.Column(
                        secciones_gui,
                        spacing=0,
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                    ),
                    padding=32,
                    bgcolor=COLOR_CARD,
                    border_radius=ft.BorderRadius.only(bottom_left=16, bottom_right=16),
                    border=ft.Border(left=ft.BorderSide(1, COLOR_BORDE), bottom=ft.BorderSide(1, COLOR_BORDE), right=ft.BorderSide(1, COLOR_BORDE)),
                ),
            ],
            spacing=0,
        ),
        border_radius=16,
        shadow=get_sombra_card(),
    )
