"""
Autenticación: hash de contraseñas y verificación.

Usa PBKDF2-HMAC-SHA256 con salt aleatorio (100 000 iteraciones).
Soporta hashes legacy SHA-256 (sin salt) para compatibilidad con usuarios existentes.
"""
import hashlib
import os

PBKDF2_ITERATIONS = 100_000
SALT_LENGTH = 16  # bytes


def hash_password(plain: str) -> str:
    """Genera hash seguro: salt aleatorio + PBKDF2-HMAC-SHA256.
    Retorna 'salt_hex:hash_hex'."""
    salt = os.urandom(SALT_LENGTH)
    dk = hashlib.pbkdf2_hmac("sha256", plain.encode("utf-8"), salt, PBKDF2_ITERATIONS)
    return f"{salt.hex()}:{dk.hex()}"


def _es_hash_legacy(stored_hash: str) -> bool:
    """True si el hash es SHA-256 viejo (64 chars hex, sin ':')."""
    return ":" not in stored_hash and len(stored_hash) == 64


def verificar_password(plain: str, stored_hash: str) -> bool:
    """Comprueba la contraseña contra el hash almacenado.
    Soporta formato nuevo (salt:hash) y legacy (SHA-256 puro)."""
    if _es_hash_legacy(stored_hash):
        return stored_hash == hashlib.sha256(plain.encode("utf-8")).hexdigest()
    # Formato nuevo: salt_hex:hash_hex
    try:
        salt_hex, hash_hex = stored_hash.split(":", 1)
        salt = bytes.fromhex(salt_hex)
        dk = hashlib.pbkdf2_hmac("sha256", plain.encode("utf-8"), salt, PBKDF2_ITERATIONS)
        return dk.hex() == hash_hex
    except (ValueError, TypeError):
        return False
