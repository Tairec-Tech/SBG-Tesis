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


def crear_brigada(nombre_brigada: str, area_accion: str, institucion_id: int) -> int:
    """Inserta una brigada y retorna idBrigada."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO Brigada (nombre_brigada, area_accion, Institucion_Educativa_idInstitucion)
            VALUES (%s, %s, %s)
            """,
            (nombre_brigada, area_accion, institucion_id),
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def crear_usuario(nombre: str, apellido: str, email: str, contrasena_plana: str, rol: str, brigada_id: int) -> int:
    """Inserta un usuario (contraseña se hashea). Retorna idUsuario."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO Usuario (nombre, apellido, email, contrasena, rol, Brigada_idBrigada)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (nombre, apellido, email.strip().lower(), hash_password(contrasena_plana), rol, brigada_id),
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def email_ya_existe(email: str) -> bool:
    """True si ya existe un usuario con ese email."""
    return buscar_usuario_por_email(email) is not None


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
