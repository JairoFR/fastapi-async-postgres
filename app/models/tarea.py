from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from pydantic import BaseModel, ConfigDict
from app.core.database import Base

class Tarea(Base):
    """
    Tabla 'tareas' en PostgreSQL.
    Cada tarea pertenece a un usuario — relación FK.
    """
    __tablename__ = "tareas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    descripcion = Column(Text, nullable=True)  # Text = texto largo
    completada = Column(Boolean, default=False)
    creado_en = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    # Foreign Key — conecta cada tarea con su usuario
    # ondelete="CASCADE" = si se borra el usuario
    # se borran todas sus tareas automáticamente
    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id", ondelete="CASCADE"),
        nullable=False
    )

    # Relación inversa con Usuario
    usuario = relationship("Usuario", back_populates="tareas")


# ── Schemas Pydantic ──────────────────────────────────

class TareaCreate(BaseModel):
    """Para crear una tarea"""
    titulo: str
    descripcion: Optional[str] = None

class TareaUpdate(BaseModel):
    """Para actualizar — todo opcional"""
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    completada: Optional[bool] = None

class TareaResponse(BaseModel):
    """Lo que devuelve la API"""
    id: int
    titulo: str
    descripcion: Optional[str] = None
    completada: bool
    usuario_id: int
    creado_en: datetime

    model_config = ConfigDict(from_attributes=True)