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

Pendiente para conectar:

- Definir nombre del repositorio.
- Definir si sera privado o publico.
- Iniciar sesion en GitHub desde esta maquina.
- Crear el repositorio remoto.
- Vincular el remoto con el repositorio local.

## Vercel

Pendiente para conectar:

- Instalar o ejecutar Vercel CLI.
- Iniciar sesion con la cuenta de Vercel.
- Vincular el proyecto local.
- Configurar variables de entorno en Vercel.
- Validar despliegue de funciones Python compatibles con ASGI para FastAPI.

## Neon PostgreSQL

Pendiente para conectar:

- Crear proyecto en Neon.
- Crear base de datos inicial.
- Obtener `DATABASE_URL`.
- Guardar `DATABASE_URL` en `.env` local y variables de entorno de Vercel.

## Cloudinary

Pendiente para conectar:

- Crear cuenta o usar cuenta existente de Cloudinary.
- Obtener `CLOUDINARY_CLOUD_NAME`.
- Obtener `CLOUDINARY_API_KEY`.
- Obtener `CLOUDINARY_API_SECRET`.
- Guardar credenciales en `.env` local y variables de entorno de Vercel.

## Regla de seguridad

Nunca subir archivos `.env` reales al repositorio. Solo se permite subir `.env.example`.
