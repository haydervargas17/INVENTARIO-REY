# Frontend

Aplicacion web inicial del sistema de inventario.

Stack:

- React.
- TypeScript.
- Vite.
- TailwindCSS.
- React Router.
- Axios.
- React Query.
- React Hook Form.
- Framer Motion.

## Ejecucion local

```powershell
cd frontend
npm install
npm run dev
```

Variables de entorno opcionales:

- `VITE_API_BASE_URL`: URL base de la API. Por defecto usa `/api/v1`.

En desarrollo, `vite.config.ts` redirige `/api` hacia `http://127.0.0.1:8000`.

## Estado actual

- Login conectado al backend.
- Panel de inventario con cards.
- Creacion de referencias con foto.
- Registro de entradas, salidas y ajustes.
- Historial de movimientos por existencia.

La implementacion debe seguir los flujos y componentes definidos en `docs/05-interfaz.md`.
