"""
Autenticación: hash de contraseñas y verificación.
"""
import hashlib


def hash_password(plain: str) -> str:
    """Devuelve el hash SHA-256 de la contraseña en hexadecimal."""
    return hashlib.sha256(plain.encode("utf-8")).hexdigest()


def verificar_password(plain: str, stored_hash: str) -> bool:
    """Comprueba si la contraseña en texto plano coincide con el hash almacenado."""
    return stored_hash == hash_password(plain)
