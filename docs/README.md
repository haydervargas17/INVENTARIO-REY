# El Rey de los Zapatos - Documentacion del Proyecto

Sistema web de gestion de inventario para una empresa dedicada a la comercializacion de calzado AAA.

## Estado actual

Version documentada: 1.0

Etapa actual del proyecto:

1. Analisis del requerimiento.
2. Diseno inicial de la solucion.
3. Definicion de datos, API e interfaz.
4. Diseno definitivo de base de datos del modulo de calzado.
5. Preparacion inicial de estructura del repositorio.

No se ha iniciado implementacion de codigo porque el flujo oficial del proyecto exige documentar y disenar antes de programar.

## Fuente principal

La fuente principal de requisitos es el documento entregado por el usuario:

`Documento sin titulo.md`

## Documentos

- [01-analisis.md](01-analisis.md): problema, objetivo, alcance inicial y restricciones.
- [02-arquitectura.md](02-arquitectura.md): arquitectura tecnica, stack y estructura del repositorio.
- [03-modelo-datos.md](03-modelo-datos.md): modelo preliminar de base de datos y relaciones.
- [04-api.md](04-api.md): diseno preliminar de endpoints, respuestas y errores.
- [05-interfaz.md](05-interfaz.md): pantallas iniciales, flujo de usuario y componentes.
- [06-preguntas-pendientes.md](06-preguntas-pendientes.md): decisiones confirmadas y dudas restantes antes de programar.
- [07-integraciones.md](07-integraciones.md): cuentas, servicios externos y variables de entorno.
- [08-diseno-base-datos.md](08-diseno-base-datos.md): esquema definitivo de PostgreSQL para el modulo de calzado.

## Regla de trabajo

No se debe asumir logica de negocio no definida. Cuando una regla no este clara, debe registrarse como pregunta pendiente y confirmarse antes de implementarla.
