from fastapi import APIRouter, HTTPException
from typing import List
from app.models.item import ItemCreate, ItemUpdate, ItemResponse
from datetime import datetime

# Router genérico — reemplaza 'items' con tu entidad
# prefix: todas las rutas empiezan con /items
# tags: agrupa en Swagger
router = APIRouter(
    prefix="/items",
    tags=["Items"],
)

# Base de datos en memoria
# reemplazar con PostgreSQL en proyectos reales
items_db: List[dict] = []
contador_id: int = 0

@router.get("/", response_model=List[ItemResponse])
def obtener_items():
    """Retorna todos los items"""
    return items_db

@router.post("/", response_model=ItemResponse, status_code=201)
def crear_item(item: ItemCreate):
    """Crea un nuevo item"""
    global contador_id
    contador_id += 1
    nuevo = {
        **item.model_dump(),
        "id": contador_id,
        "creado_en": datetime.now()
    }
    items_db.append(nuevo)
    return nuevo

@router.get("/{id}", response_model=ItemResponse)
def obtener_item(id: int):
    """Busca un item por id"""
    for item in items_db:
        if item["id"] == id:
            return item
    raise HTTPException(
        status_code=404,
        detail=f"Item {id} no encontrado"
    )

@router.put("/{id}", response_model=ItemResponse)
def actualizar_item(id: int, datos: ItemUpdate):
    """Actualiza un item existente"""
    for item in items_db:
        if item["id"] == id:
            actualizacion = datos.model_dump(exclude_none=True)
            item.update(actualizacion)
            return item
    raise HTTPException(
        status_code=404,
        detail=f"Item {id} no encontrado"
    )

@router.delete("/{id}")
def eliminar_item(id: int):
    """Elimina un item"""
    for i, item in enumerate(items_db):
        if item["id"] == id:
            items_db.pop(i)
            return {"mensaje": f"Item {id} eliminado "}
    raise HTTPException(
        status_code=404,
        detail=f"Item {id} no encontrado"
    )