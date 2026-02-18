"""
Tema del SGB — Brigadas Ambientales.
Paleta en tonos verdes (brigadas ambientales únicamente).
Soporte para modo claro y oscuro con ft.Theme y ft.ColorScheme.
"""

import flet as ft

# --- Paleta Base (Hex) — para animaciones, gradientes, o colores estáticos ---
HEX_PRIMARIO = "#059669"       # Emerald-600 (principal)
HEX_PRIMARIO_CLARO = "#10b981" # Emerald-500
HEX_PRIMARIO_OSCURO = "#047857" # Emerald-700
HEX_VERDE_SUAVE = "#d1fae5"    # Emerald-100
HEX_FONDO_VERDE = "#f0fdf4"    # Green-50 (fondo contenido)
HEX_SIDEBAR = "#14532d"        # Green-900

# --- Definición de Temas Flet ---

TEMA_CLARO = ft.Theme(
    color_scheme=ft.ColorScheme(
        primary="#059669",                    # Emerald-600
        primary_container="#047857",          # Emerald-700
        on_primary="white",
        on_primary_container="#d1fae5",
        secondary="#10b981",                  # Emerald-500
        secondary_container="#d1fae5",
        on_secondary="white",

        surface="#ffffff",                    # Cards
        on_surface="#1e293b",                 # Texto principal (Slate-800)
        surface_container_high="#14532d",     # Sidebar fondo (Green-900) - REEMPLAZO DE surface_variant
        on_surface_variant="#f0fdf4",         # Sidebar texto (Green-50)
        surface_container_lowest="#f0fdf4",   # Fondo principal (Green-50)
        surface_container_low="#ecfdf5",      # Fondo gradiente
        surface_container="#f8fafc",          # Fondo alternativo

        outline="#e2e8f0",                    # Bordes (Slate-200)
        outline_variant="#86efac",            # Sidebar texto sec (Green-300)
        scrim="#64748b",                      # Texto secundario (Slate-500)
        shadow="black",

        error="#ef4444",
        on_error="white",

        inverse_surface="#166534",            # Sidebar ítem activo (Green-800)
        inverse_primary="#10b981",
    ),
    use_material3=True,
)

TEMA_OSCURO = ft.Theme(
    color_scheme=ft.ColorScheme(
        primary="#10b981",                    # Emerald-500 (más brillante)
        primary_container="#064e3b",          # Emerald-900
        on_primary="#022c22",
        on_primary_container="#a7f3d0",
        secondary="#34d399",                  # Emerald-400
        secondary_container="#065f46",
        on_secondary="#022c22",

        surface="#131f1a",                    # Cards oscuras
        on_surface="#ecfdf5",                 # Texto principal claro
        surface_container_high="#06120e",     # Sidebar oscuro - REEMPLAZO DE surface_variant
        on_surface_variant="#d1fae5",         # Sidebar texto
        surface_container_lowest="#0a0f0d",   # Fondo principal oscuro
        surface_container_low="#0d1612",      # Fondo gradiente oscuro
        surface_container="#111c17",          # Fondo alternativo oscuro

        outline="#374151",                    # Bordes (Gray-700)
        outline_variant="#6ee7b7",            # Sidebar texto sec
        scrim="#9ca3af",                      # Texto secundario (Gray-400)
        shadow="black",

        error="#f87171",
        on_error="#1c1917",

        inverse_surface="#065f46",            # Sidebar ítem activo
        inverse_primary="#059669",
    ),
    use_material3=True,
)

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
COLOR_TEXTO_SEC = ft.Colors.SCRIM     # Usando scrim como texto secundario
COLOR_BORDE = ft.Colors.OUTLINE
COLOR_CARD = ft.Colors.SURFACE
COLOR_CANCELAR = ft.Colors.SCRIM

# Acentos
COLOR_EXITO = "#10b981"    # Mantener hex, no cambian con tema
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
