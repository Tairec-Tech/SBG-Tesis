"""
Operaciones CRUD para la tabla Actividad.
"""
from database.connection import ejecutar

def obtener_actividades_recientes(limite=5):
    """Retorna las últimas 'limite' actividades registradas."""
    sql = """
        SELECT a.idActividad, a.titulo, a.descripcion, a.fecha_inicio, a.estado, b.nombre_brigada
        FROM actividad a
        LEFT JOIN brigada b ON a.Brigada_idBrigada = b.idBrigada
        ORDER BY a.fecha_inicio DESC
        LIMIT %s
    """
    try:
        rows, description = ejecutar(sql, (limite,))
        if not rows:
            return []
        columnas = [col[0] for col in description]
        resultados = [dict(zip(columnas, fila)) for fila in rows]
        return resultados
    except Exception as e:
        print(f"Error obteniendo actividades recientes: {e}")
        return []

def crear_actividad(titulo, descripcion, fecha_inicio, fecha_fin, estado, id_brigada):
    """Crea una nueva actividad."""
    sql = """
        INSERT INTO actividad (titulo, descripcion, fecha_inicio, fecha_fin, estado, Brigada_idBrigada)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    params = (titulo, descripcion, fecha_inicio, fecha_fin, estado, id_brigada)
    try:
        return ejecutar(sql, params, commit=True)
    except Exception as e:
        print(f"Error creando actividad: {e}")
        return None
