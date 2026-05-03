from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.core.config import get_settings

settings = get_settings()

# ── Motor de base de datos ────────────────────────────
# create_async_engine = versión async de SQLAlchemy
# echo=True muestra las queries SQL en consola
# útil para debugging — False en producción
engine = create_async_engine(
    settings.database_url,
    echo=True,
)

# ── Sesión de base de datos ───────────────────────────
# AsyncSession = sesión async para hacer queries
# autocommit=False = tú controlas las transacciones
# autoflush=False = tú controlas cuándo se envían los cambios
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
)

# ── Base para los modelos ─────────────────────────────
# Todos los modelos SQLAlchemy heredan de Base
# Base mapea las clases Python a tablas en PostgreSQL
class Base(DeclarativeBase):
    pass

# ── Dependencia para los endpoints ────────────────────
# Se inyecta con Depends(get_db) en los routers
# Abre sesión → endpoint la usa → cierra sesión
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()