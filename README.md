# INVENTARIO-REY

Sistema web de gestion de inventario para El Rey de los Zapatos.

## Estado

Proyecto en fase de diseno y preparacion inicial.

Completado:

- Documentacion base del sistema.
- Integracion de GitHub.
- Integracion de Vercel.
- Conexion probada con Neon PostgreSQL.
- Conexion probada con Cloudinary.
- Diseno definitivo de base de datos del modulo de calzado.
- Estructura inicial del repositorio.

Siguiente objetivo:

- Implementar modelos SQLAlchemy y primera migracion Alembic del modulo de calzado.

## Backend local

Instalar dependencias:

```powershell
python -m pip install -r requirements.txt
```

Ejecutar API local:

```powershell
python -m uvicorn backend.app.main:app --reload
```

Endpoints base:

- `GET /`
- `GET /api/v1/health`
- `GET /api/v1/health/database`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/logout`
- `GET /api/v1/auth/me`

Verificar Alembic:

```powershell
python -m alembic current
```

Aplicar migraciones:

```powershell
python -m alembic upgrade head
```

Ejecutar seeds iniciales:

```powershell
python -m backend.app.database.seed
```

Autenticacion:

- El login usa `username` y contrasena.
- El token JWT dura 8 horas.
- Logout revoca el token usando `jti`.
- Las rutas protegidas rechazan tokens revocados.

## Documentacion

La documentacion principal esta en [docs/README.md](docs/README.md).

El diseno definitivo de base de datos esta en [docs/08-diseno-base-datos.md](docs/08-diseno-base-datos.md).

## Seguridad

Los archivos `.env` reales no deben subirse al repositorio. Usar `.env.example` como referencia.
