from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.routers import items
from app.core.config import get_settings
import logging

#pip install fastapi uvicorn pydantic pydantic-settings pytest httpx python-dotenv

# Logger para producción
logger = logging.getLogger(__name__)

# Carga configuración
settings = get_settings()

# Crea la aplicación
app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description=settings.description,
)

# ── Manejo global de errores ──────────────────────────
# Captura CUALQUIER error no manejado en toda la API
# Desarrollo: muestra detalle
# Producción: ocultar detalle y loguear
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
            "detalle": str(exc)  # ← quitar en producción
        }
    )

# ── Healthcheck ───────────────────────────────────────
# Endpoint que usan servidores para saber si la API está viva
# Docker, Railway, AWS lo llaman automáticamente
@app.get("/health", tags=["Sistema"])
def health():
    return {
        "estado": "ok",
        "version": settings.version,
        "app": settings.app_name
    }

# ── Registrar routers ─────────────────────────────────
# Agrega aquí tus routers según el proyecto
app.include_router(items.router)