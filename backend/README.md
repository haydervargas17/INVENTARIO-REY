# Backend

API REST del sistema de inventario.

Stack previsto:

- Python 3.12.
- FastAPI.
- SQLAlchemy 2.
- Alembic.
- Pydantic.
- Passlib.
- Python-Jose.
- Cloudinary SDK.

La implementacion debe respetar las capas definidas en `docs/02-arquitectura.md`.

## Estado actual

Implementado:

- Aplicacion FastAPI base.
- Configuracion con Pydantic Settings.
- Conexion a Neon PostgreSQL con SQLAlchemy.
- Sesion de base de datos reutilizable.
- Health check de API.
- Health check de base de datos.
- Configuracion inicial de Alembic.
- Modelos SQLAlchemy iniciales del modulo de calzado.
- Migracion inicial aplicada en Neon.
- Seed modular de colores y usuario `system_admin`.
- Autenticacion JWT.
- Login, logout y `me`.
- Revocacion de token en logout.
- Entrypoints ASGI para Vercel: `app.py` y `api/index.py`.

## Ejecutar localmente

Desde la raiz del repositorio:

```powershell
python -m pip install -r requirements.txt
python -m uvicorn backend.app.main:app --reload
```

## Verificaciones

```powershell
python -m compileall app.py backend api
python -m alembic current
```

## Migraciones y seeds

```powershell
python -m alembic upgrade head
python -m backend.app.database.seed
```

El seed de `system_admin` requiere:

- `SYSTEM_ADMIN_USERNAME`
- `SYSTEM_ADMIN_PASSWORD`
- `SYSTEM_ADMIN_FULL_NAME`

## Endpoints de autenticacion

- `POST /api/v1/auth/login`
- `POST /api/v1/auth/logout`
- `GET /api/v1/auth/me`
