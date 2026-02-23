"""
CRUD para la tabla `reporte_incidente`.
"""
from database.connection import ejecutar

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

def listar_reportes():
    _asegurar_tabla_reporte()
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

def get_reporte_stats():
    _asegurar_tabla_reporte()
    stats = {
        "total": 0,
        "en_proceso": 0,
        "resueltos": 0
    }
    try:
        rows, _ = ejecutar("SELECT COUNT(*) FROM reporte_incidente")
        stats["total"] = rows[0][0] if rows else 0

        rows, _ = ejecutar("SELECT COUNT(*) FROM reporte_incidente WHERE estado != 'Resuelto'")
        stats["en_proceso"] = rows[0][0] if rows else 0

        rows, _ = ejecutar("SELECT COUNT(*) FROM reporte_incidente WHERE estado = 'Resuelto'")
        stats["resueltos"] = rows[0][0] if rows else 0
    except Exception as e:
        print(f"Error stats reporte: {e}")
    return stats
