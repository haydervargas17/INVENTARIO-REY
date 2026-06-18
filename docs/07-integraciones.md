# Integraciones y Cuentas

Este documento define como se conectaran los servicios externos del proyecto sin exponer credenciales sensibles.

## Servicios

- GitHub: repositorio remoto del codigo.
- Vercel: despliegue serverless de frontend y backend FastAPI/Python.
- Neon PostgreSQL: base de datos.
- Cloudinary: almacenamiento y optimizacion de imagenes de productos.

## Variables de entorno requeridas

Las credenciales reales no deben escribirse en la documentacion ni subirse al repositorio.

```env
DATABASE_URL=
JWT_SECRET_KEY=
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
FRONTEND_URL=
```

## GitHub

Estado:

- Repositorio creado: `INVENTARIO-REY`.
- Visibilidad: publico.
- Remoto local configurado: `https://github.com/haydervargas17/INVENTARIO-REY.git`.
- Rama principal: `main`.

## Vercel

Estado:

- Vercel CLI instalado.
- Sesion iniciada con la cuenta `haydervargas17`.
- Proyecto vinculado: `haydervargas17s-projects/inventario-rey`.
- GitHub conectado al proyecto de Vercel.
- Variables principales cargadas en Production.
- FastAPI expone una instancia `app` en `app.py`, compatible con la deteccion de Vercel.

Pendiente:

- Validar despliegue real del backend base.
- Completar variables de Preview si se decide usar despliegues de ramas antes de produccion.

## Neon PostgreSQL

Estado:

- Proyecto/base de datos creada.
- `DATABASE_URL` guardado en `.env` local.
- Conexion local probada correctamente.
- Vercel tiene variables de Neon creadas por la integracion.
- Migracion inicial aplicada correctamente.
- Tablas creadas: `users`, `colors`, `products`, `inventory_items`, `inventory_item_colors`, `inventory_movements`, `audit_logs`, `revoked_tokens`.

## Cloudinary

Estado:

- Credenciales guardadas en `.env` local.
- SDK Python instalado localmente.
- Subida de imagen de prueba ejecutada correctamente.
- URL optimizada generada correctamente.
- Variables cargadas en Vercel Production.

## Regla de seguridad

Nunca subir archivos `.env` reales al repositorio. Solo se permite subir `.env.example`.
