from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.core.database import get_db
from app.core.seguridad import verificar_token
from app.models.usuario import Usuario
from app.models.tarea import Tarea, TareaCreate, TareaUpdate, TareaResponse

router = APIRouter(
    prefix="/tareas",
    tags=["Tareas"],
)

# Extrae el token del header Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_usuario_actual(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    """
    Dependencia que verifica el JWT y retorna el usuario.
    Se inyecta en todos los endpoints protegidos.
    """
    payload = verificar_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Buscar usuario en BD
    resultado = await db.execute(
        select(Usuario).where(Usuario.email == payload.get("sub"))
    )
    usuario = resultado.scalar_one_or_none()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return usuario

@router.get("/", response_model=List[TareaResponse])
async def obtener_tareas(
    usuario: Usuario = Depends(get_usuario_actual),
    db: AsyncSession = Depends(get_db)
):
    """
    Retorna SOLO las tareas del usuario autenticado.
    Cada usuario ve únicamente sus propias tareas.
    """
    resultado = await db.execute(
        select(Tarea).where(Tarea.usuario_id == usuario.id)
    )
    return resultado.scalars().all()

@router.post("/", response_model=TareaResponse, status_code=201)
async def crear_tarea(
    tarea: TareaCreate,
    usuario: Usuario = Depends(get_usuario_actual),
    db: AsyncSession = Depends(get_db)
):
    """
    Crea una nueva tarea para el usuario autenticado.
    El usuario_id se asigna automáticamente del token.
    """
    nueva_tarea = Tarea(
        titulo=tarea.titulo,
        descripcion=tarea.descripcion,
        usuario_id=usuario.id  # ← del token, no del body
    )
    db.add(nueva_tarea)
    await db.flush()
    await db.refresh(nueva_tarea)
    return nueva_tarea

@router.get("/{id}", response_model=TareaResponse)
async def obtener_tarea(
    id: int,
    usuario: Usuario = Depends(get_usuario_actual),
    db: AsyncSession = Depends(get_db)
):
    """
    Busca una tarea por id.
    Verifica que pertenezca al usuario autenticado.
    """
    resultado = await db.execute(
        select(Tarea).where(
            Tarea.id == id,
            Tarea.usuario_id == usuario.id  # ← seguridad
        )
    )
    tarea = resultado.scalar_one_or_none()

    if not tarea:
        raise HTTPException(
            status_code=404,
            detail=f"Tarea {id} no encontrada"
        )
    return tarea

@router.put("/{id}", response_model=TareaResponse)
async def actualizar_tarea(
    id: int,
    datos: TareaUpdate,
    usuario: Usuario = Depends(get_usuario_actual),
    db: AsyncSession = Depends(get_db)
):
    """
    Actualiza una tarea existente.
    Solo actualiza los campos que llegaron.
    """
    resultado = await db.execute(
        select(Tarea).where(
            Tarea.id == id,
            Tarea.usuario_id == usuario.id
        )
    )
    tarea = resultado.scalar_one_or_none()

    if not tarea:
        raise HTTPException(
            status_code=404,
            detail=f"Tarea {id} no encontrada"
        )

    # Actualiza solo campos que llegaron
    actualizacion = datos.model_dump(exclude_none=True)
    for campo, valor in actualizacion.items():
        setattr(tarea, campo, valor)

    await db.flush()
    await db.refresh(tarea)
    return tarea

@router.delete("/{id}")
async def eliminar_tarea(
    id: int,
    usuario: Usuario = Depends(get_usuario_actual),
    db: AsyncSession = Depends(get_db)
):
    """
    Elimina una tarea del usuario autenticado.
    """
    resultado = await db.execute(
        select(Tarea).where(
            Tarea.id == id,
            Tarea.usuario_id == usuario.id
        )
    )
    tarea = resultado.scalar_one_or_none()

    if not tarea:
        raise HTTPException(
            status_code=404,
            detail=f"Tarea {id} no encontrada"
        )

    await db.delete(tarea)
    return {"mensaje": f"Tarea {id} eliminada "}