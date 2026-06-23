# INVENTARIO-REY

Sistema web de gestion de inventario para El Rey de los Zapatos.

## Estado

Proyecto en desarrollo inicial full-stack.

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
- Carga de imagenes de productos a Cloudinary desde el backend.
- Frontend inicial en React, TypeScript, Vite y TailwindCSS.
- Login conectado a la API.
- Panel de inventario con referencias, entradas, salidas, ajustes e historial.

Siguiente objetivo:

- Configurar despliegue conjunto frontend + backend en Vercel y ampliar filtros de inventario.

## Backend local

Instalar dependencias:

```powershell
python -m pip install -r requirements.txt
```

Ejecutar API local:

```powershell
python -m uvicorn backend.app.main:app --reload
```

## Frontend local

Instalar dependencias:

```powershell
cd frontend
npm install
```

Ejecutar interfaz local:

```powershell
npm run dev
```

El frontend usa `/api/v1` como URL base por defecto. En desarrollo, Vite redirige `/api` hacia `http://127.0.0.1:8000`.

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
- `POST /api/v1/products/{product_id}/image`
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

Imagenes:

- Las imagenes se cargan a Cloudinary mediante el backend.
- El endpoint acepta imagenes JPG, PNG o WebP de hasta 4 MB.
- La URL guardada en `photo_url` usa transformaciones `f_auto` y `q_auto`.
- El `cloudinary_public_id` se guarda para futuras actualizaciones.

Frontend:

- Login con usuario y contrasena.
- Logout llama al backend para revocar token y luego limpia la sesion local.
- Creacion de referencias con foto.
- Registro de entradas usando colores controlados y talla europea decimal.
- Registro de salidas y ajustes desde cada existencia.
- Vista de historial de movimientos por existencia.

## Documentacion

La documentacion principal esta en [docs/README.md](docs/README.md).

El diseno definitivo de base de datos esta en [docs/08-diseno-base-datos.md](docs/08-diseno-base-datos.md).

## Seguridad

Los archivos `.env` reales no deben subirse al repositorio. Usar `.env.example` como referencia.
