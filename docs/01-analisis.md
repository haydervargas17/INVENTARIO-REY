# Analisis del Requerimiento

## Problema

La empresa actualmente gestiona el inventario de calzado de forma manual. El punto de venta y la bodega estan en ubicaciones diferentes, lo que dificulta confirmar rapidamente si una referencia, talla, color y ubicacion tienen unidades disponibles.

Esto genera:

- Perdida de tiempo en la atencion al cliente.
- Demoras para confirmar disponibilidad.
- Posibles perdidas de ventas.
- Desorganizacion en entradas y salidas.
- Dependencia del conocimiento de los empleados.
- Falta de una fuente centralizada y actualizada del inventario.

## Objetivo

Desarrollar un aplicativo web profesional para gestionar inventario de calzado AAA, permitiendo consultar en tiempo real disponibilidad por referencia, talla, color, ubicacion y cantidad.

## Alcance inicial

Version 1.0:

- Autenticacion de usuarios autorizados con `username` y contrasena.
- Inventario centralizado.
- Registro de ingreso de productos.
- Consulta de disponibilidad.
- Registro de salidas de mercancia.
- Historial visible de movimientos de entrada y salida.
- Auditoria de acciones importantes.
- Soft delete en registros.

## Fuera del alcance inicial

El documento menciona funcionalidades futuras, pero no forman parte obligatoria de la primera version salvo confirmacion expresa:

- Catalogo publico.
- Proveedores.
- Ventas completas.
- Facturacion.
- Multiples sedes.
- Transferencias entre bodegas.
- Reportes avanzados.
- Dashboard.
- Carga masiva por Excel.
- Codigo QR.
- Codigo de barras.
- Aplicacion movil.
- API publica.
- Exportacion a Excel o PDF.

## Principios obligatorios

- Escalable.
- Seguro.
- Modular.
- Facil de mantener.
- Facil de desplegar.
- Optimizado para uso diario.
- Preparado para futuras funcionalidades.

## Reglas confirmadas

- No existira registro publico.
- El primer usuario administrador se creara mediante un script seed durante el despliegue inicial.
- Las credenciales seran generadas y entregadas solo por el administrador del software.
- Las contrasenas se almacenaran con BCrypt.
- La autenticacion usara Access Token JWT.
- En la primera version no se implementara Refresh Token.
- La sesion durara 8 horas.
- Al cerrar sesion, el token debe invalidarse para impedir su reutilizacion antes de expirar.
- Toda comunicacion en produccion debera realizarse mediante HTTPS.
- Toda validacion existira en frontend y backend.
- Las consultas deberan ser parametrizadas.
- No se deben eliminar fisicamente registros.
- Se usara soft delete.
- Todas las tablas deben incluir `id`, `created_at`, `updated_at` y `deleted_at`.
- Las respuestas de API deben ser consistentes.
- Toda accion importante debe quedar auditada.

## Regla central de inventario

Cada producto o existencia se identifica por:

- Referencia.
- Talla.
- Color.
- Tipo de ubicacion: bodega o tienda.
- Ubicacion o descripcion fisica.
- Cantidad.
- Precio de entrada.
- Precio de venta al consumidor final.
- Foto de la referencia.
- Descripcion de la referencia.

No se almacenara una cantidad general unica del producto.

Ejemplo:

- Nike Air Max, talla 38, color Negro + Blanco, cantidad 3, ubicacion Bodega / A-01.
- Nike Air Max, talla 39, color Negro + Blanco, cantidad 5, ubicacion Tienda / Exhibicion.

## Alcance adicional confirmado

- El sistema debe distinguir inventario en bodega e inventario en tienda.
- La bodega es unica, pero puede tener descripciones libres de ubicacion interna.
- El punto fisico puede tener uno o varios pares de exhibicion.
- El administrador podra crear nuevas referencias, editar referencias, sumar unidades a existencias y eliminar logicamente.
- Se permitiran ajustes manuales de inventario.
- Las cantidades no podran modificarse directamente despues de registradas.
- Los errores de cantidad se corregiran mediante movimientos de ajuste positivos o negativos con motivo obligatorio.
- Las salidas representan ventas.
- El stock en cero esta permitido, pero debe mostrarse alerta de stock bajo.
- No se permiten cantidades negativas.
- El umbral de stock bajo sera de 5 unidades.
- Se contempla un modulo futuro de ropa con catalogos controlados de categoria, talla y genero.
