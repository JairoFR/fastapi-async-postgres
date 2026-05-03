# 🐘 FastAPI Async PostgreSQL

API REST async con persistencia real usando PostgreSQL y SQLAlchemy 2.0.

## 🛠️ Stack tecnológico

- **Python 3.11**
- **FastAPI** — framework para APIs REST
- **SQLAlchemy 2.0** — ORM async
- **PostgreSQL** — base de datos
- **asyncpg** — driver async para PostgreSQL
- **Pydantic v2** — validación de datos
- **python-jose** — JWT
- **passlib + bcrypt** — encriptación de contraseñas
- **Docker** — contenedorización
- **pytest** — testing

## 📁 Estructura del proyecto

```
app/
├── core/
│   ├── config.py      # configuración central
│   ├── database.py    # conexión y sesión PostgreSQL
│   └── seguridad.py   # JWT y encriptación
├── models/
│   ├── usuario.py     # modelo SQLAlchemy + schemas Pydantic
│   └── tarea.py       # modelo SQLAlchemy + schemas Pydantic
├── routers/
│   ├── auth.py        # registro y login
│   └── tareas.py      # CRUD de tareas protegido
└── main.py            # entrada principal
tests/
└── test_tareas.py
```

## 🗄️ Tablas en PostgreSQL

```
usuarios                    tareas
────────────────            ──────────────────────
id          SERIAL          id          SERIAL
email       VARCHAR         titulo      VARCHAR
nombre      VARCHAR         descripcion TEXT
password    VARCHAR         completada  BOOLEAN
activo      BOOLEAN         usuario_id  FK → usuarios
rol         VARCHAR         creado_en   TIMESTAMP
creado_en   TIMESTAMP
```

## 🚀 Cómo correr el proyecto

### 1️⃣ Clona el repositorio
```bash
git clone git@github.com:JairoFR/fastapi-async-postgres.git
cd fastapi-async-postgres
```

### 2️⃣ Crea el ambiente virtual
```bash
python3 -m venv env
source env/bin/activate
```

### 3️⃣ Instala las dependencias
```bash
pip install -r requirements.txt
```

### 4️⃣ Instala y configura PostgreSQL
```bash
sudo apt install postgresql postgresql-contrib -y
sudo service postgresql start
sudo -u postgres psql
```

```sql
CREATE DATABASE fastapi_db;
CREATE USER fastapi_user WITH PASSWORD 'fastapi123';
GRANT ALL ON SCHEMA public TO fastapi_user;
GRANT ALL PRIVILEGES ON DATABASE fastapi_db TO fastapi_user;
ALTER DATABASE fastapi_db OWNER TO fastapi_user;
\q
```

### 5️⃣ Configura las variables de entorno
```bash
cp .env.example .env
# edita .env con tus valores
```

### 6️⃣ Corre el servidor
```bash
uvicorn app.main:app --reload
```

Las tablas se crean automáticamente al arrancar. ✅

## 🐳 Con Docker

```bash
docker build -t fastapi-async-postgres .
docker run -p 8000:8000 fastapi-async-postgres
```

## 🧪 Tests

```bash
pytest tests/ -v
```

## 📡 Endpoints

| Método | Ruta | Descripción | Protegido |
|--------|------|-------------|-----------|
| GET | /health | Estado del servidor | No |
| POST | /auth/registro | Registrar usuario | No |
| POST | /auth/login | Login → JWT | No |
| GET | /tareas | Mis tareas | ✅ Token |
| POST | /tareas | Crear tarea | ✅ Token |
| GET | /tareas/{id} | Ver una tarea | ✅ Token |
| PUT | /tareas/{id} | Actualizar tarea | ✅ Token |
| DELETE | /tareas/{id} | Eliminar tarea | ✅ Token |

## 🔄 Flujo de autenticación

```
1. POST /auth/registro  → crea usuario en PostgreSQL
2. POST /auth/login     → devuelve JWT
3. Endpoints /tareas    → requieren JWT válido
4. Cada usuario ve SOLO sus propias tareas
```

## 📖 Documentación

```
http://localhost:8000/docs
```

## 📝 Variables de entorno

```
APP_NAME=FastAPI Async PostgreSQL
VERSION=1.0.0
DESCRIPTION=API con PostgreSQL async
DEBUG=False
DATABASE_URL=postgresql+asyncpg://usuario:password@localhost/nombre_db
SECRET_KEY=tu-clave-secreta
ACCESS_TOKEN_EXPIRE_MINUTES=30
```