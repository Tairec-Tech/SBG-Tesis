"""CRUD para configuración global (ej. mensaje del día)."""
from database.connection import get_connection

CLAVE_MENSAJE_DIA = "mensaje_dia"


def get_mensaje_dia() -> str:
    """Obtiene el mensaje del día. Retorna cadena vacía si no existe la tabla o la clave."""
    try:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT valor FROM configuracion WHERE clave = %s",
                (CLAVE_MENSAJE_DIA,),
            )
            row = cursor.fetchone()
            return (row[0] or "").strip() if row else ""
        finally:
            conn.close()
    except Exception:
        return ""


def set_mensaje_dia(texto: str) -> bool:
    """Guarda el mensaje del día. Retorna True si se guardó correctamente."""
    try:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO configuracion (clave, valor) VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE valor = VALUES(valor)
                """,
                (CLAVE_MENSAJE_DIA, (texto or "").strip()),
            )
            conn.commit()
            return True
        finally:
            conn.close()
    except Exception:
        return False
