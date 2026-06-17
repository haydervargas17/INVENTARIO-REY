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
