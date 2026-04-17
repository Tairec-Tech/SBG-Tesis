import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

host = os.environ.get("SBE_DB_HOST")
port = int(os.environ.get("SBE_DB_PORT", "14197"))
user = os.environ.get("SBE_DB_USER")
password = os.environ.get("SBE_DB_PASSWORD")
database = os.environ.get("SBE_DB_NAME", "defaultdb")

print(f"[*] Conectando a Aiven MySQL (Host: {host}, BD: {database})...")

try:
    conn = mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        ssl_ca="", 
        use_pure=True
    )
    cursor = conn.cursor()
    print("[+] Conexión exitosa!")
except Exception as e:
    print(f"[!] Error de conexión: {e}")
    exit(1)

archivos_sql = [
    "database/db_brigadas_maracaibo.sql",
    "database/migracion_actividad_creador.sql",
    "database/migracion_reportes.sql",
    "database/migrate_mensaje_dia.sql",
    "database/seed_super.sql"
]

for ruta in archivos_sql:
    print(f"\n[*] Procesando {ruta}...")
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            sql = f.read()
            
        # Remover o reemplazar líneas problemáticas en la nube para no chocar con Aiven
        lineas_limpias = []
        for linea in sql.split("\n"):
            if "CREATE DATABASE" in linea.upper() or "USE " in linea.upper():
                continue
            lineas_limpias.append(linea)
            
        sql_limpio = "\n".join(lineas_limpias)

        # Ejecutar instrucción a instrucción
        for instruccion in sql_limpio.split(';'):
            instruccion = instruccion.strip()
            if not instruccion:
                continue
                
            # Parche para MySQL 8 vs IF NOT EXISTS en migraciones
            if "ADD COLUMN IF NOT EXISTS" in instruccion:
                instruccion = instruccion.replace("ADD COLUMN IF NOT EXISTS", "ADD COLUMN")
                
            try:
                cursor.execute(instruccion)
            except Exception as e:
                # Ignorar error de 'Duplicate column name' si ocurre al quitar el IF NOT EXISTS
                if "Duplicate column name" in str(e):
                    continue
                # Si es un error crítico, imprimir en nueva línea y no sobreescribir la consola
                print(f"\n[!] Falló instrucción de {ruta}. Error: {e}")
                print(f"    Consulta: {instruccion[:100]}...")
                
        print(f"\n[+] {ruta} procesado.")
    except Exception as e:
        print(f"\n[!] Error fatal al procesar archivo {ruta}: {e}")

conn.commit()
cursor.close()
conn.close()

print("\n[✔] ¡MIGRACIÓN A AIVEN COMPLETADA EXITOSAMENTE!")
