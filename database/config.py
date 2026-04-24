"""
Configuración de la base de datos MySQL.
Usa variables de entorno o el archivo .env en la raíz del proyecto.
El sistema soporta SBE_ENV=local|production para aislamiento de BBDD.
"""
import os
import sys

from dotenv import load_dotenv

if getattr(sys, 'frozen', False):
    # Si es .exe, el .env debe estar al lado del .exe compilado
    env_path = os.path.join(os.path.dirname(sys.executable), '.env')
    load_dotenv(env_path)
else:
    load_dotenv()

SBE_ENV = os.environ.get("SBE_ENV", "local").lower()

if SBE_ENV == "production":
    print("[SYSTEM] Arrancando en modo PRODUCCIÓN (Nube)")
    DB_HOST = os.environ.get("SBE_DB_HOST_PROD", "localhost")
    DB_PORT = int(os.environ.get("SBE_DB_PORT_PROD", "3306"))
    DB_USER = os.environ.get("SBE_DB_USER_PROD", "root")
    DB_PASSWORD = os.environ.get("SBE_DB_PASSWORD_PROD", "")
    DB_NAME = os.environ.get("SBE_DB_NAME_PROD", "db_brigadas_maracaibo")
else:
    print("[SYSTEM] Arrancando en modo LOCAL")
    DB_HOST = os.environ.get("SBE_DB_HOST_LOCAL", "localhost")
    DB_PORT = int(os.environ.get("SBE_DB_PORT_LOCAL", "3306"))
    DB_USER = os.environ.get("SBE_DB_USER_LOCAL", "root")
    DB_PASSWORD = os.environ.get("SBE_DB_PASSWORD_LOCAL", "")
    DB_NAME = os.environ.get("SBE_DB_NAME_LOCAL", "db_brigadas_maracaibo")
