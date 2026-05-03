from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ItemBase(BaseModel):
    """
    Modelo base con campos comunes.
    Todos los modelos heredan de aquí.
    Reemplaza 'Item' con tu entidad (Factura, Usuario, Producto, etc.)
    """
    nombre: str
    descripcion: Optional[str] = None  # campo opcional — puede ser None
    activo: bool = True                # valor por defecto True

class ItemCreate(ItemBase):
    """
    Modelo para CREAR un item.
    Hereda todos los campos de ItemBase.
    Aquí agregas campos que solo se usan al crear.
    """
    pass  # por ahora igual que Base

class ItemUpdate(BaseModel):
    """
    Modelo para ACTUALIZAR un item.
    Todos los campos son opcionales — solo actualizas lo que llega.
    No hereda de ItemBase porque aquí TODO es opcional.
    """
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    activo: Optional[bool] = None

class ItemResponse(ItemBase):
    """
    Modelo de RESPUESTA — lo que devuelve la API al cliente.
    Hereda de ItemBase y agrega campos generados automáticamente.
    El cliente nunca envía id ni creado_en — los genera el servidor.
    """
    id: int                              # generado por BD o código
    creado_en: datetime = datetime.now() # timestamp automático

    # ConfigDict reemplaza class Config en Pydantic V2
    # from_attributes=True permite crear desde objetos SQLAlchemy
    model_config = ConfigDict(from_attributes=True)