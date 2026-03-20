"""
Tema del SBG — Sistema Multi-Brigada.
4 paletas de color (una por tipo de brigada) + paleta neutra para auth.
Soporte para modo claro y oscuro con ft.Theme y ft.ColorScheme.
"""

import flet as ft

# =====================================================================
# PALETA ECOLÓGICA (Verde) — La original, sin cambios
# =====================================================================
HEX_ECO_PRIMARIO = "#059669"
HEX_ECO_PRIMARIO_CLARO = "#10b981"
HEX_ECO_PRIMARIO_OSCURO = "#047857"
HEX_ECO_VERDE_SUAVE = "#d1fae5"
HEX_ECO_FONDO = "#f0fdf4"
HEX_ECO_SIDEBAR = "#14532d"

TEMA_ECO_CLARO = ft.Theme(
    color_scheme=ft.ColorScheme(
        primary="#059669",
        primary_container="#047857",
        on_primary="white",
        on_primary_container="#d1fae5",
        secondary="#10b981",
        secondary_container="#d1fae5",
        on_secondary="white",
        surface="#ffffff",
        on_surface="#1e293b",
        surface_container_high="#14532d",
        on_surface_variant="#f0fdf4",
        surface_container_lowest="#f0fdf4",
        surface_container_low="#ecfdf5",
        surface_container="#f8fafc",
        outline="#e2e8f0",
        outline_variant="#86efac",
        scrim="#64748b",
        shadow="black",
        error="#ef4444",
        on_error="white",
        inverse_surface="#166534",
        inverse_primary="#10b981",
    ),
    use_material3=True,
    date_picker_theme=ft.DatePickerTheme(
        bgcolor="#ffffff",
        header_bgcolor="#059669",
        header_foreground_color="white",
        day_foreground_color="#1e293b",
        today_foreground_color="white",
        today_bgcolor="#059669",
        shadow_color="transparent",
    ),
    time_picker_theme=ft.TimePickerTheme(
        bgcolor="#ffffff",
        dial_bgcolor="#d1fae5",
        dial_hand_color="#059669",
        dial_text_color="#1e293b",
        hour_minute_color="#d1fae5",
        hour_minute_text_color="#1e293b",
        day_period_color="#d1fae5",
        day_period_text_color="#1e293b",
        entry_mode_icon_color="#059669",
        time_selector_separator_color="#059669",
    ),
)

TEMA_ECO_OSCURO = ft.Theme(
    color_scheme=ft.ColorScheme(
        primary="#10b981",
        primary_container="#064e3b",
        on_primary="white",
        on_primary_container="#a7f3d0",
        secondary="#34d399",
        secondary_container="#065f46",
        on_secondary="#022c22",
        surface="#131f1a",
        on_surface="#ecfdf5",
        surface_container_high="#06120e",
        on_surface_variant="#d1fae5",
        surface_container_lowest="#0a0f0d",
        surface_container_low="#0d1612",
        surface_container="#111c17",
        outline="#374151",
        outline_variant="#6ee7b7",
        scrim="#9ca3af",
        shadow="black",
        error="#f87171",
        on_error="#1c1917",
        inverse_surface="#065f46",
        inverse_primary="#059669",
    ),
    use_material3=True,
    date_picker_theme=ft.DatePickerTheme(
        bgcolor="#131f1a",
        header_bgcolor="#064e3b",
        header_foreground_color="white",
        day_foreground_color="#ecfdf5",
        today_foreground_color="white",
        today_bgcolor="#10b981",
        shadow_color="transparent",
    ),
    time_picker_theme=ft.TimePickerTheme(
        bgcolor="#131f1a",
        dial_bgcolor="#064e3b",
        dial_hand_color="#10b981",
        dial_text_color="#ecfdf5",
        hour_minute_color="#064e3b",
        hour_minute_text_color="#ecfdf5",
        day_period_color="#064e3b",
        day_period_text_color="#ecfdf5",
        entry_mode_icon_color="#10b981",
        time_selector_separator_color="#10b981",
    ),
)

# =====================================================================
# PALETA GESTIÓN DE RIESGO (Rojo + Amarillo)
# =====================================================================
HEX_RIESGO_PRIMARIO = "#dc2626"
HEX_RIESGO_PRIMARIO_CLARO = "#ef4444"
HEX_RIESGO_PRIMARIO_OSCURO = "#991b1b"
HEX_RIESGO_SUAVE = "#fecaca"
HEX_RIESGO_FONDO = "#fef2f2"
HEX_RIESGO_SIDEBAR = "#450a0a"

TEMA_RIESGO_CLARO = ft.Theme(
    color_scheme=ft.ColorScheme(
        primary="#dc2626",
        primary_container="#991b1b",
        on_primary="white",
        on_primary_container="#fecaca",
        secondary="#ef4444",
        secondary_container="#fecaca",
        on_secondary="white",
        surface="#ffffff",
        on_surface="#1e293b",
        surface_container_high="#450a0a",
        on_surface_variant="#fef2f2",
        surface_container_lowest="#fef2f2",
        surface_container_low="#fff1f2",
        surface_container="#f8fafc",
        outline="#e2e8f0",
        outline_variant="#fca5a5",
        scrim="#64748b",
        shadow="black",
        error="#ef4444",
        on_error="white",
        inverse_surface="#7f1d1d",
        inverse_primary="#ef4444",
    ),
    use_material3=True,
    date_picker_theme=ft.DatePickerTheme(
        bgcolor="#ffffff",
        header_bgcolor="#dc2626",
        header_foreground_color="white",
        day_foreground_color="#1e293b",
        today_foreground_color="white",
        today_bgcolor="#dc2626",
        shadow_color="transparent",
    ),
    time_picker_theme=ft.TimePickerTheme(
        bgcolor="#ffffff",
        dial_bgcolor="#fecaca",
        dial_hand_color="#dc2626",
        dial_text_color="#1e293b",
        hour_minute_color="#fecaca",
        hour_minute_text_color="#1e293b",
        day_period_color="#fecaca",
        day_period_text_color="#1e293b",
        entry_mode_icon_color="#dc2626",
        time_selector_separator_color="#dc2626",
    ),
)

TEMA_RIESGO_OSCURO = ft.Theme(
    color_scheme=ft.ColorScheme(
        primary="#ef4444",
        primary_container="#7f1d1d",
        on_primary="white",
        on_primary_container="#fca5a5",
        secondary="#f87171",
        secondary_container="#991b1b",
        on_secondary="#1c0404",
        surface="#1f1315",
        on_surface="#fef2f2",
        surface_container_high="#120a0b",
        on_surface_variant="#fecaca",
        surface_container_lowest="#0f0a0b",
        surface_container_low="#160e10",
        surface_container="#1a1113",
        outline="#374151",
        outline_variant="#f87171",
        scrim="#9ca3af",
        shadow="black",
        error="#f87171",
        on_error="#1c1917",
        inverse_surface="#991b1b",
        inverse_primary="#dc2626",
    ),
    use_material3=True,
    date_picker_theme=ft.DatePickerTheme(
        bgcolor="#1f1315",
        header_bgcolor="#7f1d1d",
        header_foreground_color="white",
        day_foreground_color="#fef2f2",
        today_foreground_color="white",
        today_bgcolor="#ef4444",
        shadow_color="transparent",
    ),
    time_picker_theme=ft.TimePickerTheme(
        bgcolor="#1f1315",
        dial_bgcolor="#7f1d1d",
        dial_hand_color="#ef4444",
        dial_text_color="#fef2f2",
        hour_minute_color="#7f1d1d",
        hour_minute_text_color="#fef2f2",
        day_period_color="#7f1d1d",
        day_period_text_color="#fef2f2",
        entry_mode_icon_color="#ef4444",
        time_selector_separator_color="#ef4444",
    ),
)

# =====================================================================
# PALETA PATRULLA ESCOLAR (Naranja)
# =====================================================================
HEX_PATRULLA_PRIMARIO = "#ea580c"
HEX_PATRULLA_PRIMARIO_CLARO = "#f97316"
HEX_PATRULLA_PRIMARIO_OSCURO = "#c2410c"
HEX_PATRULLA_SUAVE = "#fed7aa"
HEX_PATRULLA_FONDO = "#fff7ed"
HEX_PATRULLA_SIDEBAR = "#431407"

TEMA_PATRULLA_CLARO = ft.Theme(
    color_scheme=ft.ColorScheme(
        primary="#ea580c",
        primary_container="#c2410c",
        on_primary="white",
        on_primary_container="#fed7aa",
        secondary="#f97316",
        secondary_container="#fed7aa",
        on_secondary="white",
        surface="#ffffff",
        on_surface="#1e293b",
        surface_container_high="#431407",
        on_surface_variant="#fff7ed",
        surface_container_lowest="#fff7ed",
        surface_container_low="#ffedd5",
        surface_container="#f8fafc",
        outline="#e2e8f0",
        outline_variant="#fdba74",
        scrim="#64748b",
        shadow="black",
        error="#ef4444",
        on_error="white",
        inverse_surface="#7c2d12",
        inverse_primary="#f97316",
    ),
    use_material3=True,
    date_picker_theme=ft.DatePickerTheme(
        bgcolor="#ffffff",
        header_bgcolor="#ea580c",
        header_foreground_color="white",
        day_foreground_color="#1e293b",
        today_foreground_color="white",
        today_bgcolor="#ea580c",
        shadow_color="transparent",
    ),
    time_picker_theme=ft.TimePickerTheme(
        bgcolor="#ffffff",
        dial_bgcolor="#fed7aa",
        dial_hand_color="#ea580c",
        dial_text_color="#1e293b",
        hour_minute_color="#fed7aa",
        hour_minute_text_color="#1e293b",
        day_period_color="#fed7aa",
        day_period_text_color="#1e293b",
        entry_mode_icon_color="#ea580c",
        time_selector_separator_color="#ea580c",
    ),
)

TEMA_PATRULLA_OSCURO = ft.Theme(
    color_scheme=ft.ColorScheme(
        primary="#f97316",
        primary_container="#7c2d12",
        on_primary="white",
        on_primary_container="#fdba74",
        secondary="#fb923c",
        secondary_container="#9a3412",
        on_secondary="#1c0c04",
        surface="#1f1712",
        on_surface="#fff7ed",
        surface_container_high="#120d08",
        on_surface_variant="#fed7aa",
        surface_container_lowest="#0f0b07",
        surface_container_low="#16110c",
        surface_container="#1a140f",
        outline="#374151",
        outline_variant="#fb923c",
        scrim="#9ca3af",
        shadow="black",
        error="#f87171",
        on_error="#1c1917",
        inverse_surface="#9a3412",
        inverse_primary="#ea580c",
    ),
    use_material3=True,
    date_picker_theme=ft.DatePickerTheme(
        bgcolor="#1f1712",
        header_bgcolor="#7c2d12",
        header_foreground_color="white",
        day_foreground_color="#fff7ed",
        today_foreground_color="white",
        today_bgcolor="#f97316",
        shadow_color="transparent",
    ),
    time_picker_theme=ft.TimePickerTheme(
        bgcolor="#1f1712",
        dial_bgcolor="#7c2d12",
        dial_hand_color="#f97316",
        dial_text_color="#fff7ed",
        hour_minute_color="#7c2d12",
        hour_minute_text_color="#fff7ed",
        day_period_color="#7c2d12",
        day_period_text_color="#fff7ed",
        entry_mode_icon_color="#f97316",
        time_selector_separator_color="#f97316",
    ),
)

# =====================================================================
# PALETA CONVIVENCIA Y PAZ (Gris perla / Slate — tonos blancos visibles)
# =====================================================================
HEX_CONVIVENCIA_PRIMARIO = "#64748b"
HEX_CONVIVENCIA_PRIMARIO_CLARO = "#94a3b8"
HEX_CONVIVENCIA_PRIMARIO_OSCURO = "#475569"
HEX_CONVIVENCIA_SUAVE = "#e2e8f0"
HEX_CONVIVENCIA_FONDO = "#f1f5f9"
HEX_CONVIVENCIA_SIDEBAR = "#1e293b"

TEMA_CONVIVENCIA_CLARO = ft.Theme(
    color_scheme=ft.ColorScheme(
        primary="#64748b",
        primary_container="#475569",
        on_primary="white",
        on_primary_container="#e2e8f0",
        secondary="#94a3b8",
        secondary_container="#e2e8f0",
        on_secondary="white",
        surface="#ffffff",
        on_surface="#1e293b",
        surface_container_high="#1e293b",
        on_surface_variant="#f1f5f9",
        surface_container_lowest="#f1f5f9",
        surface_container_low="#f8fafc",
        surface_container="#f8fafc",
        outline="#e2e8f0",
        outline_variant="#94a3b8",
        scrim="#64748b",
        shadow="black",
        error="#ef4444",
        on_error="white",
        inverse_surface="#334155",
        inverse_primary="#94a3b8",
    ),
    use_material3=True,
    date_picker_theme=ft.DatePickerTheme(
        bgcolor="#ffffff",
        header_bgcolor="#64748b",
        header_foreground_color="white",
        day_foreground_color="#1e293b",
        today_foreground_color="white",
        today_bgcolor="#64748b",
        shadow_color="transparent",
    ),
    time_picker_theme=ft.TimePickerTheme(
        bgcolor="#ffffff",
        dial_bgcolor="#e2e8f0",
        dial_hand_color="#64748b",
        dial_text_color="#1e293b",
        hour_minute_color="#e2e8f0",
        hour_minute_text_color="#1e293b",
        day_period_color="#e2e8f0",
        day_period_text_color="#1e293b",
        entry_mode_icon_color="#64748b",
        time_selector_separator_color="#64748b",
    ),
)

TEMA_CONVIVENCIA_OSCURO = ft.Theme(
    color_scheme=ft.ColorScheme(
        primary="#94a3b8",
        primary_container="#334155",
        on_primary="white",
        on_primary_container="#cbd5e1",
        secondary="#cbd5e1",
        secondary_container="#475569",
        on_secondary="#0f172a",
        surface="#1a1f2e",
        on_surface="#f1f5f9",
        surface_container_high="#0f1420",
        on_surface_variant="#e2e8f0",
        surface_container_lowest="#0c1018",
        surface_container_low="#141925",
        surface_container="#171c2a",
        outline="#374151",
        outline_variant="#94a3b8",
        scrim="#9ca3af",
        shadow="black",
        error="#f87171",
        on_error="#1c1917",
        inverse_surface="#475569",
        inverse_primary="#64748b",
    ),
    use_material3=True,
    date_picker_theme=ft.DatePickerTheme(
        bgcolor="#1a1f2e",
        header_bgcolor="#334155",
        header_foreground_color="white",
        day_foreground_color="#f1f5f9",
        today_foreground_color="white",
        today_bgcolor="#94a3b8",
        shadow_color="transparent",
    ),
    time_picker_theme=ft.TimePickerTheme(
        bgcolor="#1a1f2e",
        dial_bgcolor="#334155",
        dial_hand_color="#94a3b8",
        dial_text_color="#f1f5f9",
        hour_minute_color="#334155",
        hour_minute_text_color="#f1f5f9",
        day_period_color="#334155",
        day_period_text_color="#f1f5f9",
        entry_mode_icon_color="#94a3b8",
        time_selector_separator_color="#94a3b8",
    ),
)

# =====================================================================
# PALETA NEUTRA (Slate — para Login, Registro, Recuperación)
# =====================================================================
HEX_NEUTRA_PRIMARIO = "#475569"
HEX_NEUTRA_PRIMARIO_CLARO = "#64748b"
HEX_NEUTRA_PRIMARIO_OSCURO = "#334155"
HEX_NEUTRA_SIDEBAR = "#1e293b"

TEMA_NEUTRA_CLARO = ft.Theme(
    color_scheme=ft.ColorScheme(
        primary="#475569",
        primary_container="#334155",
        on_primary="white",
        on_primary_container="#cbd5e1",
        secondary="#64748b",
        secondary_container="#e2e8f0",
        on_secondary="white",
        surface="#ffffff",
        on_surface="#1e293b",
        surface_container_high="#1e293b",
        on_surface_variant="#f1f5f9",
        surface_container_lowest="#f8fafc",
        surface_container_low="#f1f5f9",
        surface_container="#f8fafc",
        outline="#e2e8f0",
        outline_variant="#94a3b8",
        scrim="#64748b",
        shadow="black",
        error="#ef4444",
        on_error="white",
        inverse_surface="#334155",
        inverse_primary="#94a3b8",
    ),
    use_material3=True,
)

TEMA_NEUTRA_OSCURO = ft.Theme(
    color_scheme=ft.ColorScheme(
        primary="#94a3b8",
        primary_container="#334155",
        on_primary="white",
        on_primary_container="#cbd5e1",
        secondary="#cbd5e1",
        secondary_container="#475569",
        on_secondary="#0f172a",
        surface="#1e293b",
        on_surface="#f1f5f9",
        surface_container_high="#0f172a",
        on_surface_variant="#e2e8f0",
        surface_container_lowest="#0f172a",
        surface_container_low="#1e293b",
        surface_container="#1e293b",
        outline="#374151",
        outline_variant="#94a3b8",
        scrim="#9ca3af",
        shadow="black",
        error="#f87171",
        on_error="#1c1917",
        inverse_surface="#475569",
        inverse_primary="#64748b",
    ),
    use_material3=True,
)

# =====================================================================
# ALIAS RETROCOMPATIBLES — Apuntan a Ecológica por defecto
# =====================================================================
TEMA_CLARO = TEMA_ECO_CLARO
TEMA_OSCURO = TEMA_ECO_OSCURO

HEX_PRIMARIO = HEX_ECO_PRIMARIO
HEX_PRIMARIO_CLARO = HEX_ECO_PRIMARIO_CLARO
HEX_PRIMARIO_OSCURO = HEX_ECO_PRIMARIO_OSCURO
HEX_VERDE_SUAVE = HEX_ECO_VERDE_SUAVE
HEX_FONDO_VERDE = HEX_ECO_FONDO
HEX_SIDEBAR = HEX_ECO_SIDEBAR

# =====================================================================
# REGISTRO DE PALETAS
# =====================================================================
BRIGADAS = {
    "ecologica": {
        "nombre": "Brigada Ecológica",
        "claro": TEMA_ECO_CLARO,
        "oscuro": TEMA_ECO_OSCURO,
        "hex_primario": HEX_ECO_PRIMARIO,
        "hex_primario_claro": HEX_ECO_PRIMARIO_CLARO,
        "hex_primario_oscuro": HEX_ECO_PRIMARIO_OSCURO,
        "hex_sidebar": HEX_ECO_SIDEBAR,
        "hex_fondo": HEX_ECO_FONDO,
        "icono": "ECO",
    },
    "riesgo": {
        "nombre": "Brigada de Gestión de Riesgo",
        "claro": TEMA_RIESGO_CLARO,
        "oscuro": TEMA_RIESGO_OSCURO,
        "hex_primario": HEX_RIESGO_PRIMARIO,
        "hex_primario_claro": HEX_RIESGO_PRIMARIO_CLARO,
        "hex_primario_oscuro": HEX_RIESGO_PRIMARIO_OSCURO,
        "hex_sidebar": HEX_RIESGO_SIDEBAR,
        "hex_fondo": HEX_RIESGO_FONDO,
        "icono": "HEALTH_AND_SAFETY",
    },
    "patrulla": {
        "nombre": "Brigada de Patrulla Escolar",
        "claro": TEMA_PATRULLA_CLARO,
        "oscuro": TEMA_PATRULLA_OSCURO,
        "hex_primario": HEX_PATRULLA_PRIMARIO,
        "hex_primario_claro": HEX_PATRULLA_PRIMARIO_CLARO,
        "hex_primario_oscuro": HEX_PATRULLA_PRIMARIO_OSCURO,
        "hex_sidebar": HEX_PATRULLA_SIDEBAR,
        "hex_fondo": HEX_PATRULLA_FONDO,
        "icono": "TRAFFIC",
    },
    "convivencia": {
        "nombre": "Brigada de Convivencia y Paz",
        "claro": TEMA_CONVIVENCIA_CLARO,
        "oscuro": TEMA_CONVIVENCIA_OSCURO,
        "hex_primario": HEX_CONVIVENCIA_PRIMARIO,
        "hex_primario_claro": HEX_CONVIVENCIA_PRIMARIO_CLARO,
        "hex_primario_oscuro": HEX_CONVIVENCIA_PRIMARIO_OSCURO,
        "hex_sidebar": HEX_CONVIVENCIA_SIDEBAR,
        "hex_fondo": HEX_CONVIVENCIA_FONDO,
        "icono": "HANDSHAKE",
    },
}


def aplicar_paleta(page, nombre_brigada: str):
    """Cambia el tema de la página según la brigada seleccionada."""
    paleta = BRIGADAS.get(nombre_brigada)
    if paleta:
        page.theme = paleta["claro"]
        page.dark_theme = paleta["oscuro"]
    page.update()


def aplicar_paleta_neutra(page):
    """Aplica la paleta neutra (Login/Registro/Recuperación)."""
    page.theme = TEMA_NEUTRA_CLARO
    page.dark_theme = TEMA_NEUTRA_OSCURO
    page.update()


# --- Constantes Dinámicas (Flet resuelve según ThemeMode) ---
COLOR_PRIMARIO = ft.Colors.PRIMARY
COLOR_PRIMARIO_CLARO = ft.Colors.SECONDARY
COLOR_PRIMARIO_OSCURO = ft.Colors.PRIMARY_CONTAINER

COLOR_VERDE_SUAVE = ft.Colors.SECONDARY_CONTAINER

# Fondos
COLOR_FONDO_VERDE = ft.Colors.SURFACE_CONTAINER_LOWEST
COLOR_FONDO_GRADIENTE_INICIO = ft.Colors.SURFACE_CONTAINER_LOWEST
COLOR_FONDO_GRADIENTE_FIN = ft.Colors.SURFACE

# Sidebar
COLOR_SIDEBAR = ft.Colors.SURFACE_CONTAINER_HIGH
COLOR_SIDEBAR_ACTIVO = ft.Colors.INVERSE_SURFACE
COLOR_SIDEBAR_TEXTO = ft.Colors.ON_SURFACE_VARIANT
COLOR_SIDEBAR_TEXTO_SEC = ft.Colors.OUTLINE_VARIANT

# Contenido
COLOR_TEXTO = ft.Colors.ON_SURFACE
COLOR_TEXTO_SEC = ft.Colors.SCRIM
COLOR_BORDE = ft.Colors.OUTLINE
COLOR_CARD = ft.Colors.SURFACE
COLOR_CANCELAR = ft.Colors.SCRIM

# Acentos
COLOR_EXITO = "#10b981"
COLOR_ALERTA = "#f59e0b"
COLOR_PELIGRO = "#ef4444"
COLOR_INFO = "#0ea5e9"

# Tipografía y espaciado
RADIO = 12
RADIO_GRANDE = 16
PADDING = 24
SOMBRA_SUAVE = None

def get_sombra_suave():
    return ft.BoxShadow(
        blur_radius=20,
        spread_radius=-4,
        color=ft.Colors.with_opacity(0.06, "black"),
        offset=ft.Offset(0, 4),
    )

def get_sombra_card():
    return [
        ft.BoxShadow(
            blur_radius=24,
            spread_radius=-6,
            color=ft.Colors.with_opacity(0.08, "black"),
            offset=ft.Offset(0, 6),
        ),
    ]
