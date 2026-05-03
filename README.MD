# ⚡ FastAPI Boilerplate

Base profesional y reutilizable para proyectos FastAPI.
Clona este repositorio como punto de partida para nuevas APIs.

## 🛠️ Stack tecnológico

- **Python 3.11**
- **FastAPI** — framework para APIs REST
- **Pydantic v2** — validación de datos
- **Docker** — contenedorización
- **Uvicorn** — servidor ASGI
- **pytest** — testing

## 📁 Estructura del proyecto

```
app/
├── core/
│   └── config.py    # configuración central con .env
├── models/
│   └── item.py      # modelos Pydantic — reemplaza con tu entidad
├── routers/
│   └── items.py     # endpoints — reemplaza con tu lógica
└── main.py          # entrada principal, manejo de errores global
tests/
└── test_health.py   # tests base
```

## 🚀 Cómo usar este boilerplate

### 1️⃣ Clona el repositorio
```bash
git clone git@github.com:JairoFR/fastapi-boilerplate.git mi-nuevo-proyecto
cd mi-nuevo-proyecto
```

### 2️⃣ Desconecta del repo original y conecta al tuyo

```bash
# 1. Elimina la historia git del boilerplate
rm -rf .git

# 2. Inicia git limpio
git init

# 3. Ve a GitHub y crea un nuevo repositorio vacío
#    sin README, sin .gitignore, sin nada
#    luego copia la URL SSH que te da GitHub y úsala aquí:
git remote add origin git@github.com:TuUsuario/mi-nuevo-proyecto.git

# 4. Verifica que quedó conectado a tu repo
git remote -v

# 5. Sube el código
git add .
git commit -m "feat: inicio del proyecto"
git branch -M main
git push -u origin main
```

### 3️⃣ Crea el ambiente virtual
```bash
python3 -m venv env
source env/bin/activate
```

### 4️⃣ Instala las dependencias
```bash
# Instala todas las librerías del proyecto
pip install -r requirements.txt

# Si agregas nuevas librerías actualiza el archivo
pip freeze > requirements.txt
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

## 🐳 Con Docker

```bash
docker build -t mi-proyecto .
docker run -p 8000:8000 mi-proyecto
```

## 🧪 Tests

```bash
# Correr todos los tests
pytest tests/ -v

# Ver cobertura
pytest tests/ -v --tb=short
```

## 📡 Endpoints base

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | /health | Estado del servidor |
| GET | /items | Listar todos |
| POST | /items | Crear nuevo |
| GET | /items/{id} | Buscar uno |
| PUT | /items/{id} | Actualizar |
| DELETE | /items/{id} | Eliminar |

## 📖 Documentación

```
http://localhost:8000/docs
```

## 🔄 Cómo adaptar a tu proyecto

```
1. Renombra app/models/item.py     → tu entidad
2. Renombra app/routers/items.py   → tu lógica
3. Actualiza app/main.py           → registra tu router
4. Agrega variables en .env        → tu configuración
5. Actualiza requirements.txt      → tus dependencias
```

## 📝 Variables de entorno

Copia `.env.example` a `.env` y configura:

```
APP_NAME=nombre-de-tu-app
VERSION=1.0.0
DESCRIPTION=descripcion-de-tu-app
DEBUG=False
```
