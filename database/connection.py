"""
Conexión a MySQL para el SGB.
"""
import mysql.connector
from mysql.connector import Error

from database.config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME


def get_connection():
    """Abre una conexión a la base de datos. Cerrar con conn.close()."""
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            charset="utf8mb4",
        )
        return conn
    except Error as e:
        raise RuntimeError(f"Error al conectar a la base de datos: {e}") from e


def ejecutar(consulta, params=None, commit=False):
    """
    Ejecuta una consulta (SELECT o INSERT/UPDATE/DELETE).
    Si commit=True, hace commit. Retorna el cursor para SELECT o el lastrowid para INSERT.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(consulta, params or ())
        if commit:
            conn.commit()
            return cursor.lastrowid
        return cursor
    finally:
        if not commit:
            conn.close()
