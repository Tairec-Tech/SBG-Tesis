"""
Operaciones CRUD para la tabla Actividad.
Filtrado por tipo_brigada para aislamiento de datos.
Incluye soporte para marcar actividades como completadas por su creador
(o por un administrador) cuando la base de datos tenga aplicada la migración
que añade Usuario_idUsuarioCreador.
"""
from database.connection import ejecutar, ejecutar_modificar


def obtener_actividades_recientes(limite=5, tipo_brigada=None, solo_usuario_id=None):
    """
    Retorna las últimas 'limite' actividades, filtradas por tipo_brigada.
    Si solo_usuario_id se proporciona, solo devuelve las del creador indicado.
    """
    condiciones = []
    params = []

    if tipo_brigada:
        condiciones.append("b.tipo_brigada = %s")
        params.append(tipo_brigada)

    if solo_usuario_id is not None:
        condiciones.append("a.Usuario_idUsuarioCreador = %s")
        params.append(solo_usuario_id)

    where = ("WHERE " + " AND ".join(condiciones)) if condiciones else ""

    sql = f"""
        SELECT a.idActividad, a.titulo, a.descripcion, a.fecha_inicio, a.fecha_fin,
               a.estado, a.Brigada_idBrigada, a.Usuario_idUsuarioCreador AS creador_id,
               b.nombre_brigada
        FROM actividad a
        LEFT JOIN brigada b ON a.Brigada_idBrigada = b.idBrigada
        {where}
        ORDER BY a.fecha_inicio DESC
        LIMIT %s
    """
    params.append(limite)

    try:
        rows, description = ejecutar(sql, tuple(params))
        if not rows:
            return []
        columnas = [col[0] for col in description]
        return [dict(zip(columnas, fila)) for fila in rows]
    except Exception as e:
        print(f"Error obteniendo actividades recientes: {e}")
        return []


def crear_actividad(titulo, descripcion, fecha_inicio, fecha_fin, estado, id_brigada, usuario_creador_id=None):
    """Crea una nueva actividad."""
    if usuario_creador_id is not None:
        sql = """
            INSERT INTO actividad (
                titulo, descripcion, fecha_inicio, fecha_fin, estado,
                Brigada_idBrigada, Usuario_idUsuarioCreador
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (titulo, descripcion, fecha_inicio, fecha_fin, estado, id_brigada, usuario_creador_id)
    else:
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


def actualizar_actividad(id_actividad: int, titulo: str, descripcion: str,
                         fecha_inicio: str, fecha_fin: str, estado: str,
                         usuario_id: int, es_admin_usuario: bool = False) -> bool:
    """
    Actualiza una actividad existente.
    - Un admin puede editar cualquier actividad.
    - Un profesor solo puede editar si es el creador.
    """
    try:
        if es_admin_usuario:
            sql = """
                UPDATE actividad
                SET titulo = %s, descripcion = %s, fecha_inicio = %s,
                    fecha_fin = %s, estado = %s
                WHERE idActividad = %s
            """
            params = (titulo, descripcion, fecha_inicio, fecha_fin, estado, id_actividad)
        else:
            sql = """
                UPDATE actividad
                SET titulo = %s, descripcion = %s, fecha_inicio = %s,
                    fecha_fin = %s, estado = %s
                WHERE idActividad = %s AND Usuario_idUsuarioCreador = %s
            """
            params = (titulo, descripcion, fecha_inicio, fecha_fin, estado, id_actividad, usuario_id)

        afectadas = ejecutar_modificar(sql, params)
        return afectadas > 0
    except Exception as e:
        print(f"Error actualizando actividad: {e}")
        return False


def eliminar_actividad(id_actividad: int, usuario_id: int, es_admin_usuario: bool = False) -> str | None:
    """
    Elimina una actividad.
    - Un admin puede eliminar cualquier actividad.
    - Un profesor solo puede eliminar si es el creador.
    Retorna None si fue exitoso, o un string de error si no.
    """
    try:
        # Verificar dependencias (reportes de impacto, indicadores, reportes de actividad)
        for tabla, col in [
            ("reporte_de_impacto", "Actividad_idActividad"),
            ("indicador_ambiental", "Actividad_idActividad"),
            ("reporte_actividad", "Actividad_idActividad"),
        ]:
            sql_check = f"SELECT COUNT(*) FROM {tabla} WHERE {col} = %s"
            rows, _ = ejecutar(sql_check, (id_actividad,))
            if rows and rows[0][0] > 0:
                return f"No se puede eliminar: hay registros asociados en {tabla}."

        if es_admin_usuario:
            sql = "DELETE FROM actividad WHERE idActividad = %s"
            params = (id_actividad,)
        else:
            sql = "DELETE FROM actividad WHERE idActividad = %s AND Usuario_idUsuarioCreador = %s"
            params = (id_actividad, usuario_id)

        afectadas = ejecutar_modificar(sql, params)
        if afectadas > 0:
            return None
        return "No se pudo eliminar. Verifique permisos."
    except Exception as e:
        print(f"Error eliminando actividad: {e}")
        return f"Error: {e}"


def marcar_actividad_completada(id_actividad: int, usuario_id: int, es_admin_usuario: bool = False) -> bool:
    """
    Marca una actividad como 'Completada'.
    - Un administrador puede completar cualquier actividad.
    - Un profesor solo puede completar la actividad si es su creador.
    Requiere la columna Usuario_idUsuarioCreador en la tabla actividad.
    """
    try:
        if es_admin_usuario:
            sql = """
                UPDATE actividad
                SET estado = 'Completada'
                WHERE idActividad = %s AND estado <> 'Completada'
            """
            params = (id_actividad,)
        else:
            sql = """
                UPDATE actividad
                SET estado = 'Completada'
                WHERE idActividad = %s
                  AND Usuario_idUsuarioCreador = %s
                  AND estado <> 'Completada'
            """
            params = (id_actividad, usuario_id)

        afectadas = ejecutar_modificar(sql, params)
        return afectadas > 0
    except Exception as e:
        print(f"Error marcando actividad como completada: {e}")
        return False


def obtener_actividad_por_id(id_actividad: int) -> dict | None:
    """Retorna los datos de una actividad específica."""
    sql = """
        SELECT a.idActividad, a.titulo, a.descripcion, a.fecha_inicio, a.fecha_fin,
               a.estado, a.Brigada_idBrigada, a.Usuario_idUsuarioCreador AS creador_id,
               b.nombre_brigada
        FROM actividad a
        LEFT JOIN brigada b ON a.Brigada_idBrigada = b.idBrigada
        WHERE a.idActividad = %s
    """
    try:
        rows, description = ejecutar(sql, (id_actividad,))
        if not rows:
            return None
        columnas = [col[0] for col in description]
        return dict(zip(columnas, rows[0]))
    except Exception as e:
        print(f"Error obteniendo actividad {id_actividad}: {e}")
        return None


def listar_actividades(tipo_brigada=None):
    """Retorna todas las actividades, filtradas por tipo_brigada."""
    if tipo_brigada:
        sql = """
            SELECT a.idActividad as id, a.titulo, a.estado,
                   a.Brigada_idBrigada, a.Usuario_idUsuarioCreador AS creador_id
            FROM actividad a
            JOIN brigada b ON a.Brigada_idBrigada = b.idBrigada
            WHERE b.tipo_brigada = %s
            ORDER BY a.fecha_inicio DESC
        """
        params = (tipo_brigada,)
    else:
        sql = """
            SELECT idActividad as id, titulo, estado,
                   Brigada_idBrigada, Usuario_idUsuarioCreador AS creador_id
            FROM actividad
            ORDER BY fecha_inicio DESC
        """
        params = None
    try:
        rows, description = ejecutar(sql, params)
        if not rows:
            return []
        columnas = [col[0] for col in description]
        return [dict(zip(columnas, fila)) for fila in rows]
    except Exception as e:
        print(f"Error listando actividades: {e}")
        return []
