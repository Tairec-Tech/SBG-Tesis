"""
Conexión a MySQL para el SBE — con connection pool.
"""
import mysql.connector
from mysql.connector import Error
from mysql.connector.pooling import MySQLConnectionPool

from database.config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

# Pool global: reutiliza conexiones en vez de abrir/cerrar cada vez
_pool = None


def _get_pool():
    """Inicializa el pool de conexiones (lazy, una sola vez)."""
    global _pool
    if _pool is None:
        try:
            _pool = MySQLConnectionPool(
                pool_name="sgb_pool",
                pool_size=5,
                pool_reset_session=True,
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                charset="utf8mb4",
            )
        except Error as e:
            raise RuntimeError(f"Error al crear pool de conexiones: {e}") from e
    return _pool


def get_connection():
    """Obtiene una conexión del pool. Cerrar con conn.close() (la devuelve al pool)."""
    try:
        return _get_pool().get_connection()
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
