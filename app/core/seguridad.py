from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import get_settings

settings = get_settings()

# ── Encriptación de contraseñas ───────────────────────
# bcrypt es el algoritmo más seguro para contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashear_password(password: str) -> str:
    """
    Convierte contraseña plana a hash seguro.
    "123456" → "$2b$12$xyz..." (irreversible)
    """
    return pwd_context.hash(password)

def verificar_password(password_plano: str, password_hash: str) -> bool:
    """
    Compara contraseña plana con hash guardado.
    Retorna True si coinciden.
    """
    return pwd_context.verify(password_plano, password_hash)

def crear_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Genera un JWT firmado con SECRET_KEY.
    Expira después de ACCESS_TOKEN_EXPIRE_MINUTES.
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes
        )

    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, settings.secret_key, algorithm="HS256")
    return token

def verificar_token(token: str) -> Optional[dict]:
    """
    Verifica y decodifica un JWT.
    Retorna payload si es válido.
    Retorna None si es inválido o expiró.
    """
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=["HS256"]
        )
        return payload
    except JWTError:
        return None