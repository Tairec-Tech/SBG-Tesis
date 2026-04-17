"""
Conexión a MySQL para el SBE — con connection pool.
"""
import time
from time import perf_counter
import mysql.connector
from mysql.connector import Error
from mysql.connector.pooling import MySQLConnectionPool
import os
import sys

from database.config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME


if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SSL_CA_PATH = os.path.join(BASE_DIR, "ca.pem")
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
                connection_timeout=10,
                ssl_ca=SSL_CA_PATH,
                ssl_disabled=False,
                use_pure=True  # Previene errores de extensión C en empaquetado
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
    t0 = perf_counter()
    conn = get_connection()
    t_conn = perf_counter()
    try:
        cursor = conn.cursor()
        cursor.execute(consulta, params or ())
        t_exec = perf_counter()
        if commit:
            conn.commit()
            last_id = cursor.lastrowid
            cursor.close()
            t_fetch = perf_counter()
            print(f"[DB] conn={t_conn-t0:.3f}s exec={t_exec-t_conn:.3f}s fetch={t_fetch-t_exec:.3f}s total={t_fetch-t0:.3f}s | Q: {consulta.strip()[:60]}...")
            return last_id
        else:
            rows = cursor.fetchall()
            description = cursor.description
            cursor.close()
            t_fetch = perf_counter()
            print(f"[DB] conn={t_conn-t0:.3f}s exec={t_exec-t_conn:.3f}s fetch={t_fetch-t_exec:.3f}s total={t_fetch-t0:.3f}s | Q: {consulta.strip()[:60]}...")
            return rows, description
    finally:
        if conn.is_connected():
            conn.close()


def ejecutar_modificar(consulta, params=None):
    """
    Ejecuta un UPDATE o DELETE y retorna el número de filas afectadas (rowcount).
    Hace commit automáticamente.
    """
    t0 = perf_counter()
    conn = get_connection()
    t_conn = perf_counter()
    try:
        cursor = conn.cursor()
        cursor.execute(consulta, params or ())
        t_exec = perf_counter()
        conn.commit()
        afectadas = cursor.rowcount
        cursor.close()
        t_fetch = perf_counter()
        print(f"[DB] conn={t_conn-t0:.3f}s exec={t_exec-t_conn:.3f}s commit={t_fetch-t_exec:.3f}s total={t_fetch-t0:.3f}s | Q: {consulta.strip()[:60]}...")
        return afectadas
    finally:
        if conn.is_connected():
            conn.close()
