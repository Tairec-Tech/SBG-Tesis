"""
Operaciones CRUD específicas para el Dashboard (KPIs y estadísticas).
"""
from database.connection import ejecutar


def get_kpi_stats():
    """
    Retorna un diccionario con estadísticas clave.
    """
    stats = {
        "total_brigadas": 0,
        "total_usuarios": 0,
        "actividades_activas": 0,
        "actividades_completadas": 0
    }
    
    try:
        # Total Brigadas
        rows, _ = ejecutar("SELECT COUNT(*) FROM brigada")
        stats["total_brigadas"] = rows[0][0] if rows else 0

        # Total Usuarios
        rows, _ = ejecutar("SELECT COUNT(*) FROM usuario")
        stats["total_usuarios"] = rows[0][0] if rows else 0
        
        # Actividades Activas
        rows, _ = ejecutar("SELECT COUNT(*) FROM actividad WHERE estado NOT IN ('Completada', 'Cancelada')")
        stats["actividades_activas"] = rows[0][0] if rows else 0

        # Actividades Completadas
        rows, _ = ejecutar("SELECT COUNT(*) FROM actividad WHERE estado = 'Completada'")
        stats["actividades_completadas"] = rows[0][0] if rows else 0

    except Exception as e:
        print(f"Error obteniendo KPIs: {e}")
    
    return stats

def get_activities_stats_by_month():
    """
    Retorna cantidad de actividades por mes para gráficas.
    """
    sql = """
        SELECT DATE_FORMAT(fecha_inicio, '%Y-%m') as mes, COUNT(*) as cantidad
        FROM actividad
        GROUP BY mes
        ORDER BY mes DESC
        LIMIT 6
    """
    try:
        rows, _ = ejecutar(sql)
        return rows # Lista de tuplas
    except Exception as e:
        print(f"Error stats actividades: {e}")
        return []
