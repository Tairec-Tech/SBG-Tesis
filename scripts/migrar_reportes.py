import sys
import os

# Asegurar que el directorio raíz del proyecto esté en el PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.crud_reporte import ejecutar_migracion_reportes

def main():
    print("Iniciando migración manual de la tabla de reportes...")
    try:
        ejecutar_migracion_reportes()
        print("Migración completada con éxito.")
    except Exception as e:
        print(f"Error durante la migración: {e}")

if __name__ == "__main__":
    main()
