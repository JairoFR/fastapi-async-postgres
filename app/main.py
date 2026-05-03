from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.routers import auth, tareas
from app.core.config import get_settings
from app.core.database import engine, Base
import logging

logger = logging.getLogger(__name__)
settings = get_settings()

# ── Lifespan ──────────────────────────────────────────
# Se ejecuta al arrancar y apagar la aplicación
# Crea las tablas en PostgreSQL automáticamente
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Al arrancar — crea tablas si no existen
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Al apagar — cierra conexiones
    await engine.dispose()

# Crea la aplicación con lifespan
app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description=settings.description,
    lifespan=lifespan,
)

# ── Manejo global de errores ──────────────────────────
@app.exception_handler(Exception)
async def error_global(request: Request, exc: Exception):
    logger.error(
        f"Error en {request.method} {request.url}: {exc}",
        exc_info=True
    )
    return JSONResponse(
        status_code=500,
        content={
            "error": "Error interno del servidor",
            "detalle": str(exc)
        }
    )

# ── Healthcheck ───────────────────────────────────────
@app.get("/health", tags=["Sistema"])
def health():
    return {
        "estado": "ok",
        "version": settings.version,
        "app": settings.app_name
    }

# ── Registrar routers ─────────────────────────────────
app.include_router(auth.router)
app.include_router(tareas.router)