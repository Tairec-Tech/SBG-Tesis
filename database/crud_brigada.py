"""
CRUD de Brigada para el SGB.
Requiere haber ejecutado database/migrate_brigada_campos.sql si usas descripcion, coordinador, color.
"""
from database.connection import get_connection


def insertar_brigada(nombre, descripcion, coordinador, color_identificador, institucion_id=1):
    """
    Inserta una nueva brigada.
    institucion_id: por defecto 1 (debe existir en Institucion_Educativa).
    Retorna el idBrigada creado o lanza excepción.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        # area_accion es obligatorio en el esquema original; usamos descripcion truncada o nombre
        area_accion = (descripcion or nombre or "General")[:45]
        cursor.execute(
            """
            INSERT INTO Brigada (
                nombre_brigada, area_accion, descripcion, coordinador, color_identificador,
                Institucion_Educativa_idInstitucion
            ) VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (nombre, area_accion, descripcion or None, coordinador or None, color_identificador or None, institucion_id),
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def listar_brigadas():
    """
    Lista todas las brigadas con conteo de miembros.
    Retorna lista de dict con: idBrigada, nombre_brigada, area_accion, descripcion, coordinador, color_identificador, num_miembros.
    Si no existen columnas descripcion/coordinador/color (sin migración), usa solo nombre_brigada y area_accion.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        # Intentar con columnas extendidas (tras migrate_brigada_campos.sql)
        try:
            cursor.execute(
                """
                SELECT b.idBrigada, b.nombre_brigada, b.area_accion,
                    b.descripcion, b.coordinador, b.color_identificador,
                    COUNT(u.idUsuario) AS num_miembros
                FROM Brigada b
                LEFT JOIN Usuario u ON u.Brigada_idBrigada = b.idBrigada
                GROUP BY b.idBrigada, b.nombre_brigada, b.area_accion, b.descripcion, b.coordinador, b.color_identificador
                ORDER BY b.nombre_brigada
                """
            )
        except Exception:
            cursor.execute(
                """
                SELECT b.idBrigada, b.nombre_brigada, b.area_accion,
                    COUNT(u.idUsuario) AS num_miembros
                FROM Brigada b
                LEFT JOIN Usuario u ON u.Brigada_idBrigada = b.idBrigada
                GROUP BY b.idBrigada, b.nombre_brigada, b.area_accion
                ORDER BY b.nombre_brigada
                """
            )
        rows = cursor.fetchall()
        # Normalizar: asegurar claves opcionales
        for r in rows:
            r.setdefault("descripcion", None)
            r.setdefault("coordinador", None)
            r.setdefault("color_identificador", None)
            r["num_miembros"] = r.get("num_miembros", 0) or 0
        return rows
    finally:
        conn.close()


def obtener_brigada(id_brigada: int):
    """Obtiene una brigada por id. Retorna dict o None."""
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT idBrigada, nombre_brigada, area_accion, descripcion, coordinador, color_identificador,
                    Institucion_Educativa_idInstitucion
                FROM Brigada WHERE idBrigada = %s
                """,
                (id_brigada,),
            )
        except Exception:
            cursor.execute(
                "SELECT idBrigada, nombre_brigada, area_accion, Institucion_Educativa_idInstitucion FROM Brigada WHERE idBrigada = %s",
                (id_brigada,),
            )
        row = cursor.fetchone()
        if row:
            row.setdefault("descripcion", None)
            row.setdefault("coordinador", None)
            row.setdefault("color_identificador", None)
        return row
    finally:
        conn.close()


def actualizar_brigada(id_brigada: int, nombre: str, area_accion: str = None, descripcion: str = None, coordinador: str = None, color_identificador: str = None, institucion_id: int = None):
    """Actualiza una brigada. area_accion es obligatorio en BD; si no se pasa, se usa nombre o 'General'."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        area = (area_accion or nombre or "General")[:45]
        try:
            cursor.execute(
                """
                UPDATE Brigada SET nombre_brigada = %s, area_accion = %s, descripcion = %s, coordinador = %s, color_identificador = %s
                WHERE idBrigada = %s
                """,
                (nombre, area, descripcion or None, coordinador or None, color_identificador or None, id_brigada),
            )
        except Exception:
            cursor.execute(
                "UPDATE Brigada SET nombre_brigada = %s, area_accion = %s WHERE idBrigada = %s",
                (nombre, area, id_brigada),
            )
        conn.commit()
    finally:
        conn.close()


def eliminar_brigada(id_brigada: int) -> str | None:
    """
    Elimina la brigada si no tiene usuarios asignados.
    Retorna None si OK, o mensaje de error si tiene miembros o fallo.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Usuario WHERE Brigada_idBrigada = %s", (id_brigada,))
        (num,) = cursor.fetchone()
        if num and num > 0:
            return f"No se puede eliminar: la brigada tiene {num} usuario(s) asignado(s). Asigne o elimine los usuarios primero."
        cursor.execute("DELETE FROM Brigada WHERE idBrigada = %s", (id_brigada,))
        conn.commit()
        return None
    except Exception as e:
        return str(e)
    finally:
        conn.close()
