"""
Tema del SGB — Brigadas Ambientales.
Paleta en tonos verdes (brigadas ambientales únicamente).
"""

# --- Brigadas ambientales: tonos verdes ---
COLOR_PRIMARIO = "#059669"       # Emerald-600 (principal)
COLOR_PRIMARIO_CLARO = "#10b981" # Emerald-500
COLOR_PRIMARIO_OSCURO = "#047857" # Emerald-700
COLOR_VERDE_SUAVE = "#d1fae5"    # Emerald-100
COLOR_FONDO_VERDE = "#f0fdf4"    # Green-50 (fondo contenido)
COLOR_FONDO_GRADIENTE_INICIO = "#ecfdf5"  # para gradientes
COLOR_FONDO_GRADIENTE_FIN = "#ffffff"

# Sidebar — verde oscuro (misma oscuridad que antes, tono brigadas ambientales)
COLOR_SIDEBAR = "#14532d"         # Green-900
COLOR_SIDEBAR_ACTIVO = "#166534"  # Green-800 (ítem activo)
COLOR_SIDEBAR_TEXTO = "#f0fdf4"   # Green-50
COLOR_SIDEBAR_TEXTO_SEC = "#86efac" # Green-300

# Contenido
COLOR_TEXTO = "#1e293b"
COLOR_TEXTO_SEC = "#64748b"
COLOR_BORDE = "#e2e8f0"
COLOR_CARD = "#ffffff"
COLOR_CANCELAR = "#64748b"

# Acentos (para cards, estados)
COLOR_EXITO = "#10b981"
COLOR_ALERTA = "#f59e0b"
COLOR_PELIGRO = "#ef4444"
COLOR_INFO = "#0ea5e9"

# Tipografía y espaciado
RADIO = 12
RADIO_GRANDE = 16
PADDING = 24
SOMBRA_SUAVE = None  # se crea en runtime

def get_sombra_suave():
    import flet as ft
    return ft.BoxShadow(
        blur_radius=20,
        spread_radius=-4,
        color=ft.Colors.with_opacity(0.06, "black"),
        offset=ft.Offset(0, 4),
    )

def get_sombra_card():
    import flet as ft
    return [
        ft.BoxShadow(
            blur_radius=24,
            spread_radius=-6,
            color=ft.Colors.with_opacity(0.08, "black"),
            offset=ft.Offset(0, 6),
        ),
    ]
