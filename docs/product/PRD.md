# PRD — Asistente Financiero Personal Inteligente - KAIROS

**Nombre provisional:** Personal Finance AI  
**Versión:** 1.0  
**Fecha:** 17 de noviembre de 2026  
**Estado:** Definición inicial del producto  
**Tipo de producto:** Aplicación web con capacidades de inteligencia artificial  
**Mercado inicial:** Uso personal en Ecuador, con posibilidad de evolucionar a un producto multiusuario.

---

# 1. Resumen ejecutivo

Personal Finance AI es una aplicación web que permitirá a los usuarios gestionar, analizar y planificar sus finanzas personales mediante una combinación de herramientas financieras tradicionales e inteligencia artificial.

El producto busca ir más allá de un gestor de gastos convencional. Su propósito es ayudar al usuario a comprender su situación financiera, identificar patrones de consumo, establecer objetivos de ahorro, anticipar desviaciones y evaluar las consecuencias económicas de decisiones antes de realizarlas.

La aplicación permitirá importar estados de cuenta bancarios, registrar movimientos manualmente, administrar múltiples cuentas y tarjetas, establecer presupuestos y objetivos financieros y consultar un asistente inteligente que utilizará los datos del usuario para generar análisis y simulaciones.

La privacidad será un requisito fundamental: los documentos financieros originales deberán procesarse y anonimizarse localmente antes de transmitir información al backend.

El producto comenzará como una herramienta de uso personal, pero su arquitectura estará preparada para incorporar múltiples usuarios y evolucionar hacia un posible servicio comercial.

# 2. Problema que busca resolver

La gestión financiera personal suele estar fragmentada entre aplicaciones bancarias, hojas de cálculo, documentos PDF y registros manuales.

Esto genera diferentes problemas:

- Dificultad para conocer cuánto dinero se gasta realmente.
- Falta de visibilidad sobre los gastos pequeños y recurrentes.
- Dificultad para consolidar información de diferentes cuentas bancarias.
- Desconocimiento de cuánto dinero se puede gastar sin comprometer objetivos.
- Falta de seguimiento de presupuestos y metas de ahorro.
- Dificultad para evaluar si una compra importante es financieramente conveniente.
- Falta de alertas oportunas cuando los hábitos de consumo afectan los objetivos.

Las aplicaciones tradicionales suelen mostrar información histórica, pero no necesariamente ayudan a responder preguntas sobre decisiones futuras.

**Oportunidad:** desarrollar un asistente que transforme los movimientos financieros en información útil para planificar y tomar decisiones.

# 3. Objetivos del producto

## 3.1 Objetivo general

Desarrollar una aplicación web de gestión y planificación financiera personal que utilice inteligencia artificial para analizar el comportamiento económico del usuario, supervisar objetivos financieros y asistir en la toma de decisiones.

## 3.2 Objetivos específicos

1. Centralizar los movimientos de diferentes cuentas y entidades financieras.
2. Facilitar la importación y clasificación de transacciones.
3. Identificar gastos, ingresos, transferencias internas y rendimientos.
4. Permitir establecer presupuestos y objetivos financieros simultáneos.
5. Detectar desviaciones en los hábitos de consumo.
6. Proyectar la capacidad de ahorro y el cumplimiento de objetivos.
7. Simular compras y evaluar su impacto financiero.
8. Proporcionar un asistente conversacional basado en información financiera verificable.
9. Garantizar la privacidad y el aislamiento de los datos de cada usuario.
10. Crear una arquitectura escalable y preparada para un despliegue comercial.

# 4. Usuarios objetivo

## 4.1 Usuario inicial

Persona que desea administrar sus finanzas personales, controlar sus gastos, ahorrar y comprender mejor sus decisiones económicas.

Características:

- Maneja una o varias cuentas bancarias.
- Puede utilizar tarjetas de crédito.
- Recibe estados de cuenta en PDF.
- Realiza gastos mediante transferencias, tarjetas y efectivo.
- Tiene objetivos de ahorro.
- Desea conocer su capacidad real de gasto.
- Busca recomendaciones basadas en sus propios movimientos financieros.

## 4.2 Evolución futura

La aplicación podrá admitir múltiples usuarios independientes, cada uno con sus propias cuentas, transacciones, presupuestos, objetivos y configuraciones.

Se contempla la posibilidad de convertir el proyecto en un producto SaaS, sujeto a validación de mercado y requisitos adicionales de seguridad, soporte y operación.

# 5. Alcance funcional

## 5.1 Gestión de usuarios y autenticación

La aplicación dispondrá de un sistema de autenticación para controlar el acceso a la información financiera.

Requisitos:

- Registro de usuarios.
- Inicio y cierre de sesión.
- Recuperación de acceso.
- Verificación de identidad.
- Protección de rutas y operaciones.
- Identificación de usuarios mediante un identificador estable.
- Autorización en el backend.
- Aislamiento de información por usuario.
- Preparación para autenticación multifactor.

**Tecnología propuesta:** Microsoft Entra External ID para la gestión de identidad, MSAL Angular para la integración del frontend y validación de tokens JWT en FastAPI.

La autenticación y la autorización serán responsabilidades diferenciadas. Entra verificará la identidad; el backend determinará los recursos y operaciones a los que tiene acceso cada usuario.

## 5.2 Gestión de bancos, cuentas y tarjetas

El sistema permitirá registrar múltiples entidades financieras y productos asociados.

Requisitos:

- Registrar diferentes bancos.
- Crear varias cuentas dentro de un mismo banco.
- Registrar cuentas de ahorro, corrientes y ahorro programado.
- Registrar tarjetas de crédito.
- Asignar nombres personalizados a las cuentas.
- Definir el propósito de cada cuenta.
- Consultar movimientos por cuenta.
- Consultar saldos cuando exista información suficiente.
- Asociar estados de cuenta con una cuenta o tarjeta.
- Identificar cuentas propias para conciliar transferencias internas.

Los identificadores bancarios sensibles no deberán almacenarse completos si no son necesarios. Se priorizará el uso de identificadores internos y referencias enmascaradas.

## 5.3 Importación de estados de cuenta

La primera integración bancaria será Banco Pichincha Ecuador.

Se contemplan dos tipos de documentos:

1. Estado de cuenta de movimientos y transferencias de cuentas bancarias.
2. Estado de cuenta de consumos y movimientos de tarjetas.

Requisitos:

- Seleccionar el banco y la cuenta correspondiente.
- Importar archivos PDF.
- Extraer fechas, descripciones, importes, monedas y tipos de movimiento.
- Identificar documentos y movimientos duplicados.
- Asociar cada movimiento con su documento de origen.
- Clasificar automáticamente los movimientos.
- Mostrar una vista previa antes de confirmar.
- Permitir corregir información extraída.
- Registrar errores y movimientos que requieren revisión.
- Mantener trazabilidad de las importaciones.

### Privacidad durante la importación

El documento original deberá permanecer en el dispositivo del usuario durante el procesamiento inicial.

El flujo será:

1. Selección del PDF.
2. Extracción local de texto y tablas.
3. OCR local cuando sea necesario.
4. Detección de información confidencial.
5. Redacción o eliminación real de datos sensibles.
6. Revisión y confirmación del usuario.
7. Transmisión de los datos financieros mínimos necesarios.
8. Procesamiento y almacenamiento en el backend.

No se considerará anonimización válida la simple superposición visual de rectángulos sobre información confidencial.

Si no es posible garantizar que el contenido sensible ha sido eliminado, la aplicación deberá detener la importación y solicitar revisión.

Los PDF originales no se enviarán a Microsoft Foundry.

## 5.4 Registro manual de movimientos

El usuario podrá registrar movimientos que no aparezcan en los documentos importados.

Ejemplos:

- Gastos en efectivo.
- Compras pequeñas.
- Propinas.
- Ingresos adicionales.
- Gastos compartidos.
- Movimientos que no aparecen en los estados de cuenta.

Datos principales:

- Fecha.
- Descripción.
- Importe.
- Moneda.
- Tipo de movimiento.
- Cuenta o medio de pago, cuando corresponda.
- Categoría y subcategoría.
- Observaciones opcionales.

La experiencia deberá facilitar el registro desde dispositivos móviles.

## 5.5 Clasificación y conciliación financiera

El sistema distinguirá entre:

- Ingresos.
- Gastos.
- Compras con tarjeta.
- Transferencias internas.
- Transferencias externas.
- Pagos de tarjetas.
- Retiros y depósitos.
- Devoluciones.
- Intereses.
- Comisiones.
- Otros movimientos financieros.

### Reglas de conciliación

Las transferencias entre cuentas propias no se contabilizarán como gastos ni como ingresos.

Ejemplo:

Una transferencia de $200 desde una cuenta personal hacia una cuenta de ahorro programado representa:

- Salida de $200 de la cuenta de origen.
- Entrada de $200 en la cuenta de destino.
- Cero dólares de gasto real.

El sistema deberá relacionar ambos movimientos cuando sea posible.

También deberá evitar contabilizar dos veces una compra con tarjeta y el posterior pago de esa tarjeta desde una cuenta bancaria.

Los intereses recibidos sí se considerarán ingresos financieros.

La conciliación automática requerirá confirmación cuando exista incertidumbre.

## 5.6 Categorías y presupuestos

El usuario podrá organizar sus gastos mediante categorías y subcategorías.

Categorías iniciales propuestas:

- Alimentación.
- Transporte.
- Vivienda.
- Servicios básicos.
- Salud.
- Educación.
- Entretenimiento.
- Compras personales.
- Suscripciones.
- Ahorro.
- Otros.

Requisitos:

- Crear categorías personalizadas.
- Asignar categorías a movimientos.
- Configurar presupuestos mensuales.
- Consultar el presupuesto consumido.
- Detectar desviaciones.
- Comparar períodos.
- Identificar categorías con mayor crecimiento.
- Recomendar ajustes de presupuesto.

Los presupuestos deberán poder configurarse independientemente de los objetivos de ahorro.

## 5.7 Objetivos financieros

El sistema permitirá crear y administrar múltiples objetivos simultáneamente.

Cada objetivo tendrá:

- Nombre.
- Descripción.
- Importe objetivo.
- Importe acumulado.
- Fecha de creación.
- Fecha límite.
- Prioridad.
- Estado.
- Cuenta asociada opcional.
- Historial de aportaciones.

Tipos de objetivos:

- Objetivos con ahorro reservado en una cuenta específica.
- Objetivos basados en la capacidad financiera general del usuario.

Ejemplos:

- Ahorrar $1.000 en tres meses.
- Crear un fondo de emergencia de $2.000.
- Ahorrar para vacaciones.
- Comprar un dispositivo.
- Ahorrar para un proyecto personal.

### Priorización

Los objetivos podrán tener prioridad alta, media o baja.

El sistema deberá evaluar los objetivos de manera conjunta para identificar conflictos de capacidad de ahorro.

No deberá modificar automáticamente las metas, prioridades o fechas límite.

## 5.8 Seguimiento y proyección de ahorro

El sistema analizará los ingresos, gastos, compromisos y aportaciones para calcular la capacidad de ahorro.

Requisitos:

- Calcular el ahorro necesario por período.
- Comparar el ahorro esperado con el real.
- Proyectar el cumplimiento de objetivos.
- Identificar desviaciones.
- Estimar el ahorro acumulado.
- Evaluar diferentes escenarios.
- Mostrar cuánto falta para alcanzar cada objetivo.

Las proyecciones deberán identificar sus supuestos y nivel de incertidumbre.

## 5.9 Análisis inteligente de gastos

El sistema deberá identificar patrones financieros y generar alertas cuando existan desviaciones relevantes.

Casos de uso:

- Detección de gastos hormiga.
- Incrementos inusuales.
- Gastos recurrentes.
- Suscripciones.
- Categorías que superan su presupuesto.
- Gastos que crecen respecto a meses anteriores.
- Diferencias entre ingresos y gastos.
- Comportamientos que ponen en riesgo los objetivos.

Las recomendaciones deberán estar contextualizadas. Un gasto no se clasificará automáticamente como innecesario sin considerar las preferencias y compromisos del usuario.

## 5.10 Simulador de decisiones y compras

El usuario podrá consultar el impacto de una compra antes de realizarla.

Ejemplo:

"Quiero comprar un dron de $600. ¿Puedo hacerlo sin afectar mis objetivos?"

El sistema deberá considerar:

- Dinero disponible.
- Ingresos esperados.
- Gastos habituales.
- Compromisos pendientes.
- Objetivos activos.
- Prioridades.
- Fechas límite.
- Reserva de emergencia, si existe.
- Otros escenarios financieros relevantes.

Resultados posibles:

- Compra compatible con los objetivos.
- Compra posible, pero con ajustes necesarios.
- Compra que pone en riesgo uno o varios objetivos.
- Información insuficiente para emitir una evaluación confiable.

El sistema deberá mostrar:

- Impacto estimado de la compra.
- Objetivos afectados.
- Dinero restante.
- Cambios necesarios para mantener las metas.
- Alternativas como posponer la compra o ajustar una meta.

El asistente no tendrá autoridad para impedir compras ni modificar automáticamente los objetivos.

## 5.11 Dashboard financiero

La pantalla principal mostrará una visión general de la situación financiera.

Indicadores propuestos:

- Saldo consolidado de cuentas.
- Ingresos del período.
- Gastos reales del período.
- Ahorro acumulado.
- Transferencias internas.
- Gastos por categoría.
- Evolución mensual.
- Presupuestos utilizados.
- Objetivos activos.
- Progreso de ahorro.
- Alertas importantes.

Los saldos deberán diferenciarse de los importes disponibles para gastar.

## 5.12 Asistente conversacional

La aplicación incluirá un asistente financiero que permitirá consultar información mediante lenguaje natural.

Ejemplos:

- ¿Cuánto gasté en transporte este mes?
- ¿Cuáles fueron mis cinco gastos más altos?
- ¿Cuánto dinero tengo distribuido entre mis cuentas?
- ¿Cuánto he ahorrado este año?
- ¿Qué suscripciones tengo?
- ¿Estoy gastando más de lo que gano?
- ¿Cuánto necesito ahorrar este mes?
- ¿Puedo comprar un dron de $600?
- ¿Qué pasaría si reduzco mis gastos de entretenimiento?
- ¿Qué objetivo financiero está en mayor riesgo?

El asistente utilizará herramientas controladas para consultar información y ejecutar cálculos.

No tendrá acceso SQL ilimitado ni podrá modificar datos financieros sin autorización.

# 6. Automatizaciones

Se contempla incorporar progresivamente:

- Clasificación automática al importar movimientos.
- Detección de duplicados.
- Conciliación de transferencias.
- Alertas de presupuesto.
- Alertas de objetivos en riesgo.
- Identificación de pagos recurrentes.
- Resúmenes semanales.
- Informes mensuales.
- Revisión de notificaciones bancarias por correo electrónico.

La integración con Gmail será posterior al MVP. Utilizará OAuth y permisos mínimos, inicialmente de solo lectura, con filtros para identificar notificaciones financieras relevantes.

No se enviará contenido completo de correos a modelos de IA sin una política de minimización y redacción previa.

# 7. Requisitos no funcionales

## 7.1 Seguridad

- Autenticación mediante proveedor especializado.
- Autorización en el backend.
- Aislamiento de datos por usuario.
- Cifrado en tránsito mediante HTTPS.
- Cifrado en reposo.
- Gestión segura de secretos.
- Protección contra accesos no autorizados.
- Auditoría de operaciones relevantes.
- Validación estricta de archivos importados.
- Control de permisos para las herramientas del agente.

## 7.2 Privacidad

- Minimización de datos.
- Procesamiento local de documentos originales.
- Eliminación de identificadores innecesarios.
- Transparencia sobre los datos transmitidos.
- Consentimiento para integraciones externas.
- Políticas de retención y eliminación.
- Separación de información por usuario.
- No utilizar información financiera personal para entrenamiento de modelos.

## 7.3 Rendimiento

- Consultas financieras frecuentes optimizadas.
- Procesamiento de importaciones en segundo plano cuando sea necesario.
- Interfaz adaptable a dispositivos móviles.
- Paginación de historiales.
- Evitar llamadas innecesarias a modelos de IA.

Los objetivos concretos de rendimiento se definirán mediante pruebas y mediciones del MVP.

## 7.4 Disponibilidad y recuperación

- Copias de seguridad de la base de datos.
- Registro de errores.
- Monitoreo de servicios.
- Procedimientos de recuperación.
- Separación de entornos.
- Gestión de versiones y migraciones.

## 7.5 Escalabilidad

La arquitectura deberá permitir:

- Incorporar nuevos bancos.
- Incorporar nuevos formatos de documentos.
- Agregar usuarios.
- Añadir nuevas herramientas de IA.
- Integrar servicios externos.
- Ampliar el procesamiento de información.

# 8. Arquitectura tecnológica propuesta

## 8.1 Frontend

- Angular 19.
- TypeScript.
- MSAL Angular.
- Diseño responsive.
- Componentes reutilizables.

## 8.2 Backend

- Python.
- FastAPI.
- Pydantic.
- SQLAlchemy.
- Alembic para migraciones.
- Servicios separados por responsabilidad.

## 8.3 Base de datos

- PostgreSQL.
- pgvector cuando exista una necesidad de búsqueda vectorial.
- Índices y restricciones de integridad.
- Aislamiento de información por usuario.

## 8.4 Inteligencia artificial

- Microsoft Foundry para acceso y gestión de modelos.
- Microsoft Agent Framework para orquestación cuando se justifique.
- Herramientas Python para cálculos.
- RAG para recuperar información documental relevante cuando sea necesario.
- Evaluaciones de calidad, seguridad y alucinaciones.

El uso de agentes múltiples, bases vectoriales y grafos no será obligatorio en el MVP. Se incorporarán únicamente cuando exista una necesidad funcional demostrable.

## 8.5 Identidad

- Microsoft Entra External ID.
- MSAL Angular.
- Validación JWT en FastAPI.
- Autorización basada en identidad y permisos.

## 8.6 Infraestructura y DevOps

- GitHub.
- GitHub Actions.
- Docker y Docker Compose.
- Azure Static Web Apps para frontend.
- Azure Container Apps para backend.
- Azure Database for PostgreSQL, sujeto a evaluación de costos.
- Azure Key Vault.
- Application Insights.
- Bicep para infraestructura como código.

La arquitectura comenzará localmente y evolucionará hacia Azure mediante entornos independientes.

# 9. Modelo de datos conceptual inicial

El siguiente modelo representa las entidades principales. No constituye todavía el esquema SQL definitivo.

| Entidad                | Responsabilidad                     |
| ---------------------- | ----------------------------------- |
| users                  | Identidad interna del usuario       |
| banks                  | Entidades financieras               |
| financial_accounts     | Cuentas bancarias                   |
| payment_cards          | Tarjetas                            |
| statement_imports      | Importaciones de documentos         |
| transactions           | Movimientos financieros             |
| transaction_categories | Categorías y subcategorías          |
| merchants              | Comercios                           |
| transfer_groups        | Relación de transferencias internas |
| budgets                | Presupuestos                        |
| financial_goals        | Objetivos de ahorro                 |
| goal_contributions     | Aportaciones a objetivos            |
| recurring_rules        | Gastos e ingresos recurrentes       |
| transaction_audit      | Historial de cambios                |
| data_sources           | Origen de los movimientos           |

### Consideraciones del modelo

- Las entidades financieras tendrán un `user_id` o una relación equivalente que permita aislamiento.
- Cada cuenta podrá tener múltiples estados de cuenta.
- Cada importación podrá generar múltiples transacciones.
- Cada transacción tendrá una fuente identificable.
- Las transferencias internas podrán relacionar dos movimientos.
- Los objetivos podrán recibir múltiples aportaciones.
- Los movimientos podrán tener categorías personalizadas.
- Se utilizarán identificadores estables para evitar depender del correo electrónico.
- Los importes utilizarán tipos numéricos decimales, nunca valores de punto flotante para cálculos monetarios.

El modelo deberá evolucionar después de inspeccionar formatos de documentos sintéticos que representen los estados de cuenta de Banco Pichincha.

# 10. Alcance del MVP

La primera versión funcional tendrá como objetivo demostrar que la aplicación puede centralizar movimientos financieros, organizar gastos y ayudar a controlar objetivos de ahorro.

### Funcionalidades incluidas

1. Registro e inicio de sesión.
2. Aislamiento de información por usuario.
3. Registro de Banco Pichincha.
4. Gestión de múltiples cuentas.
5. Registro de tarjetas.
6. Importación de PDF de movimientos bancarios.
7. Importación de PDF de tarjetas.
8. Procesamiento y anonimización local.
9. Vista previa y validación de movimientos.
10. Registro manual.
11. Clasificación de movimientos.
12. Conciliación de transferencias internas.
13. Detección de duplicados.
14. Presupuestos por categoría.
15. Múltiples objetivos financieros y prioridades.
16. Dashboard financiero.
17. Alertas de desviación.
18. Proyecciones de ahorro.
19. Simulador básico de compras.

### Funcionalidades excluidas inicialmente

- Integración con Gmail.
- Conexión bancaria directa mediante APIs.
- Soporte para todos los bancos.
- Importación automática de datos bancarios en tiempo real.
- Multiagentes complejos.
- Grafos financieros.
- Recomendaciones de inversión personalizadas.
- Compra o venta de activos financieros.
- Automatización de pagos.
- Aplicación móvil nativa.

# 11. Roadmap de desarrollo

## Fase 0 — Definición y preparación

- Validar requisitos.
- Diseñar arquitectura.
- Definir modelo de datos.
- Crear repositorio GitHub.
- Configurar estándares de desarrollo.
- Crear backlog inicial.
- Diseñar prototipos de interfaz.
- Crear documentos financieros sintéticos para pruebas.

**Entregable:** especificación funcional y técnica inicial.

## Fase 1 — Infraestructura y fundamentos

- Crear estructura Angular.
- Crear backend FastAPI.
- Configurar PostgreSQL local.
- Configurar Docker Compose.
- Configurar migraciones.
- Preparar integración con Entra External ID.
- Configurar entornos.
- Crear pipeline inicial de GitHub Actions.

**Entregable:** aplicación web desplegable con autenticación y base de datos.

## Fase 2 — Gestión financiera

- Crear bancos y cuentas.
- Crear tarjetas.
- Registrar movimientos manuales.
- Implementar categorías.
- Importar documentos.
- Anonimizar localmente.
- Validar y confirmar movimientos.
- Implementar deduplicación.
- Conciliar transferencias.

**Entregable:** sistema funcional de gestión financiera.

## Fase 3 — Presupuestos y objetivos

- Crear presupuestos.
- Crear múltiples objetivos.
- Asignar prioridades.
- Registrar aportaciones.
- Calcular capacidad de ahorro.
- Crear dashboard.
- Implementar alertas y proyecciones.

**Entregable:** primera versión de planificación financiera.

## Fase 4 — Inteligencia artificial

- Integrar Microsoft Foundry.
- Implementar clasificación inteligente.
- Crear herramientas financieras.
- Desarrollar asistente conversacional.
- Implementar simulador de compras.
- Evaluar precisión y confiabilidad.
- Incorporar protección frente a instrucciones maliciosas en documentos y consultas.

**Entregable:** asistente financiero inteligente.

## Fase 5 — Despliegue y robustecimiento

- Desplegar frontend y backend en Azure.
- Configurar PostgreSQL administrado si el presupuesto lo permite.
- Configurar Key Vault.
- Implementar observabilidad.
- Crear infraestructura mediante Bicep.
- Implementar copias de seguridad.
- Ejecutar pruebas de seguridad y aislamiento.
- Medir costos.

**Entregable:** versión de pruebas en la nube con controles de seguridad.

## Fase 6 — Evolución del producto

- Integración Gmail.
- Nuevos bancos.
- Importación CSV y Excel.
- Automatizaciones.
- Informes avanzados.
- Memoria contextual del asistente.
- RAG cuando se justifique.
- Multiusuario comercial.
- Grafos y nuevas integraciones si aportan valor.

**Entregable:** producto ampliado y preparado para validar su comercialización.

# 12. Criterios de aceptación del MVP

El MVP se considerará funcional cuando cumpla, como mínimo, los siguientes criterios:

1. Un usuario puede registrarse e iniciar sesión.
2. Dos usuarios distintos no pueden consultar ni modificar los datos del otro.
3. Un usuario puede registrar varios bancos, cuentas y tarjetas.
4. Puede importar un estado de cuenta sintético de cada formato inicial.
5. Los documentos se procesan localmente antes de transmitir información financiera.
6. El usuario puede revisar y corregir movimientos antes de guardarlos.
7. Puede registrar gastos manualmente.
8. El sistema detecta movimientos duplicados.
9. Las transferencias entre cuentas propias no incrementan los gastos reales.
10. Los pagos de tarjetas no duplican las compras contabilizadas.
11. Los intereses recibidos se identifican como ingresos.
12. El usuario puede crear varios objetivos con diferentes prioridades.
13. El sistema calcula el ahorro necesario para cada objetivo.
14. Puede detectar desviaciones de presupuesto.
15. Puede proyectar el cumplimiento de objetivos.
16. Puede simular una compra y mostrar sus consecuencias financieras.
17. Los cálculos pueden verificarse mediante pruebas automatizadas.
18. La aplicación puede desplegarse en un entorno de pruebas accesible mediante URL.

# 13. Restricciones y riesgos

## Formatos bancarios

Los formatos de los PDF pueden cambiar y no se ha validado todavía su estructura exacta.

Mitigación: utilizar documentos sintéticos y diseñar parsers específicos y versionados.

## Extracción de datos

Los PDF escaneados o con tablas complejas pueden dificultar la extracción.

Mitigación: OCR local, validaciones y revisión humana.

## Duplicación de movimientos

Una transacción puede aparecer en diferentes fuentes.

Mitigación: huellas de movimientos, reglas de conciliación y confirmación.

## Privacidad

La información financiera es altamente sensible.

Mitigación: procesamiento local, minimización de datos, aislamiento, cifrado y auditoría.

## Proyecciones financieras

Las estimaciones pueden ser incorrectas si los datos están incompletos o los ingresos futuros cambian.

Mitigación: mostrar supuestos, rangos e incertidumbre.

## Costos de infraestructura

Los servicios administrados y modelos de IA pueden superar el presupuesto inicial.

Mitigación: comenzar localmente, evaluar consumo y desplegar solo lo necesario.

## Recomendaciones de IA

Un modelo podría interpretar incorrectamente una situación financiera.

Mitigación: cálculos deterministas, herramientas controladas, trazabilidad y explicaciones basadas en resultados verificables.

# 14. Principios de diseño del producto

1. La información financiera debe ser propiedad del usuario.
2. La privacidad debe estar integrada en la arquitectura.
3. Los cálculos monetarios deben ser deterministas.
4. La IA debe explicar y asistir, no inventar cifras.
5. Las decisiones financieras siempre pertenecen al usuario.
6. Las recomendaciones deben mostrar sus fundamentos.
7. Los datos incompletos deben identificarse explícitamente.
8. La aplicación debe funcionar sin depender de modelos de IA para sus operaciones financieras básicas.
9. La arquitectura debe evitar complejidad innecesaria.
10. Las funcionalidades nuevas deben responder a necesidades reales.

# 15. Indicadores de éxito

Para evaluar el producto se proponen los siguientes indicadores:

- Porcentaje de movimientos extraídos correctamente.
- Porcentaje de duplicados detectados.
- Precisión de la clasificación automática.
- Porcentaje de transferencias internas conciliadas correctamente.
- Diferencia entre saldos calculados y saldos de referencia.
- Exactitud de las proyecciones en escenarios controlados.
- Tiempo necesario para importar un estado de cuenta.
- Capacidad de completar tareas financieras frecuentes.
- Número de objetivos cuyo progreso puede calcularse correctamente.
- Costo mensual de operación.

Los valores objetivo se definirán después de construir un conjunto de pruebas sintético y medir el comportamiento inicial.

# 16. Consideraciones comerciales y regulatorias

El producto se diseñará inicialmente como herramienta de organización, análisis y educación financiera personal.

No ejecutará transacciones bancarias ni ofrecerá servicios de intermediación financiera.

Las recomendaciones no se presentarán como asesoría financiera o de inversión regulada.

Antes de comercializarlo en Ecuador u otros mercados, será necesario evaluar las obligaciones legales aplicables a protección de datos personales, tratamiento de información financiera, contratos, seguridad, privacidad y prestación del servicio.

---

# 17. Decisiones tecnológicas iniciales

| Área                 | Decisión                                      |
| -------------------- | --------------------------------------------- |
| Frontend             | Angular                                       |
| Backend              | Python + FastAPI                              |
| Base de datos        | PostgreSQL                                    |
| Autenticación        | Microsoft Entra External ID                   |
| IA                   | Microsoft Foundry                             |
| Orquestación         | Microsoft Agent Framework, cuando corresponda |
| Contenedores         | Docker                                        |
| Control de versiones | GitHub                                        |
| CI/CD                | GitHub Actions                                |
| Infraestructura      | Azure                                         |
| IaC                  | Bicep                                         |
| Observabilidad       | Application Insights                          |
| Secretos             | Azure Key Vault                               |

Estas tecnologías constituyen la arquitectura objetivo propuesta. La contratación y configuración de servicios Azure quedarán sujetas a pruebas de viabilidad, disponibilidad regional y costos.

# 18. Próximos entregables

Una vez aprobado este PRD, el proyecto avanzará mediante los siguientes documentos y artefactos:

1. **Documento de arquitectura:** componentes, responsabilidades, comunicación, seguridad y entornos.
2. **Modelo entidad-relación:** tablas, relaciones, restricciones e índices.
3. **Diseño de API:** endpoints, contratos, autenticación y autorización.
4. **Prototipo de interfaz:** pantallas y navegación principal.
5. **Backlog de desarrollo:** épicas, historias de usuario, tareas y criterios de aceptación.
6. **Plan de pruebas:** datos sintéticos, escenarios financieros, seguridad y evaluación de IA.
7. **Estimación de infraestructura:** costos de desarrollo, pruebas y producción.

---

**Visión final del producto**

Personal Finance AI no pretende ser solamente una aplicación que indique cuánto dinero ha gastado una persona.

Busca convertirse en un asistente que conozca su contexto financiero, entienda sus objetivos, detecte riesgos y le permita evaluar las consecuencias de sus decisiones antes de realizarlas.

El éxito del producto estará en ayudar al usuario a tomar mejores decisiones financieras, con información confiable, explicaciones claras y control absoluto sobre sus datos.
