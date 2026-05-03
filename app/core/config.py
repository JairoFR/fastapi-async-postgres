from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    """
    Configuración central de la aplicación.
    Lee automáticamente desde el archivo .env
    """
    model_config = ConfigDict(env_file=".env")

    # Datos básicos de la API
    app_name: str = "FastAPI Async PostgreSQL"
    version: str = "1.0.0"
    description: str = "API con PostgreSQL async y SQLAlchemy"
    debug: bool = False

    # Base de datos
    # postgresql+asyncpg = driver async para PostgreSQL
    database_url: str = "postgresql+asyncpg://fastapi_user:fastapi123@localhost/fastapi_db"

    # JWT
    secret_key: str = "clave-secreta-cambiar-en-produccion"
    access_token_expire_minutes: int = 30

@lru_cache()
def get_settings() -> Settings:
    return Settings()