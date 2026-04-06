"""
CRUD para la tabla `reporte_incidente`, `reporte_actividad`, `reporte_de_impacto`.
Filtrado por tipo_brigada para aislamiento de datos.
"""
from database.connection import ejecutar

# ==============================================================
# AUTO-MIGRACIÓN (se ejecuta una sola vez; idempotente)
# ==============================================================

def _migrar_reportes():
    """Aplica migraciones necesarias para alinear las tablas con los escenarios SBE."""
    migraciones = [
        # --- reporte_de_impacto: nuevos campos ---
        "ALTER TABLE `reporte_de_impacto` ADD COLUMN `brigada` VARCHAR(100) NULL AFTER `contenido`",
        "ALTER TABLE `reporte_de_impacto` ADD COLUMN `area_evaluada` VARCHAR(200) NULL AFTER `brigada`",
        "ALTER TABLE `reporte_de_impacto` ADD COLUMN `indicador` VARCHAR(100) NULL AFTER `area_evaluada`",
        "ALTER TABLE `reporte_de_impacto` ADD COLUMN `valor` VARCHAR(50) NULL AFTER `indicador`",
        "ALTER TABLE `reporte_de_impacto` ADD COLUMN `unidad` VARCHAR(50) NULL AFTER `valor`",
        # --- reporte_de_impacto: Actividad opcional ---
        "ALTER TABLE `reporte_de_impacto` MODIFY COLUMN `Actividad_idActividad` INT(11) NULL",
        # --- reporte_de_impacto: contenido nullable ---
        "ALTER TABLE `reporte_de_impacto` MODIFY COLUMN `contenido` TEXT NULL",
        # --- reporte_actividad: campo participantes ---
        "ALTER TABLE `reporte_actividad` ADD COLUMN `participantes` VARCHAR(500) NULL AFTER `resumen`",
    ]
    for sql in migraciones:
        try:
            ejecutar(sql, commit=True)
        except Exception as e:
            msg = str(e).lower()
            if "duplicate column" in msg or "duplicate" in msg:
                pass  # Ya existe, ignorar
            else:
                print(f"[migración reportes] {e}")

_migrar_reportes()

# ==============================================================
# REPORTE DE INCIDENTES
# ==============================================================

def _asegurar_tabla_reporte():
    sql = """
    CREATE TABLE IF NOT EXISTS `reporte_incidente` (
      `idReporte` INT(11) NOT NULL AUTO_INCREMENT,
      `titulo` VARCHAR(100) NOT NULL,
      `descripcion` TEXT NOT NULL,
      `ubicacion` VARCHAR(200) NOT NULL,
      `prioridad` VARCHAR(50) NOT NULL,
      `estado` VARCHAR(50) NOT NULL DEFAULT 'En Proceso',
      `Brigada_idBrigada` INT(11) NOT NULL,
      `creado_en` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
      `actualizado_en` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      PRIMARY KEY (`idReporte`),
      KEY `fk_reporte_brigada_idx` (`Brigada_idBrigada`),
      CONSTRAINT `fk_reporte_brigada` FOREIGN KEY (`Brigada_idBrigada`)
        REFERENCES `brigada` (`idBrigada`) ON DELETE CASCADE ON UPDATE NO ACTION
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
    """
    try:
        ejecutar(sql, commit=True)
    except Exception as e:
        print(f"[reporte] tabla ya existe o error: {e}")

def crear_reporte(titulo: str, descripcion: str, ubicacion: str, prioridad: str, brigada_id: int) -> int | None:
    _asegurar_tabla_reporte()
    sql = """
    INSERT INTO reporte_incidente (titulo, descripcion, ubicacion, prioridad, Brigada_idBrigada)
    VALUES (%s, %s, %s, %s, %s)
    """
    try:
        lid = ejecutar(sql, (titulo, descripcion, ubicacion, prioridad, brigada_id), commit=True)
        return lid
    except Exception as e:
        print(f"Error creando reporte: {e}")
        return None

def listar_reportes(tipo_brigada=None):
    _asegurar_tabla_reporte()
    if tipo_brigada:
        sql = """
        SELECT r.idReporte, r.titulo, r.descripcion, r.ubicacion, r.prioridad, r.estado, r.creado_en, 
               b.nombre_brigada, b.color_identificador
        FROM reporte_incidente r
        JOIN brigada b ON r.Brigada_idBrigada = b.idBrigada
        WHERE b.tipo_brigada = %s
        ORDER BY r.creado_en DESC
        """
        rows, _ = ejecutar(sql, (tipo_brigada,))
    else:
        sql = """
        SELECT r.idReporte, r.titulo, r.descripcion, r.ubicacion, r.prioridad, r.estado, r.creado_en, 
               b.nombre_brigada, b.color_identificador
        FROM reporte_incidente r
        JOIN brigada b ON r.Brigada_idBrigada = b.idBrigada
        ORDER BY r.creado_en DESC
        """
        rows, _ = ejecutar(sql)
    reportes = []
    for r in rows:
        reportes.append({
            "id": r[0],
            "titulo": r[1],
            "descripcion": r[2],
            "ubicacion": r[3],
            "prioridad": r[4],
            "estado": r[5],
            "fecha": r[6],
            "brigada": r[7],
            "color_brigada": r[8] or "#2563eb",
        })
    return reportes

def actualizar_estado(id_reporte: int, nuevo_estado: str) -> bool:
    sql = "UPDATE reporte_incidente SET estado = %s WHERE idReporte = %s"
    try:
        ejecutar(sql, (nuevo_estado, id_reporte), commit=True)
        return True
    except Exception as e:
        print(f"Error actualizando estado del reporte: {e}")
        return False

def get_reporte_stats(tipo_brigada=None):
    _asegurar_tabla_reporte()
    stats = {
        "total": 0,
        "en_proceso": 0,
        "resueltos": 0
    }
    try:
        if tipo_brigada:
            rows, _ = ejecutar("SELECT COUNT(*) FROM reporte_incidente r JOIN brigada b ON r.Brigada_idBrigada = b.idBrigada WHERE b.tipo_brigada = %s", (tipo_brigada,))
            stats["total"] = rows[0][0] if rows else 0
            rows, _ = ejecutar("SELECT COUNT(*) FROM reporte_incidente r JOIN brigada b ON r.Brigada_idBrigada = b.idBrigada WHERE b.tipo_brigada = %s AND r.estado != 'Resuelto'", (tipo_brigada,))
            stats["en_proceso"] = rows[0][0] if rows else 0
            rows, _ = ejecutar("SELECT COUNT(*) FROM reporte_incidente r JOIN brigada b ON r.Brigada_idBrigada = b.idBrigada WHERE b.tipo_brigada = %s AND r.estado = 'Resuelto'", (tipo_brigada,))
            stats["resueltos"] = rows[0][0] if rows else 0
        else:
            rows, _ = ejecutar("SELECT COUNT(*) FROM reporte_incidente")
            stats["total"] = rows[0][0] if rows else 0
            rows, _ = ejecutar("SELECT COUNT(*) FROM reporte_incidente WHERE estado != 'Resuelto'")
            stats["en_proceso"] = rows[0][0] if rows else 0
            rows, _ = ejecutar("SELECT COUNT(*) FROM reporte_incidente WHERE estado = 'Resuelto'")
            stats["resueltos"] = rows[0][0] if rows else 0
    except Exception as e:
        print(f"Error stats reporte: {e}")
    return stats

# ==========================================================
# REPORTES DE ACTIVIDADES
# ==========================================================

def listar_reportes_actividad(tipo_brigada=None):
    """Obtiene los reportes de actividades, filtrados por tipo_brigada."""
    if tipo_brigada:
        sql = """
        SELECT 
            r.idReporte_actividad, 
            r.resumen, 
            r.resultado, 
            r.fecha_reporte,
            a.titulo AS actividad_titulo, 
            a.fecha_inicio AS actividad_fecha,
            u.nombre, u.apellido,
            r.participantes
        FROM reporte_actividad r
        LEFT JOIN actividad a ON r.Actividad_idActividad = a.idActividad
        LEFT JOIN brigada b ON a.Brigada_idBrigada = b.idBrigada
        LEFT JOIN usuario u ON r.Usuario_idUsuario = u.idUsuario
        WHERE b.tipo_brigada = %s
        ORDER BY r.fecha_reporte DESC
        """
        rows, _ = ejecutar(sql, (tipo_brigada,))
    else:
        sql = """
        SELECT 
            r.idReporte_actividad, 
            r.resumen, 
            r.resultado, 
            r.fecha_reporte,
            a.titulo AS actividad_titulo, 
            a.fecha_inicio AS actividad_fecha,
            u.nombre, u.apellido,
            r.participantes
        FROM reporte_actividad r
        LEFT JOIN actividad a ON r.Actividad_idActividad = a.idActividad
        LEFT JOIN usuario u ON r.Usuario_idUsuario = u.idUsuario
        ORDER BY r.fecha_reporte DESC
        """
        rows, _ = ejecutar(sql)
    reportes = []
    for r in rows:
        reportes.append({
            "id": r[0],
            "resumen": r[1],
            "resultado": r[2],
            "fecha_reporte": r[3],
            "actividad_titulo": r[4] or "Desconocida",
            "actividad_fecha": r[5],
            "usuario_nombre": f"{r[6] or ''} {r[7] or ''}".strip() or "Sistema",
            "participantes": r[8] or "",
        })
    return reportes

def crear_reporte_actividad(resumen: str, resultado: str, actividad_id: int, usuario_id: int, participantes: str = "") -> int | None:
    sql = """
    INSERT INTO reporte_actividad (resumen, participantes, resultado, Actividad_idActividad, Usuario_idUsuario)
    VALUES (%s, %s, %s, %s, %s)
    """
    try:
        lid = ejecutar(sql, (resumen, participantes, resultado, actividad_id, usuario_id), commit=True)
        return lid
    except Exception as e:
        print(f"Error creando reporte actividad: {e}")
        return None

# ==========================================================
# REPORTES DE IMPACTO
# ==========================================================

def listar_reportes_impacto(tipo_brigada=None):
    """Obtiene los reportes de impacto, filtrados por tipo_brigada."""
    if tipo_brigada:
        sql = """
        SELECT 
            i.idReporte_impacto, 
            i.contenido, 
            i.fecha_generacion,
            a.titulo AS actividad_titulo,
            u.nombre, u.apellido,
            i.brigada,
            i.area_evaluada,
            i.indicador,
            i.valor,
            i.unidad
        FROM reporte_de_impacto i
        LEFT JOIN actividad a ON i.Actividad_idActividad = a.idActividad
        LEFT JOIN brigada b ON a.Brigada_idBrigada = b.idBrigada
        LEFT JOIN usuario u ON i.Usuario_idUsuario = u.idUsuario
        WHERE b.tipo_brigada = %s
        ORDER BY i.fecha_generacion DESC
        """
        rows, _ = ejecutar(sql, (tipo_brigada,))
    else:
        sql = """
        SELECT 
            i.idReporte_impacto, 
            i.contenido, 
            i.fecha_generacion,
            a.titulo AS actividad_titulo,
            u.nombre, u.apellido,
            i.brigada,
            i.area_evaluada,
            i.indicador,
            i.valor,
            i.unidad
        FROM reporte_de_impacto i
        LEFT JOIN actividad a ON i.Actividad_idActividad = a.idActividad
        LEFT JOIN usuario u ON i.Usuario_idUsuario = u.idUsuario
        ORDER BY i.fecha_generacion DESC
        """
        rows, _ = ejecutar(sql)
    reportes = []
    for r in rows:
        reportes.append({
            "id": r[0],
            "contenido": r[1] or "",
            "fecha_generacion": r[2],
            "actividad_titulo": r[3] or "",
            "usuario_nombre": f"{r[4] or ''} {r[5] or ''}".strip() or "Sistema",
            "brigada": r[6] or "",
            "area_evaluada": r[7] or "",
            "indicador": r[8] or "",
            "valor": r[9] or "",
            "unidad": r[10] or "",
        })
    return reportes

def crear_reporte_impacto(
    usuario_id: int,
    brigada: str = "",
    area_evaluada: str = "",
    indicador: str = "",
    valor: str = "",
    unidad: str = "",
    contenido: str = "",
    actividad_id: int | None = None,
) -> int | None:
    sql = """
    INSERT INTO reporte_de_impacto 
        (contenido, brigada, area_evaluada, indicador, valor, unidad, Actividad_idActividad, Usuario_idUsuario)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    try:
        lid = ejecutar(sql, (
            contenido or None,
            brigada or None,
            area_evaluada or None,
            indicador or None,
            valor or None,
            unidad or None,
            actividad_id,
            usuario_id,
        ), commit=True)
        return lid
    except Exception as e:
        print(f"Error creando reporte impacto: {e}")
        return None
