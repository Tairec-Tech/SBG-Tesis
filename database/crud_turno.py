"""
CRUD para la tabla `turno` — Turnos y Horarios de Brigadas.
Filtrado por tipo_brigada para aislamiento de datos.
"""
from database.connection import ejecutar, ejecutar_modificar


_TABLA_TURNO_VERIFICADA = False

def _asegurar_tabla_turno():
    """Crea la tabla si no existe."""
    global _TABLA_TURNO_VERIFICADA
    if _TABLA_TURNO_VERIFICADA:
        return
    sql = """
    CREATE TABLE IF NOT EXISTS `turno` (
      `idTurno` INT(11) NOT NULL AUTO_INCREMENT,
      `Brigada_idBrigada` INT(11) NOT NULL,
      `fecha` DATE NOT NULL,
      `hora_inicio` TIME NOT NULL,
      `hora_fin` TIME NOT NULL,
      `ubicacion` VARCHAR(200) DEFAULT NULL,
      `notas` TEXT DEFAULT NULL,
      `estado` VARCHAR(30) NOT NULL DEFAULT 'Programado',
      `creado_en` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY (`idTurno`),
      KEY `fk_turno_brigada_idx` (`Brigada_idBrigada`),
      CONSTRAINT `fk_turno_brigada` FOREIGN KEY (`Brigada_idBrigada`)
        REFERENCES `brigada` (`idBrigada`) ON DELETE CASCADE ON UPDATE NO ACTION
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
    """
    try:
        ejecutar(sql, commit=True)
        _TABLA_TURNO_VERIFICADA = True
    except Exception as e:
        print(f"[turno] tabla ya existe o error: {e}")


# ---------- CRUD ----------

def crear_turno(brigada_id: int, fecha: str, hora_inicio: str, hora_fin: str,
                ubicacion: str = "", notas: str = "") -> int | None:
    """Inserta un turno y devuelve su ID."""
    _asegurar_tabla_turno()
    sql = """
    INSERT INTO turno (Brigada_idBrigada, fecha, hora_inicio, hora_fin, ubicacion, notas)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    try:
        lid = ejecutar(sql, (brigada_id, fecha, hora_inicio, hora_fin, ubicacion, notas), commit=True)
        return lid
    except Exception as e:
        print(f"Error creando turno: {e}")
        return None


def listar_turnos(brigada_id: int | None = None, tipo_brigada=None):
    """Lista turnos, opcionalmente filtrados por brigada_id y/o tipo_brigada."""
    _asegurar_tabla_turno()
    conditions = []
    params = []
    if brigada_id:
        conditions.append("t.Brigada_idBrigada = %s")
        params.append(brigada_id)
    if tipo_brigada:
        conditions.append("b.tipo_brigada = %s")
        params.append(tipo_brigada)
    where = ""
    if conditions:
        where = "WHERE " + " AND ".join(conditions)

    sql = f"""
    SELECT t.idTurno, t.fecha, t.hora_inicio, t.hora_fin, t.ubicacion, t.notas,
           t.estado, b.nombre_brigada, b.color_identificador,
           b.profesor_id, t.Brigada_idBrigada
    FROM turno t
    JOIN brigada b ON t.Brigada_idBrigada = b.idBrigada
    {where}
    ORDER BY t.fecha DESC, t.hora_inicio ASC
    """
    rows, _ = ejecutar(sql, tuple(params) if params else None)

    turnos = []
    for r in rows:
        turnos.append({
            "id": r[0],
            "fecha": r[1],
            "hora_inicio": r[2],
            "hora_fin": r[3],
            "ubicacion": r[4] or "",
            "notas": r[5] or "",
            "estado": r[6],
            "brigada": r[7],
            "color": r[8] or "#2563eb",
            "profesor_id": r[9],
            "brigada_id": r[10],
        })
    return turnos


def get_turno_stats(tipo_brigada=None):
    """Devuelve un dict con KPIs para la pantalla de turnos."""
    _asegurar_tabla_turno()
    stats = {
        "total_turnos": 0,
        "brigadistas_asignados": 0,
        "dias_con_turnos": 0,
    }
    try:
        if tipo_brigada:
            rows, _ = ejecutar("SELECT COUNT(*) FROM turno t JOIN brigada b ON t.Brigada_idBrigada = b.idBrigada WHERE b.tipo_brigada = %s", (tipo_brigada,))
            stats["total_turnos"] = rows[0][0] if rows else 0
            rows, _ = ejecutar("""
                SELECT COUNT(DISTINCT u.idUsuario)
                FROM usuario u
                JOIN turno t ON u.Brigada_idBrigada = t.Brigada_idBrigada
                JOIN brigada b ON t.Brigada_idBrigada = b.idBrigada
                WHERE b.tipo_brigada = %s
            """, (tipo_brigada,))
            stats["brigadistas_asignados"] = rows[0][0] if rows else 0
            rows, _ = ejecutar("SELECT COUNT(DISTINCT t.fecha) FROM turno t JOIN brigada b ON t.Brigada_idBrigada = b.idBrigada WHERE b.tipo_brigada = %s", (tipo_brigada,))
            stats["dias_con_turnos"] = rows[0][0] if rows else 0
        else:
            rows, _ = ejecutar("SELECT COUNT(*) FROM turno")
            stats["total_turnos"] = rows[0][0] if rows else 0
            rows, _ = ejecutar("""
                SELECT COUNT(DISTINCT u.idUsuario)
                FROM usuario u
                JOIN turno t ON u.Brigada_idBrigada = t.Brigada_idBrigada
            """)
            stats["brigadistas_asignados"] = rows[0][0] if rows else 0
            rows, _ = ejecutar("SELECT COUNT(DISTINCT fecha) FROM turno")
            stats["dias_con_turnos"] = rows[0][0] if rows else 0
    except Exception as e:
        print(f"Error stats turno: {e}")
    return stats


def eliminar_turno(turno_id: int) -> bool:
    """Elimina un turno por ID."""
    try:
        ejecutar("DELETE FROM turno WHERE idTurno = %s", (turno_id,), commit=True)
        return True
    except Exception as e:
        print(f"Error eliminando turno: {e}")
        return False


def actualizar_turno(turno_id: int, fecha: str, hora_inicio: str, hora_fin: str,
                     ubicacion: str = "", notas: str = "", estado: str = "Programado") -> bool:
    """Actualiza un turno existente."""
    sql = """
    UPDATE turno
    SET fecha = %s, hora_inicio = %s, hora_fin = %s,
        ubicacion = %s, notas = %s, estado = %s
    WHERE idTurno = %s
    """
    try:
        afectadas = ejecutar_modificar(sql, (fecha, hora_inicio, hora_fin, ubicacion, notas, estado, turno_id))
        return afectadas > 0
    except Exception as e:
        print(f"Error actualizando turno: {e}")
        return False
