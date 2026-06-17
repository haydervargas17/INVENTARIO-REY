# Diseno Preliminar de API

La API sera REST y estara construida con FastAPI.

## Formato estandar de respuesta

Todas las respuestas deben seguir este formato:

```json
{
  "success": true,
  "message": "Operacion realizada correctamente.",
  "data": {},
  "errors": null
}
```

En caso de error:

```json
{
  "success": false,
  "message": "No se pudo completar la operacion.",
  "data": null,
  "errors": [
    {
      "field": "quantity",
      "message": "La cantidad no puede ser negativa."
    }
  ]
}
```

## Autenticacion

### POST `/api/v1/auth/login`

Permite iniciar sesion con usuario y contrasena.

Request preliminar:

```json
{
  "username": "admin",
  "password": "secret"
}
```

Response preliminar:

```json
{
  "success": true,
  "message": "Inicio de sesion exitoso.",
  "data": {
    "access_token": "jwt",
    "token_type": "bearer",
    "user": {
      "id": "uuid",
      "username": "admin",
      "role": "admin"
    }
  },
  "errors": null
}
```

Reglas confirmadas:

- Se usara `username`.
- Se usara solo Access Token JWT en la primera version.
- No habra Refresh Token en el MVP.
- El Access Token durara 8 horas.
- No existira registro publico.
- El primer administrador se creara mediante script seed.

### POST `/api/v1/auth/logout`

Registra auditoria de cierre de sesion e invalida el token.

Reglas:

- Debe registrar el evento en auditoria.
- Debe invalidar el token de acceso para impedir su reutilizacion antes de expirar.
- El Access Token debe incluir un identificador unico `jti`.
- El `jti` del token cerrado debe almacenarse como token revocado hasta su expiracion.
- Las rutas protegidas deben rechazar tokens cuyo `jti` este revocado.
- Al cerrar sesion o expirar el token, el usuario debera autenticarse nuevamente.

## Inventario

### GET `/api/v1/inventory`

Lista existencias de inventario con filtros.

Filtros preliminares:

- `reference`
- `name`
- `size`
- `color`
- `location_type`
- `location_detail`
- `available_only`
- `low_stock_only`

Reglas confirmadas:

- La busqueda debe permitir encontrar referencias por descripcion.
- Debe distinguir inventario en bodega e inventario en tienda.

### POST `/api/v1/inventory`

Registra una nueva existencia o entrada de producto.

Request preliminar:

```json
{
  "product": {
    "name": "Nike Air Max",
    "reference": "AIRMAX-001",
    "brand": "Nike",
    "description": "Zapato deportivo AAA",
    "photo_url": "https://res.cloudinary.com/demo/image/upload/v1/products/airmax-001/main.webp",
    "current_purchase_price": 100000,
    "current_sale_price": 180000
  },
  "size": 38,
  "color_ids": ["uuid-negro", "uuid-blanco"],
  "location_type": "WAREHOUSE",
  "location_detail": "A-01",
  "quantity": 3
}
```

Reglas confirmadas:

- Si ya existe la misma referencia, talla, color y ubicacion, se suma la cantidad al registro existente.
- Solo se crea una nueva existencia cuando la combinacion no existe.
- La talla sera numerica decimal en escala europea.
- Color sera catalogo controlado y permitira multiples colores.
- `color_signature` se generara automaticamente, ordenando y normalizando los colores seleccionados.
- `color_signature` no se recibira como campo editable desde el frontend.
- La ubicacion fisica sera texto libre y se debe distinguir bodega o tienda.

### POST `/api/v1/inventory/{inventory_item_id}/entries`

Registra entrada de unidades a una existencia.

Request preliminar:

```json
{
  "quantity": 5,
  "purchase_unit_price": 100000,
  "sale_unit_price": 180000,
  "reason": "Ingreso de mercancia"
}
```

Reglas:

- Debe verificar si la combinacion referencia, talla, color y ubicacion ya existe.
- Si existe, suma unidades.
- Si el precio cambio, debe registrar el nuevo precio en el movimiento.
- El precio pertenece a la referencia general.
- Si el precio cambio, debe actualizar automaticamente el precio vigente de la referencia.

### POST `/api/v1/inventory/{inventory_item_id}/exits`

Registra salida de unidades.

Request preliminar:

```json
{
  "quantity": 1,
  "reason": "Venta"
}
```

Reglas:

- La cantidad debe ser mayor que cero.
- No se permite dejar cantidad negativa.
- Toda salida representa una venta.
- Debe guardar el precio de venta historico al momento de la venta.
- Debe crear movimiento.
- Debe crear auditoria.

### PATCH `/api/v1/inventory/{inventory_item_id}`

Actualiza datos permitidos de una existencia.

Reglas confirmadas:

- El administrador podra editar referencias y existencias.
- El administrador podra sumar unidades a existencias.
- El administrador podra eliminar logicamente.
- La cantidad no podra modificarse directamente.
- Las correcciones de cantidad se haran mediante ajustes positivos o negativos.

### POST `/api/v1/inventory/{inventory_item_id}/adjustments`

Registra un ajuste manual de inventario.

Request preliminar:

```json
{
  "quantity_delta": -1,
  "reason": "Correccion por error de conteo"
}
```

Reglas:

- `quantity_delta` no puede ser `0`.
- Puede ser positivo o negativo.
- Un ajuste negativo no puede dejar inventario por debajo de cero.
- El motivo es obligatorio.
- Debe registrar fecha, usuario, cantidad anterior, cambio realizado y nueva cantidad.
- Debe crear auditoria.

### DELETE `/api/v1/inventory/{inventory_item_id}`

Realiza eliminacion logica.

Reglas:

- No debe eliminar fisicamente.
- Debe registrar auditoria.

## Productos

### GET `/api/v1/products`

Lista productos.

### POST `/api/v1/products`

Crea producto base.

Reglas confirmadas:

- El administrador podra crear nuevas referencias.
- Campos obligatorios: referencia, marca, descripcion, foto, talla, color, cantidad, ubicacion, precio de entrada y precio de venta.

### POST `/api/v1/products/{product_id}/image`

Carga la imagen principal de una referencia.

Reglas:

- La imagen sera capturada desde dispositivo movil o seleccionada desde el equipo del administrador.
- El backend cargara la imagen a Cloudinary.
- Cloudinary almacenara la imagen de forma persistente.
- Cloudinary entregara la imagen optimizada para web.
- La base de datos guardara la URL de la imagen principal.
- El sistema podra guardar el `cloudinary_public_id` para futuras actualizaciones o eliminaciones logicas.
- Las credenciales de Cloudinary se configuraran mediante variables de entorno.

## Auditoria

### GET `/api/v1/audit-logs`

Lista eventos de auditoria.

Reglas confirmadas:

- La auditoria sera visible en la interfaz.

## Historial de movimientos

### GET `/api/v1/inventory/{inventory_item_id}/movements`

Lista historial de entradas, salidas y ajustes de una existencia.

Reglas:

- Debe incluir fecha, usuario, tipo de movimiento, cantidad anterior, cantidad nueva, precio registrado y motivo.

## Catalogos

### GET `/api/v1/catalogs/colors`

Lista colores controlados.

### GET `/api/v1/catalogs/location-types`

Lista tipos de ubicacion.

Valores iniciales:

- `WAREHOUSE`: bodega.
- `STORE`: tienda.

## Ropa

El modulo de ropa estara contemplado en la arquitectura, pero no se agregaran funcionalidades que no correspondan al modulo de zapatos durante la primera version.

## Codigos HTTP esperados

- `200 OK`: consulta o accion exitosa.
- `201 Created`: recurso creado.
- `400 Bad Request`: datos invalidos.
- `401 Unauthorized`: no autenticado.
- `403 Forbidden`: sin permisos.
- `404 Not Found`: recurso no encontrado.
- `409 Conflict`: conflicto de negocio.
- `422 Unprocessable Entity`: error de validacion.
- `500 Internal Server Error`: error inesperado.
