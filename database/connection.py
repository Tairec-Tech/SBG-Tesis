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
    Ejecuta una consulta.
    Si commit=True: hace commit y retorna lastrowid. Cierra conexión.
    Si commit=False: hace fetchall y retorna (rows, description). Cierra conexión.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(consulta, params or ())
        if commit:
            conn.commit()
            last_id = cursor.lastrowid
            cursor.close()
            return last_id
        else:
            rows = cursor.fetchall()
            description = cursor.description
            cursor.close()
            return rows, description
    finally:
        if conn.is_connected():
            conn.close()

