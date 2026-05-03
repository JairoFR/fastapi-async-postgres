from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from app.core.database import Base

class Usuario(Base):
    """
    Tabla 'usuarios' en PostgreSQL.
    Cada atributo = columna en la tabla.
    """
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    nombre = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    activo = Column(Boolean, default=True)
    rol = Column(String, default="user")
    creado_en = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    tareas = relationship("Tarea", back_populates="usuario")


class UsuarioCreate(BaseModel):
    """Para registrar un usuario"""
    email: EmailStr
    nombre: str
    password: str

class UsuarioResponse(BaseModel):
    """Lo que devuelve la API — sin password"""
    id: int
    email: str
    nombre: str
    activo: bool
    rol: str

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    """Respuesta del login"""
    access_token: str
    token_type: str = "bearer"