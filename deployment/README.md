# Despliegue en Vercel

Pasos mínimos para desplegar la aplicación en Vercel usando GitHub:

1. Asegúrate de que el repositorio esté en GitHub (ya existe una rama `feat/frontend-scaffold`).
2. En Vercel, crea un nuevo proyecto y conéctalo al repositorio GitHub.
3. Configura las variables de entorno en el dashboard del proyecto (Settings → Environment Variables):
   - `DATABASE_URL` — URL de Neon Postgres.
   - `JWT_SECRET_KEY` — secreto fuerte (mínimo 32 caracteres).
   - `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`.
   - `FRONTEND_URL` — URL de la app en Vercel (por ejemplo `https://mi-proyecto.vercel.app`).
   - `SYSTEM_ADMIN_USERNAME`, `SYSTEM_ADMIN_PASSWORD`, `SYSTEM_ADMIN_FULL_NAME` (opcional, para el seed).
4. Vercel detectará la función Python en `api/index.py` y desplegará el backend como serverless.
5. El frontend está en la carpeta `frontend` y Vercel detectará el build (Vite). Si Vercel no detecta automáticamente, configura el `Build Command` a `cd frontend && npm install && npm run build` y `Output Directory` a `frontend/dist`.
6. Después del primer despliegue, ejecuta el seed para crear colores y el administrador (si configuraste las variables de seed). Puedes ejecutar el script en una máquina local con `python backend/app/database/seed.py` usando la misma `DATABASE_URL`.

Notas:
- Neon ya debe estar provisionado; pega su `DATABASE_URL` en las variables de entorno.
- Revisa `vercel.json` para ajustes de rutas ya incluidos (mapear `/` a `api/index.py`).
# Deployment

Configuraciones y notas de despliegue.

Servicios previstos:

- GitHub.
- Vercel.
- Neon PostgreSQL.
- Cloudinary.
