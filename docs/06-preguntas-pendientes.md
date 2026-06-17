# Decisiones Confirmadas y Preguntas Pendientes

Este documento registra las respuestas dadas por el usuario y las dudas que aun deben cerrarse antes de iniciar implementacion.

## Usuarios y seguridad - confirmado

1. El sistema tendra `admin` y `system_admin`.
2. `system_admin` tendra acceso a todo.
3. No habra registro publico.
4. El inicio de sesion sera con `username` y contrasena.
5. Las credenciales seran creadas por el administrador del software.
6. El primer usuario administrador se creara manualmente mediante un script seed durante el despliegue inicial.
7. En la primera version se usara solo Access Token JWT.
8. No se implementara Refresh Token en el MVP.
9. La sesion durara 8 horas.
10. Al cerrar sesion, el sistema registrara auditoria e invalidara el token para impedir su reutilizacion antes de expirar.
11. Al cerrar sesion o expirar el token, el usuario debera autenticarse de nuevo.
12. La auditoria sera visible en la interfaz.
13. `admin` sera el administrador operativo de una sede.
14. `system_admin` sera el super administrador con acceso total para mantenimiento, soporte, revision de problemas, nuevos modulos y futuras sedes.

## Productos - confirmado

1. Cada producto tendra una referencia unica.
2. La referencia identificara un modelo especifico de calzado.
3. Marca sera obligatoria.
4. Descripcion sera obligatoria.
5. La descripcion ayudara a mejorar busquedas y filtros.
6. Se manejara precio de entrada.
7. Se manejara precio de venta al consumidor final.
8. Se manejaran fotos de productos.
9. Campos obligatorios al crear referencia: referencia, marca, descripcion, foto.
10. El administrador podra crear nueva referencia, editar, sumar a existencias y eliminar logicamente.
11. El precio de entrada y el precio de venta pertenecen a la referencia general.
12. Si cambia el precio al ingresar nuevas unidades, el precio visible de la referencia se actualizara automaticamente.
13. Las imagenes se capturaran desde dispositivo movil.
14. Las imagenes se almacenaran en Cloudinary usando su plan gratuito.
15. El backend sera responsable de cargar las imagenes a Cloudinary.
16. La base de datos Neon PostgreSQL guardara solo la URL correspondiente.
17. Cloudinary aportara almacenamiento persistente, seguro y optimizado para aplicaciones web.
18. Esta decision evita perdida de archivos en despliegues serverless sobre Vercel.

## Inventario - confirmado

1. La talla sera numerica.
2. La talla usara escala europea.
3. La talla puede ser decimal, por ejemplo `30` o `30.5`.
4. El color sera catalogo controlado.
5. El color permitira seleccion multiple, por ejemplo Negro + Blanco.
6. Colores iniciales: Negro, Blanco, Gris, Azul, Rojo, Verde, Beige, Cafe, Camel, Crema, Amarillo, Naranja, Rosado, Morado, Multicolor y Otro.
7. La ubicacion fisica sera texto libre.
8. El sistema distinguira entre inventario en bodega e inventario en tienda.
9. Se permite cantidad `0`, pero debe mostrarse alerta de stock bajo.
10. No se permiten cantidades negativas.
11. El umbral de stock bajo sera de 5 unidades.
12. Cuando exista la misma referencia, talla, color y ubicacion, una nueva entrada sumara unidades al stock existente.
13. Solo se creara nuevo registro de inventario cuando la combinacion referencia, talla, color y ubicacion no exista.
14. Al sumar stock se deberan verificar precios de entrada y venta, permitiendo modificarlos si han cambiado con el tiempo.
15. Toda salida representa una venta.
16. Se permitiran ajustes manuales.
17. El administrador puede registrar entradas, salidas y ajustes.
18. Campos obligatorios de inventario: referencia, color, talla, numero de unidades, ubicacion, precio de entrada y precio de venta.
19. Las cantidades no podran modificarse directamente una vez registradas.
20. En caso de errores, se realizaran movimientos de ajuste positivos o negativos.
21. Todo ajuste requiere motivo.
22. Todo ajuste registrara fecha, usuario y modificacion realizada.
23. Los ajustes negativos no podran dejar cantidad menor que `0`.

## Operacion - confirmado

1. Existe una sola bodega.
2. La descripcion o detalle de ubicacion indicara donde esta el producto dentro de la bodega.
3. El punto fisico puede tener uno o varios pares de exhibicion segun necesidad del administrador.
4. El sistema debe distinguir inventario en bodega e inventario en tienda.
5. Se requiere un modulo o vista de historial de movimientos de entrada y salida.
6. No se requiere exportar a Excel o PDF en la primera version.

## Modulo futuro de ropa - confirmado

1. Se contempla un modulo aparte para ingreso de ropa.
2. El modulo de ropa usara catalogos controlados.
3. Catalogos previstos para ropa: categorias, tallas y genero.
4. No se usara texto libre para categoria, talla ni genero en ropa.
5. El modulo estara contemplado, pero no se agregaran funcionalidades que no correspondan al modulo de zapatos en la primera version.

## Despliegue - confirmado

1. Se desea desplegar en Vercel.
2. El backend se desarrollara en Python con FastAPI.
3. El backend se desplegara en Vercel mediante funciones Python compatibles con ASGI.
4. El frontend usara React, TypeScript, JavaScript y CSS.
5. La base de datos sera Neon PostgreSQL.
6. La arquitectura sera serverless.
7. No hay base de datos Neon creada.
8. No hay repositorio GitHub creado.
9. La URL final aun no esta definida.

## Imagenes - confirmado

1. Las imagenes de productos se almacenaran en Cloudinary usando su plan gratuito.
2. El backend sera responsable de cargar las imagenes al servicio.
3. La base de datos Neon PostgreSQL almacenara solo la URL correspondiente.
4. Cloudinary evitara perdida de archivos en despliegues serverless sobre Vercel.
5. Cloudinary mejorara el rendimiento mediante optimizacion automatica de imagenes.
6. Esta decision prepara el sistema para futuras funcionalidades como catalogo publico de productos.

## Color signature - confirmado

1. `color_signature` se generara automaticamente desde los colores seleccionados.
2. No sera editable manualmente.
3. La combinacion se ordenara y normalizara internamente.
4. `Negro + Blanco` sera equivalente a `Blanco + Negro`.
5. Esta regla evitara duplicados por diferencias en el orden de seleccion.

## Preguntas pendientes reales

No hay preguntas de negocio pendientes para el modulo inicial de inventario de calzado.

## Siguiente objetivo recomendado

Disenar la base de datos definitiva del modulo de calzado y preparar la estructura inicial del repositorio.
