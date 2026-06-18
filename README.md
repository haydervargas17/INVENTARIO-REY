# INVENTARIO-REY

Sistema web de gestion de inventario para El Rey de los Zapatos.

## Estado

Proyecto en desarrollo inicial del backend.

Completado:

- Documentacion base del sistema.
- Integracion de GitHub.
- Integracion de Vercel.
- Conexion probada con Neon PostgreSQL.
- Conexion probada con Cloudinary.
- Diseno definitivo de base de datos del modulo de calzado.
- Estructura inicial del repositorio.
- Modelos SQLAlchemy y migracion inicial Alembic.
- Seed inicial de colores y usuario `system_admin`.
- Autenticacion JWT con logout y revocacion de token.
- Endpoints base de catalogos, productos e inventario.
- Salidas por venta, ajustes manuales e historial de movimientos.

Siguiente objetivo:

- Implementar carga de imagenes a Cloudinary desde el backend.

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
- `GET /api/v1/catalogs/colors`
- `GET /api/v1/products`
- `POST /api/v1/products`
- `PATCH /api/v1/products/{product_id}`
- `GET /api/v1/inventory`
- `POST /api/v1/inventory/entries`
- `POST /api/v1/inventory/{inventory_item_id}/exits`
- `POST /api/v1/inventory/{inventory_item_id}/adjustments`
- `GET /api/v1/inventory/{inventory_item_id}/movements`

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

Inventario:

- La entrada de inventario crea la referencia si no existe.
- Si ya existe la misma referencia, talla, combinacion de colores y ubicacion, suma unidades.
- `color_signature` se genera automaticamente desde colores normalizados.
- Las cantidades no se editan directamente; se modifican por movimientos.
- Las salidas por venta no permiten dejar stock negativo.
- Los ajustes manuales pueden ser positivos o negativos, pero no pueden dejar stock negativo.
- El historial muestra fecha, usuario, tipo de movimiento, cantidades, precios y motivo.

## Documentacion

La documentacion principal esta en [docs/README.md](docs/README.md).

El diseno definitivo de base de datos esta en [docs/08-diseno-base-datos.md](docs/08-diseno-base-datos.md).

## Seguridad

Los archivos `.env` reales no deben subirse al repositorio. Usar `.env.example` como referencia.
