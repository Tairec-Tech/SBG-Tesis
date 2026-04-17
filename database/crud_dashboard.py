"""
Operaciones CRUD específicas para el Dashboard (KPIs y estadísticas).
Filtrado por tipo_brigada para aislamiento de datos por tipo de brigada.
"""
from database.connection import ejecutar


def get_kpi_stats(tipo_brigada=None):
    """
    Retorna un diccionario con estadísticas clave, filtradas por tipo_brigada.
    """
    stats = {
        "total_brigadas": 0,
        "total_usuarios": 0,
        "actividades_activas": 0,
        "actividades_completadas": 0
    }

    try:
        if tipo_brigada:
            sql = """
                SELECT 
                    (SELECT COUNT(*) FROM brigada WHERE tipo_brigada = %s) as total_brigadas,
                    (SELECT COUNT(*) FROM usuario u JOIN brigada b ON u.Brigada_idBrigada = b.idBrigada WHERE b.tipo_brigada = %s) as total_usuarios,
                    (SELECT COUNT(*) FROM actividad a JOIN brigada b ON a.Brigada_idBrigada = b.idBrigada WHERE b.tipo_brigada = %s AND a.estado NOT IN ('Completada', 'Cancelada')) as actividades_activas,
                    (SELECT COUNT(*) FROM actividad a JOIN brigada b ON a.Brigada_idBrigada = b.idBrigada WHERE b.tipo_brigada = %s AND a.estado = 'Completada') as actividades_completadas
            """
            rows, _ = ejecutar(sql, (tipo_brigada, tipo_brigada, tipo_brigada, tipo_brigada))
        else:
            sql = """
                SELECT 
                    (SELECT COUNT(*) FROM brigada) as total_brigadas,
                    (SELECT COUNT(*) FROM usuario) as total_usuarios,
                    (SELECT COUNT(*) FROM actividad WHERE estado NOT IN ('Completada', 'Cancelada')) as actividades_activas,
                    (SELECT COUNT(*) FROM actividad WHERE estado = 'Completada') as actividades_completadas
            """
            rows, _ = ejecutar(sql)

        if rows and rows[0]:
            stats["total_brigadas"] = rows[0][0] or 0
            stats["total_usuarios"] = rows[0][1] or 0
            stats["actividades_activas"] = rows[0][2] or 0
            stats["actividades_completadas"] = rows[0][3] or 0

    except Exception as e:
        print(f"Error obteniendo KPIs: {e}")

    return stats

def get_activities_stats_by_month(tipo_brigada=None):
    """
    Retorna cantidad de actividades por mes, filtradas por tipo_brigada.
    """
    if tipo_brigada:
        sql = """
            SELECT DATE_FORMAT(a.fecha_inicio, '%Y-%m') as mes, COUNT(*) as cantidad
            FROM actividad a
            JOIN brigada b ON a.Brigada_idBrigada = b.idBrigada
            WHERE b.tipo_brigada = %s
            GROUP BY mes
            ORDER BY mes DESC
            LIMIT 6
        """
        params = (tipo_brigada,)
    else:
        sql = """
            SELECT DATE_FORMAT(fecha_inicio, '%Y-%m') as mes, COUNT(*) as cantidad
            FROM actividad
            GROUP BY mes
            ORDER BY mes DESC
            LIMIT 6
        """
        params = None

    try:
        rows, _ = ejecutar(sql, params)
        return rows
    except Exception as e:
        print(f"Error stats actividades: {e}")
        return []
