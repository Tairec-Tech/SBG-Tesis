"""
Operaciones CRUD dedicadas a la pantalla de Estadísticas.
Extrae KPIs globales y métricas temporales/agrupadas para gráficos.
Filtrado por tipo_brigada para aislamiento de datos.
"""
from database.connection import ejecutar

def get_kpis_estadisticas(tipo_brigada=None, brigada_rol_id=None):
    """Calcula 5 KPIs de alto impacto, filtrados por brigada_rol_id o tipo_brigada."""
    kpis = {
        "voluntariado_activo": 0,
        "horas_invertidas": 0,
        "despliegue_operativo": 0,
        "impacto_documentado": 0,
        "tasa_efectividad": 0
    }

    try:
        where_b = ""
        params = {}
        if brigada_rol_id is not None:
            where_b = "WHERE b.idBrigada = %(bid)s"
            params["bid"] = brigada_rol_id
        elif tipo_brigada:
            where_b = "WHERE b.tipo_brigada = %(tb)s"
            params["tb"] = tipo_brigada

        if where_b:
            sql = f"""
                SELECT 
                    (SELECT COUNT(*) FROM usuario u JOIN brigada b ON u.Brigada_idBrigada = b.idBrigada {where_b} AND u.rol = 'Brigadista') as voluntariado_activo,
                    (SELECT SUM(TIMESTAMPDIFF(HOUR, a.fecha_inicio, a.fecha_fin)) FROM actividad a JOIN brigada b ON a.Brigada_idBrigada = b.idBrigada {where_b} AND a.estado = 'Completada' AND a.fecha_inicio IS NOT NULL AND a.fecha_fin IS NOT NULL) as horas_invertidas,
                    (SELECT COUNT(*) FROM brigada b {where_b}) as total_brigadas,
                    (SELECT COUNT(DISTINCT a.Brigada_idBrigada) FROM actividad a JOIN brigada b ON a.Brigada_idBrigada = b.idBrigada {where_b}) as brigadas_activas,
                    (SELECT COUNT(*) FROM reporte_de_impacto i JOIN actividad a ON i.Actividad_idActividad = a.idActividad JOIN brigada b ON a.Brigada_idBrigada = b.idBrigada {where_b}) as impacto_documentado,
                    (SELECT COUNT(*) FROM actividad a JOIN brigada b ON a.Brigada_idBrigada = b.idBrigada {where_b}) as total_actividades,
                    (SELECT COUNT(*) FROM actividad a JOIN brigada b ON a.Brigada_idBrigada = b.idBrigada {where_b} AND a.estado = 'Completada') as completadas
            """
        else:
            sql = """
                SELECT 
                    (SELECT COUNT(*) FROM usuario WHERE rol = 'Brigadista') as voluntariado_activo,
                    (SELECT SUM(TIMESTAMPDIFF(HOUR, fecha_inicio, fecha_fin)) FROM actividad WHERE estado = 'Completada' AND fecha_inicio IS NOT NULL AND fecha_fin IS NOT NULL) as horas_invertidas,
                    (SELECT COUNT(*) FROM brigada) as total_brigadas,
                    (SELECT COUNT(DISTINCT Brigada_idBrigada) FROM actividad) as brigadas_activas,
                    (SELECT COUNT(*) FROM reporte_de_impacto) as impacto_documentado,
                    (SELECT COUNT(*) FROM actividad) as total_actividades,
                    (SELECT COUNT(*) FROM actividad WHERE estado = 'Completada') as completadas
            """
        
        rows, _ = ejecutar(sql, params)
        if rows:
            r = rows[0]
            kpis["voluntariado_activo"] = r[0] if r[0] else 0
            kpis["horas_invertidas"] = int(r[1]) if r[1] else 0
            
            total_brigadas = r[2] if r[2] else 0
            brigadas_activas = r[3] if r[3] else 0
            if total_brigadas > 0:
                kpis["despliegue_operativo"] = round((brigadas_activas / total_brigadas) * 100)
                
            kpis["impacto_documentado"] = r[4] if r[4] else 0
            
            total_actividades = r[5] if r[5] else 0
            completadas = r[6] if r[6] else 0
            if total_actividades > 0:
                kpis["tasa_efectividad"] = round((completadas / total_actividades) * 100)

    except Exception as e:
        print(f"Error calculando KPIs de estadísticas: {e}")

    return kpis


def get_actividades_por_mes(tipo_brigada=None, brigada_rol_id=None):
    """Retorna conteo de actividades de los últimos 6 meses (BarChart)."""
    sql = """
        SELECT DATE_FORMAT(a.fecha_inicio, '%Y-%m') as mes, COUNT(*) as cantidad
        FROM actividad a
        JOIN brigada b ON a.Brigada_idBrigada = b.idBrigada
        WHERE a.fecha_inicio IS NOT NULL
    """
    params = []
    if brigada_rol_id is not None:
        sql += " AND b.idBrigada = %s"
        params.append(brigada_rol_id)
    elif tipo_brigada:
        sql += " AND b.tipo_brigada = %s"
        params.append(tipo_brigada)
    
    sql += " GROUP BY mes ORDER BY mes DESC LIMIT 6"
    
    try:
        rows, _ = ejecutar(sql, tuple(params) if params else None)
        return list(reversed(rows))
    except Exception as e:
        print(f"Error agrupando actividades por mes: {e}")
        return []


def get_tendencia_reportes_por_mes(tipo_brigada=None, brigada_rol_id=None):
    """Cuenta reportes por mes (LineChart), filtrado."""
    where_b = ""
    params = []
    if brigada_rol_id is not None:
        where_b = "WHERE b.idBrigada = %s"
        params = [brigada_rol_id, brigada_rol_id, brigada_rol_id]
    elif tipo_brigada:
        where_b = "WHERE b.tipo_brigada = %s"
        params = [tipo_brigada, tipo_brigada, tipo_brigada]
        
    sql = f"""
        SELECT DATE_FORMAT(fecha, '%%Y-%%m') as mes, COUNT(*) as cantidad
        FROM (
            SELECT r.creado_en as fecha FROM reporte_incidente r JOIN brigada b ON r.Brigada_idBrigada = b.idBrigada {where_b}
            UNION ALL
            SELECT i.fecha_generacion as fecha FROM reporte_de_impacto i JOIN actividad a ON i.Actividad_idActividad = a.idActividad JOIN brigada b ON a.Brigada_idBrigada = b.idBrigada {where_b}
            UNION ALL
            SELECT ra.fecha_reporte as fecha FROM reporte_actividad ra JOIN actividad a ON ra.Actividad_idActividad = a.idActividad JOIN brigada b ON a.Brigada_idBrigada = b.idBrigada {where_b}
        ) as todos_reportes
        WHERE fecha IS NOT NULL
        GROUP BY mes ORDER BY mes DESC LIMIT 6
    """
    try:
        rows, _ = ejecutar(sql, tuple(params) if params else None)
        return list(reversed(rows))
    except Exception as e:
        print(f"Error agrupando reportes por mes: {e}")
        return []


def get_distribucion_estados_actividades(tipo_brigada=None, brigada_rol_id=None):
    """Retorna desglose del estado de las actividades (PieChart)."""
    sql = """
        SELECT a.estado, COUNT(*) as conteo
        FROM actividad a
        JOIN brigada b ON a.Brigada_idBrigada = b.idBrigada
        WHERE 1=1
    """
    params = []
    if brigada_rol_id is not None:
        sql += " AND b.idBrigada = %s"
        params.append(brigada_rol_id)
    elif tipo_brigada:
        sql += " AND b.tipo_brigada = %s"
        params.append(tipo_brigada)
        
    sql += " GROUP BY a.estado"
    
    try:
        rows, _ = ejecutar(sql, tuple(params) if params else None)
        if not rows:
            return []
        return [{"estado": fila[0], "conteo": fila[1]} for fila in rows]
    except Exception as e:
        print(f"Error agrupando estados: {e}")
        return []
