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
            # Total Brigadas de este tipo
            rows, _ = ejecutar("SELECT COUNT(*) FROM brigada WHERE tipo_brigada = %s", (tipo_brigada,))
            stats["total_brigadas"] = rows[0][0] if rows else 0

            # Total Usuarios en brigadas de este tipo
            rows, _ = ejecutar(
                "SELECT COUNT(*) FROM usuario u JOIN brigada b ON u.Brigada_idBrigada = b.idBrigada WHERE b.tipo_brigada = %s",
                (tipo_brigada,)
            )
            stats["total_usuarios"] = rows[0][0] if rows else 0

            # Actividades Activas en brigadas de este tipo
            rows, _ = ejecutar(
                "SELECT COUNT(*) FROM actividad a JOIN brigada b ON a.Brigada_idBrigada = b.idBrigada WHERE b.tipo_brigada = %s AND a.estado NOT IN ('Completada', 'Cancelada')",
                (tipo_brigada,)
            )
            stats["actividades_activas"] = rows[0][0] if rows else 0

            # Actividades Completadas
            rows, _ = ejecutar(
                "SELECT COUNT(*) FROM actividad a JOIN brigada b ON a.Brigada_idBrigada = b.idBrigada WHERE b.tipo_brigada = %s AND a.estado = 'Completada'",
                (tipo_brigada,)
            )
            stats["actividades_completadas"] = rows[0][0] if rows else 0
        else:
            rows, _ = ejecutar("SELECT COUNT(*) FROM brigada")
            stats["total_brigadas"] = rows[0][0] if rows else 0
            rows, _ = ejecutar("SELECT COUNT(*) FROM usuario")
            stats["total_usuarios"] = rows[0][0] if rows else 0
            rows, _ = ejecutar("SELECT COUNT(*) FROM actividad WHERE estado NOT IN ('Completada', 'Cancelada')")
            stats["actividades_activas"] = rows[0][0] if rows else 0
            rows, _ = ejecutar("SELECT COUNT(*) FROM actividad WHERE estado = 'Completada'")
            stats["actividades_completadas"] = rows[0][0] if rows else 0

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
