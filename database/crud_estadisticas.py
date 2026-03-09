"""
Operaciones CRUD dedicadas a la pantalla de Estadísticas.
Extrae KPIs globales y métricas temporales/agrupadas para gráficos.
"""
from database.connection import ejecutar

def get_kpis_estadisticas():
    """Calcula 5 KPIs de alto impacto para la fila superior de estadísticas."""
    kpis = {
        "voluntariado_activo": 0,
        "horas_invertidas": 0,
        "despliegue_operativo": 0, # % de brigadas con actividades completadas
        "impacto_documentado": 0,
        "tasa_efectividad": 0
    }
    
    try:
        # 1. Voluntariado Activo (Estudiantes con rol de Brigadista)
        rows, _ = ejecutar("SELECT COUNT(*) FROM usuario WHERE rol = 'Brigadista'")
        kpis["voluntariado_activo"] = rows[0][0] if rows else 0
        
        # 2. Horas Invertidas (Diferencia acumulada en horas de actividades exitosas)
        # Asumiendo que pueden haber fechas nulas o actividades sin fin, usamos COALESCE o revisamos no nulos.
        sql_horas = """
            SELECT SUM(TIMESTAMPDIFF(HOUR, fecha_inicio, fecha_fin)) 
            FROM actividad 
            WHERE estado = 'Completada' 
            AND fecha_inicio IS NOT NULL 
            AND fecha_fin IS NOT NULL
        """
        rows, _ = ejecutar(sql_horas)
        kpis["horas_invertidas"] = int(rows[0][0]) if rows and rows[0][0] else 0
        
        # 3. Despliegue Operativo (% de brigadas en calle o con al menos 1 actividad registrada)
        rows_total_brigadas, _ = ejecutar("SELECT COUNT(*) FROM brigada")
        total_brigadas = rows_total_brigadas[0][0] if rows_total_brigadas else 0
        
        rows_brigadas_activas, _ = ejecutar("SELECT COUNT(DISTINCT Brigada_idBrigada) FROM actividad")
        brigadas_activas = rows_brigadas_activas[0][0] if rows_brigadas_activas else 0
        
        if total_brigadas > 0:
            kpis["despliegue_operativo"] = round((brigadas_activas / total_brigadas) * 100)
        
        # 4. Impacto Documentado
        rows, _ = ejecutar("SELECT COUNT(*) FROM reporte_de_impacto")
        kpis["impacto_documentado"] = rows[0][0] if rows else 0
        
        # 5. Tasa de Efectividad (% de actividades que no fueron Canceladas vs el Total creado)
        rows_act_totales, _ = ejecutar("SELECT COUNT(*) FROM actividad")
        total_actividades = rows_act_totales[0][0] if rows_act_totales else 0
        
        sql_completadas = "SELECT COUNT(*) FROM actividad WHERE estado = 'Completada'"
        rows_completadas, _ = ejecutar(sql_completadas)
        completadas = rows_completadas[0][0] if rows_completadas else 0
        
        if total_actividades > 0:
            kpis["tasa_efectividad"] = round((completadas / total_actividades) * 100)

    except Exception as e:
        print(f"Error calculando KPIs de estadísticas: {e}")
        
    return kpis


def get_actividades_por_mes():
    """Retorna conteo de actividades de los últimos 6 meses (BarChart)."""
    sql = """
        SELECT DATE_FORMAT(fecha_inicio, '%Y-%m') as mes, COUNT(*) as cantidad
        FROM actividad
        WHERE fecha_inicio IS NOT NULL
        GROUP BY mes
        ORDER BY mes DESC
        LIMIT 6
    """
    try:
        rows, _ = ejecutar(sql)
        # Devolver orden cronológico (de más antiguo a más reciente de los últimos 6)
        return list(reversed(rows))
    except Exception as e:
        print(f"Error agrupando actividades por mes: {e}")
        return []


def get_tendencia_reportes_por_mes():
    """Cuenta todos los reportes (incidentes + impacto + actividad) por mes (LineChart)."""
    # Usamos UNION ALL para juntar las fechas de las 3 tablas de reportes y las agrupamos
    sql = """
        SELECT DATE_FORMAT(fecha, '%Y-%m') as mes, COUNT(*) as cantidad
        FROM (
            SELECT creado_en as fecha FROM reporte_incidente
            UNION ALL
            SELECT fecha_generacion as fecha FROM reporte_de_impacto
            UNION ALL
            SELECT fecha_reporte as fecha FROM reporte_actividad
        ) as todos_reportes
        WHERE fecha IS NOT NULL
        GROUP BY mes
        ORDER BY mes DESC
        LIMIT 6
    """
    try:
        rows, _ = ejecutar(sql)
        return list(reversed(rows))
    except Exception as e:
        print(f"Error agrupando reportes por mes: {e}")
        return []


def get_distribucion_estados_actividades():
    """Retorna desglose del estado de las actividades (PieChart)."""
    sql = """
        SELECT estado, COUNT(*) as conteo
        FROM actividad
        GROUP BY estado
    """
    try:
        rows, _ = ejecutar(sql)
        if not rows:
            return []
        # Return format: [{"estado": "Completada", "conteo": 5}, ...]
        return [{"estado": fila[0], "conteo": fila[1]} for fila in rows]
    except Exception as e:
        print(f"Error agrupando estados: {e}")
        return []
