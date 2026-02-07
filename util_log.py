"""
Log a archivo para ver qué pasa cuando la terminal no muestra nada.
Abre el archivo sbg_log.txt en la carpeta del proyecto para ver los mensajes.
"""
import os
from datetime import datetime

LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sbg_log.txt")


def log(mensaje: str):
    """Escribe una línea con fecha/hora en sbg_log.txt (y hace flush)."""
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%H:%M:%S')}] {mensaje}\n")
            f.flush()
    except Exception:
        pass
