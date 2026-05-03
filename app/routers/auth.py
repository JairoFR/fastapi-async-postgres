from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.seguridad import hashear_password, verificar_password, crear_token
from app.models.usuario import Usuario, UsuarioCreate, UsuarioResponse, Token

router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"],
)

@router.post("/registro", response_model=UsuarioResponse, status_code=201)
async def registrar_usuario(
    usuario: UsuarioCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Registra un nuevo usuario en PostgreSQL.
    Verifica que el email no exista antes de crear.
    La contraseña se hashea antes de guardar.
    """
    # Verificar si email ya existe en BD
    resultado = await db.execute(
        select(Usuario).where(Usuario.email == usuario.email)
    )
    existe = resultado.scalar_one_or_none()

    if existe:
        raise HTTPException(
            status_code=400,
            detail="Email ya registrado"
        )

    # Crear nuevo usuario con password hasheado
    nuevo_usuario = Usuario(
        email=usuario.email,
        nombre=usuario.nombre,
        password_hash=hashear_password(usuario.password)
    )

    # Guardar en PostgreSQL
    db.add(nuevo_usuario)
    await db.flush()  # obtiene el id generado
    await db.refresh(nuevo_usuario)  # recarga desde BD

    return nuevo_usuario

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    Hace login y devuelve JWT.
    Busca el usuario en PostgreSQL y verifica la contraseña.
    """
    # Buscar usuario por email en BD
    resultado = await db.execute(
        select(Usuario).where(Usuario.email == form_data.username)
    )
    usuario = resultado.scalar_one_or_none()

    # Verificar credenciales
    if not usuario or not verificar_password(
        form_data.password,
        usuario.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Crear JWT con email y rol
    token = crear_token(data={
        "sub": usuario.email,
        "rol": usuario.rol
    })

    return {"access_token": token, "token_type": "bearer"}