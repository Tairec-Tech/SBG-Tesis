"""
CRUD de Usuario e Institucion para login y registro.
"""
from database.connection import get_connection
from database.auth import hash_password, verificar_password


def buscar_usuario_por_email(email: str):
    """
    Busca un usuario por email. Retorna el diccionario del usuario o None.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT idUsuario, nombre, apellido, email, contrasena, rol, Brigada_idBrigada FROM Usuario WHERE email = %s",
            (email.strip().lower(),),
        )
        return cursor.fetchone()
    finally:
        conn.close()


def verificar_login(email: str, password: str):
    """
    Verifica credenciales. Retorna el usuario (dict) si son correctas, None si no.
    """
    usuario = buscar_usuario_por_email(email)
    if not usuario or not usuario.get("contrasena"):
        return None
    if not verificar_password(password, usuario["contrasena"]):
        return None
    return usuario


def crear_institucion(nombre: str, direccion: str, telefono: str) -> int:
    """Inserta una institución y retorna idInstitucion."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Institucion_Educativa (nombre_institucion, direccion, telefono) VALUES (%s, %s, %s)",
            (nombre, direccion, telefono),
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def listar_instituciones():
    """Lista todas las instituciones. Retorna lista de dict: idInstitucion, nombre_institucion, direccion, telefono, logo_ruta."""
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT idInstitucion, nombre_institucion, direccion, telefono, logo_ruta FROM Institucion_Educativa ORDER BY nombre_institucion"
            )
        except Exception:
            cursor.execute(
                "SELECT idInstitucion, nombre_institucion, direccion, telefono FROM Institucion_Educativa ORDER BY nombre_institucion"
            )
        rows = cursor.fetchall()
        for r in rows:
            r.setdefault("logo_ruta", None)
        return rows
    finally:
        conn.close()


def obtener_institucion_por_id(id_institucion: int):
    """Obtiene una institución por ID. Retorna dict con nombre_institucion, logo_ruta, etc."""
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT idInstitucion, nombre_institucion, direccion, telefono, logo_ruta FROM Institucion_Educativa WHERE idInstitucion = %s",
                (id_institucion,),
            )
        except Exception:
            cursor.execute(
                "SELECT idInstitucion, nombre_institucion, direccion, telefono FROM Institucion_Educativa WHERE idInstitucion = %s",
                (id_institucion,),
            )
        row = cursor.fetchone()
        if row:
            row.setdefault("logo_ruta", None)
        return row
    finally:
        conn.close()


def obtener_institucion_por_usuario(id_usuario: int):
    """Obtiene la institución del usuario (vía su brigada). Retorna dict con nombre_institucion, logo_ruta o None."""
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT i.idInstitucion, i.nombre_institucion, i.logo_ruta
                FROM Usuario u
                INNER JOIN Brigada b ON b.idBrigada = u.Brigada_idBrigada
                INNER JOIN Institucion_Educativa i ON i.idInstitucion = b.Institucion_Educativa_idInstitucion
                WHERE u.idUsuario = %s
                """,
                (id_usuario,),
            )
        except Exception:
            cursor.execute(
                """
                SELECT i.idInstitucion, i.nombre_institucion
                FROM Usuario u
                INNER JOIN Brigada b ON b.idBrigada = u.Brigada_idBrigada
                INNER JOIN Institucion_Educativa i ON i.idInstitucion = b.Institucion_Educativa_idInstitucion
                WHERE u.idUsuario = %s
                """,
                (id_usuario,),
            )
        row = cursor.fetchone()
        if row:
            row.setdefault("logo_ruta", None)
        return row
    finally:
        conn.close()


def actualizar_logo_institucion(id_institucion: int, logo_ruta: str):
    """Actualiza la ruta del logo de una institución. Requiere columna logo_ruta (migración)."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE Institucion_Educativa SET logo_ruta = %s WHERE idInstitucion = %s", (logo_ruta, id_institucion))
        conn.commit()
    finally:
        conn.close()


def listar_brigadas_por_institucion(institucion_id: int):
    """Lista brigadas de una institución. Retorna lista de dict con idBrigada, nombre_brigada, etc."""
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT idBrigada, nombre_brigada, area_accion, Institucion_Educativa_idInstitucion
            FROM Brigada WHERE Institucion_Educativa_idInstitucion = %s ORDER BY idBrigada
            """,
            (institucion_id,),
        )
        return cursor.fetchall()
    finally:
        conn.close()


def crear_brigada(nombre_brigada: str, area_accion: str, institucion_id: int, profesor_id: int = None) -> int:
    """
    Inserta una brigada y retorna idBrigada.
    profesor_id: ID del profesor que la creó/administra (opcional, para admins que crean para un profesor).
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO Brigada (nombre_brigada, area_accion, Institucion_Educativa_idInstitucion, profesor_id)
            VALUES (%s, %s, %s, %s)
            """,
            (nombre_brigada, area_accion, institucion_id, profesor_id),
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def crear_usuario(nombre: str, apellido: str, email: str, contrasena_plana: str, rol: str, brigada_id: int, usuario: str = None) -> int:
    """Inserta un usuario (contraseña se hashea). usuario = nombre de usuario para login. Retorna idUsuario."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        usuario_val = (usuario or "").strip() or None
        if usuario_val:
            usuario_val = usuario_val.lower()
        try:
            cursor.execute(
                """
                INSERT INTO Usuario (nombre, apellido, email, usuario, contrasena, rol, Brigada_idBrigada)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (nombre, apellido, email.strip().lower(), usuario_val, hash_password(contrasena_plana), rol, brigada_id),
            )
        except Exception as e:
            if "usuario" in str(e).lower() and "unknown column" in str(e).lower():
                cursor.execute(
                    """
                    INSERT INTO Usuario (nombre, apellido, email, contrasena, rol, Brigada_idBrigada)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (nombre, apellido, email.strip().lower(), hash_password(contrasena_plana), rol, brigada_id),
                )
            else:
                raise
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def email_ya_existe(email: str) -> bool:
    """True si ya existe un usuario con ese email."""
    return buscar_usuario_por_email(email) is not None


def usuario_ya_existe(usuario: str) -> bool:
    """True si ya existe un usuario con ese nombre de usuario."""
    if not usuario or not (usuario or "").strip():
        return False
    conn = get_connection()
    try:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT 1 FROM Usuario WHERE usuario = %s", (usuario.strip().lower(),))
            return cursor.fetchone() is not None
        except Exception as e:
            if "usuario" in str(e).lower() and "unknown column" in str(e).lower():
                return False
            raise
    finally:
        conn.close()


def verificar_login_por_usuario_e_institucion(institucion_id: int, usuario: str, password: str, es_profesor: bool = None):
    """
    Verifica credenciales por institución + usuario + contraseña.
    usuario: nombre de usuario o email.
    es_profesor: True = solo rol Profesor, False = solo Directivo/Coordinador, None = cualquier rol.
    Retorna el usuario (dict) o None.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        usuario_str = (usuario or "").strip().lower()
        try:
            cursor.execute(
                """
                SELECT u.idUsuario, u.nombre, u.apellido, u.email, u.usuario, u.contrasena, u.rol, u.Brigada_idBrigada
                FROM Usuario u
                INNER JOIN Brigada b ON b.idBrigada = u.Brigada_idBrigada
                WHERE b.Institucion_Educativa_idInstitucion = %s
                  AND (u.usuario = %s OR u.email = %s)
                LIMIT 1
                """,
                (institucion_id, usuario_str, usuario_str),
            )
        except Exception as e:
            if "usuario" in str(e).lower() and "unknown column" in str(e).lower():
                cursor.execute(
                    """
                    SELECT u.idUsuario, u.nombre, u.apellido, u.email, u.contrasena, u.rol, u.Brigada_idBrigada
                    FROM Usuario u
                    INNER JOIN Brigada b ON b.idBrigada = u.Brigada_idBrigada
                    WHERE b.Institucion_Educativa_idInstitucion = %s AND u.email = %s
                    LIMIT 1
                    """,
                    (institucion_id, usuario_str),
                )
            else:
                raise
        row = cursor.fetchone()
        if not row or not row.get("contrasena"):
            return None
        if not verificar_password(password, row["contrasena"]):
            return None
        if es_profesor is True and row.get("rol") != "Profesor":
            return None
        if es_profesor is False and row.get("rol") not in ("Directivo", "Coordinador"):
            return None
        row.setdefault("usuario", None)
        return row
    finally:
        conn.close()


def listar_brigadistas():
    """
    Lista todos los usuarios (brigadistas) con el nombre de su brigada.
    Retorna lista de dict: idUsuario, nombre, apellido, email, rol, Brigada_idBrigada, nombre_brigada.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT u.idUsuario, u.nombre, u.apellido, u.email, u.rol, u.Brigada_idBrigada,
                   b.nombre_brigada
            FROM Usuario u
            LEFT JOIN Brigada b ON b.idBrigada = u.Brigada_idBrigada
            ORDER BY u.nombre, u.apellido
            """
        )
        return cursor.fetchall()
    finally:
        conn.close()


def obtener_usuario(id_usuario: int):
    """Obtiene un usuario por id (sin contraseña en uso). Retorna dict o None."""
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT idUsuario, nombre, apellido, email, rol, Brigada_idBrigada FROM Usuario WHERE idUsuario = %s",
            (id_usuario,),
        )
        return cursor.fetchone()
    finally:
        conn.close()


def actualizar_usuario(id_usuario: int, nombre: str, apellido: str, email: str, rol: str, brigada_id: int):
    """Actualiza nombre, apellido, email, rol y brigada de un usuario. No modifica contraseña."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE Usuario SET nombre = %s, apellido = %s, email = %s, rol = %s, Brigada_idBrigada = %s
            WHERE idUsuario = %s
            """,
            (nombre, apellido, email.strip().lower(), rol, brigada_id, id_usuario),
        )
        conn.commit()
    finally:
        conn.close()


def eliminar_usuario(id_usuario: int) -> str | None:
    """
    Elimina un usuario. Retorna None si OK, o mensaje de error si falla (p. ej. reportes asociados).
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Usuario WHERE idUsuario = %s", (id_usuario,))
        conn.commit()
        return None
    except Exception as e:
        return str(e)
    finally:
        conn.close()


# =====================================================
# ROLES Y PERMISOS
# =====================================================
ROLES_ADMIN = ("Directivo", "Coordinador")
ROLES_PROFESOR = ("Profesor",)
ROLES_BRIGADISTAS = ("Brigadista Jefe", "Subjefe", "Brigadista")


def es_admin(rol: str) -> bool:
    """True si el rol es Directivo o Coordinador."""
    return rol in ROLES_ADMIN


def es_profesor(rol: str) -> bool:
    """True si el rol es Profesor."""
    return rol in ROLES_PROFESOR


def es_brigadista(rol: str) -> bool:
    """True si el rol es Brigadista Jefe, Subjefe o Brigadista."""
    return rol in ROLES_BRIGADISTAS


def listar_profesores_institucion(institucion_id: int):
    """
    Lista todos los usuarios con rol 'Profesor' de una institución.
    Retorna lista de dict: idUsuario, nombre, apellido, email.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT DISTINCT u.idUsuario, u.nombre, u.apellido, u.email
            FROM Usuario u
            JOIN Brigada b ON b.idBrigada = u.Brigada_idBrigada
            WHERE b.Institucion_Educativa_idInstitucion = %s
              AND u.rol = 'Profesor'
            ORDER BY u.nombre, u.apellido
            """,
            (institucion_id,),
        )
        return cursor.fetchall()
    finally:
        conn.close()


def listar_brigadas_profesor(profesor_id: int):
    """
    Lista las brigadas creadas por un profesor específico.
    Retorna lista de dict con info de brigadas.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT b.idBrigada, b.nombre_brigada, b.area_accion, b.fecha_creacion, b.profesor_id, b.subjefe_id
            FROM Brigada b
            WHERE b.profesor_id = %s
            ORDER BY b.fecha_creacion DESC
            """,
            (profesor_id,),
        )
        return cursor.fetchall()
    finally:
        conn.close()


def listar_brigadas_otros_profesores(profesor_id: int, institucion_id: int):
    """
    Lista brigadas de otros profesores de la misma institución.
    Retorna lista de dict con info de brigadas.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT b.idBrigada, b.nombre_brigada, b.area_accion, b.fecha_creacion, b.profesor_id, b.subjefe_id,
                   u.nombre AS profesor_nombre, u.apellido AS profesor_apellido
            FROM Brigada b
            LEFT JOIN Usuario u ON u.idUsuario = b.profesor_id
            WHERE b.Institucion_Educativa_idInstitucion = %s
              AND b.profesor_id != %s
              AND b.profesor_id IS NOT NULL
            ORDER BY b.fecha_creacion DESC
            """,
            (institucion_id, profesor_id),
        )
        return cursor.fetchall()
    finally:
        conn.close()


def asignar_subjefe_brigada(brigada_id: int, subjefe_id: int):
    """Asigna un brigadista como subjefe de una brigada."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Brigada SET subjefe_id = %s WHERE idBrigada = %s",
            (subjefe_id, brigada_id),
        )
        conn.commit()
    finally:
        conn.close()


def obtener_brigada(brigada_id: int):
    """Obtiene una brigada por ID. Retorna dict o None."""
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT b.idBrigada, b.nombre_brigada, b.area_accion, b.fecha_creacion,
                   b.Institucion_Educativa_idInstitucion, b.profesor_id, b.subjefe_id
            FROM Brigada b
            WHERE b.idBrigada = %s
            """,
            (brigada_id,),
        )
        return cursor.fetchone()
    finally:
        conn.close()


def listar_brigadistas_brigada(brigada_id: int):
    """
    Lista todos los brigadistas de una brigada específica.
    Retorna lista de dict: idUsuario, nombre, apellido, email, rol.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT u.idUsuario, u.nombre, u.apellido, u.email, u.rol
            FROM Usuario u
            WHERE u.Brigada_idBrigada = %s
              AND u.rol IN ('Brigadista Jefe', 'Subjefe', 'Brigadista')
            ORDER BY
                CASE u.rol
                    WHEN 'Brigadista Jefe' THEN 1
                    WHEN 'Subjefe' THEN 2
                    WHEN 'Brigadista' THEN 3
                END,
                u.nombre, u.apellido
            """,
            (brigada_id,),
        )
        return cursor.fetchall()
    finally:
        conn.close()


def listar_brigadistas_visibles(brigada_id: int):
    """
    Lista brigadistas visibles en el listado (Jefes y Brigadistas, NO subjefes).
    Retorna lista de dict: idUsuario, nombre, apellido, email, rol.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT u.idUsuario, u.nombre, u.apellido, u.email, u.rol
            FROM Usuario u
            WHERE u.Brigada_idBrigada = %s
              AND u.rol IN ('Brigadista Jefe', 'Brigadista')
            ORDER BY
                CASE u.rol
                    WHEN 'Brigadista Jefe' THEN 1
                    WHEN 'Brigadista' THEN 2
                END,
                u.nombre, u.apellido
            """,
            (brigada_id,),
        )
        return cursor.fetchall()
    finally:
        conn.close()
