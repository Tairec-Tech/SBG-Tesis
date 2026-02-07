"""
Configuración de la base de datos MySQL.
Usa variables de entorno o el archivo .env en la raíz del proyecto.

Errores típicos si el login "no hace nada" o falla:
- "Unknown database 'db_brigadas_maracaibo'" → Crear la BD en MySQL (ej. ejecutar database/db_brigadas_fixed.sql).
- "Access denied for user 'root'" → Contraseña incorrecta: poner SBG_DB_PASSWORD en .env (XAMPP suele usar "").
- "Can't connect to MySQL server" → Servidor MySQL (XAMPP) no está iniciado.
"""
import os

from dotenv import load_dotenv
load_dotenv()

DB_HOST = os.environ.get("SBG_DB_HOST", "localhost")
DB_PORT = int(os.environ.get("SBG_DB_PORT", "3306"))
DB_USER = os.environ.get("SBG_DB_USER", "root")
DB_PASSWORD = os.environ.get("SBG_DB_PASSWORD", "")
DB_NAME = os.environ.get("SBG_DB_NAME", "db_brigadas_maracaibo")
