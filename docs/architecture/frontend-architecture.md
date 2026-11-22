# Arquitectura Frontend — Kairos (Angular 21)

## Capas y organización
- `domain/`: Modelos de datos, tipos y reglas de validación/anonimización (sin depender de Angular ni HTTP).
- `application/`: Casos de uso y estado reactivo con Signals (`signal`, `computed`, `effect`) y recursos asíncronos.
- `infrastructure/`: Adaptadores HTTP hacia FastAPI, autenticación MSAL (Entra External ID) y procesamiento local de PDF.
- `presentation/`: Componentes standalone, rutas y vistas (dashboard, cuentas, movimientos, presupuestos, metas, simulador, asistente).

## Estado con Signals
- Usar `signal()` para el estado base (ej. transacciones cargadas, filtros activos, cuenta seleccionada).
- Usar `computed()` para totales derivados (ej. saldo consolidado, presupuesto restante, ahorro proyectado).
- Evitar duplicar estado calculado en variables sueltas.

## Flujo local de lectura y anonimización de PDF (Privacidad)
1. El usuario selecciona un PDF en el navegador (el archivo NO se sube crudo al servidor ni a servicios de IA).
2. Se extrae el texto/tablas localmente (ej. con `pdfjs-dist` en un Web Worker para no bloquear la UI).
3. Se eliminan o enmascaran datos sensibles antes de armar el payload (números de cuenta/tarjeta completos, cédula/RUC, titular, direcciones). Si no se puede garantizar la anonimización, se bloquea el envío y se pide revisión manual.
4. El usuario revisa y corrige la vista previa de movimientos.
5. Solo se envían al backend (`POST /api/v1/transactions/import`) los movimientos estructurados y anonimizados junto con el hash del documento.