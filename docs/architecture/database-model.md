# Modelo de Datos Inicial — Kairos (PostgreSQL)

## Reglas clave

* **Identificadores:** Todas las claves primarias (`id`) usan `UUID` para evitar exponer secuencias predecibles.
* **Precisión monetaria:** Todos los montos usan `NUMERIC(14, 2)` (nunca `FLOAT`/`DOUBLE`) para evitar errores de redondeo.
* **Aislamiento multiusuario:** Todas las tablas con datos del usuario incluyen `user_id` (FK a `users.id`) para garantizar que cada consulta filtre estrictamente por el usuario autenticado.
* **Privacidad:** Nunca se almacenan números completos de cuentas, tarjetas, cédulas, direcciones ni teléfonos; solo los últimos 4 dígitos en `masked_number`.
* **Fechas con zona horaria:** Todas las marcas de tiempo usan `TIMESTAMPTZ` (almacenadas en UTC).

---

## Bloque 1: Identidad y Productos Financieros

### `users`

Representa el perfil del usuario dentro de Kairos.

| Campo | Tipo | Restricciones / Default | Descripción |
| :--- | :--- | :--- | :--- |
| `id` | `UUID` | PK | Identificador interno único del usuario en la base de datos. |
| `external_auth_id` | `VARCHAR` | UNIQUE, NOT NULL | Identificador estable proveniente del token JWT de Microsoft Entra External ID (no depende del correo). |
| `email` | `VARCHAR` | UNIQUE, NOT NULL | Correo electrónico del usuario para perfil y notificaciones. |
| `full_name` | `VARCHAR` | NOT NULL | Nombre completo para mostrar en la interfaz. |
| `base_currency` | `CHAR(3)` | Default `'USD'` | Moneda principal para reportes y totales. |
| `created_at` | `TIMESTAMPTZ` | Default `NOW()` | Fecha y hora de registro en Kairos. |

### `banks`

Entidades financieras (bancos o cooperativas) asociadas al usuario.

| Campo | Tipo | Restricciones / Default | Descripción |
| :--- | :--- | :--- | :--- |
| `id` | `UUID` | PK | Identificador del banco. |
| `user_id` | `UUID` | FK → `users.id`, NOT NULL | Dueño del registro. |
| `name` | `VARCHAR` | NOT NULL | Nombre de la entidad (ej. `"Banco Pichincha"`, `"Diners Club"`). |
| `country_code` | `CHAR(2)` | Default `'EC'` | Código de país del banco (ISO 3166-1 alpha-2). |

### `financial_accounts`

Cuentas bancarias del usuario (ahorro, corriente o ahorro programado).

| Campo | Tipo | Restricciones / Default | Descripción |
| :--- | :--- | :--- | :--- |
| `id` | `UUID` | PK | Identificador de la cuenta. |
| `user_id` | `UUID` | FK → `users.id`, NOT NULL | Dueño de la cuenta. |
| `bank_id` | `UUID` | FK → `banks.id`, NOT NULL | Banco al que pertenece la cuenta. |
| `name` | `VARCHAR` | NOT NULL | Alias legible (ej. `"Cuenta Principal"`, `"Fondo Emergencia"`). |
| `account_type` | `VARCHAR` | NOT NULL | Tipo de cuenta: `'savings'`, `'checking'`, `'scheduled_savings'`. |
| `masked_number` | `VARCHAR` | NOT NULL | Solo últimos 4 dígitos (ej. `"****8305"`) por privacidad. |
| `purpose` | `VARCHAR` | Nullable | Propósito opcional de la cuenta (ej. `"Gastos fijos"`). |
| `current_balance` | `NUMERIC(14, 2)` | Default `0.00` | Saldo actual de la cuenta. |
| `is_active` | `BOOLEAN` | Default `true` | Permite archivar una cuenta cerrada sin eliminar su historial. |

### `payment_cards`

Tarjetas de crédito o débito asociadas al usuario.

| Campo | Tipo | Restricciones / Default | Descripción |
| :--- | :--- | :--- | :--- |
| `id` | `UUID` | PK | Identificador de la tarjeta. |
| `user_id` | `UUID` | FK → `users.id`, NOT NULL | Dueño de la tarjeta. |
| `bank_id` | `UUID` | FK → `banks.id`, NOT NULL | Banco emisor. |
| `linked_account_id` | `UUID` | FK → `financial_accounts.id`, Nullable | Cuenta asociada si es tarjeta de débito (`NULL` si es crédito). |
| `name` | `VARCHAR` | NOT NULL | Alias de la tarjeta (ej. `"Titanium Visa"`). |
| `card_type` | `VARCHAR` | NOT NULL | Tipo de tarjeta: `'credit'` o `'debit'`. |
| `masked_number` | `VARCHAR` | NOT NULL | Últimos 4 dígitos (ej. `"****7348"`). |
| `credit_limit` | `NUMERIC(14, 2)` | Nullable | Cupo total o cupo global (aplica para crédito; útil para alertas y simulador). |
| `cutoff_day` | `SMALLINT` | Nullable | Día del mes en que corta la tarjeta (`1`–`31`). |
| `payment_due_day` | `SMALLINT` | Nullable | Día máximo de pago mensual (`1`–`31`). |

---

## Bloque 2: Importaciones, Movimientos y Conciliación

### `statement_imports`

Trazabilidad y resumen de cuadre de cada estado de cuenta PDF procesado localmente en el navegador.

| Campo | Tipo | Restricciones / Default | Descripción |
| :--- | :--- | :--- | :--- |
| `id` | `UUID` | PK | Identificador del lote de importación. |
| `user_id` | `UUID` | FK → `users.id`, NOT NULL | Usuario que realizó la importación. |
| `account_id` | `UUID` | FK → `financial_accounts.id`, Nullable | Cuenta origen si el PDF es un estado de cuenta bancaria. |
| `card_id` | `UUID` | FK → `payment_cards.id`, Nullable | Tarjeta origen si el PDF es un estado de cuenta de tarjeta. |
| `file_hash` | `VARCHAR(64)` | NOT NULL | Hash SHA-256 calculado en Angular para evitar importar exactamente el mismo PDF dos veces. |
| `statement_period` | `VARCHAR` | NOT NULL | Período del extracto (ej. `"2026-11"`). |
| `period_start` | `DATE` | Nullable | Fecha de inicio del ciclo o corte anterior del estado de cuenta. |
| `period_end` | `DATE` | Nullable | Fecha de corte actual del estado de cuenta. |
| `opening_balance` | `NUMERIC(14, 2)` | Nullable | Saldo anterior reportado en el PDF (para validación de cuadre). |
| `closing_balance` | `NUMERIC(14, 2)` | Nullable | Saldo actual o total a pagar reportado en el PDF. |
| `minimum_payment` | `NUMERIC(14, 2)` | Nullable | Pago mínimo reportado (específico para tarjetas de crédito). |
| `payment_due_date` | `DATE` | Nullable | Fecha máxima de pago (específico para tarjetas de crédito y alertas). |
| `records_imported` | `INT` | Default `0` | Cantidad de movimientos guardados desde ese archivo. |
| `status` | `VARCHAR` | NOT NULL | Estado del proceso: `'completed'`, `'partial'`, `'failed'`. |
| `imported_at` | `TIMESTAMPTZ` | Default `NOW()` | Fecha y hora en que se procesó el lote. |

### `categories`

Categorías y subcategorías de ingresos/gastos (soporta jerarquía autoreferenciada).

| Campo | Tipo | Restricciones / Default | Descripción |
| :--- | :--- | :--- | :--- |
| `id` | `UUID` | PK | Identificador de la categoría. |
| `user_id` | `UUID` | FK → `users.id`, Nullable | `NULL` si es categoría base del sistema; con `user_id` si es personalizada. |
| `parent_id` | `UUID` | FK → `categories.id`, Nullable | Permite subcategorías (ej. `Alimentación` → `Supermercado`). |
| `name` | `VARCHAR` | NOT NULL | Nombre visible de la categoría. |
| `icon` | `VARCHAR` | Nullable | Nombre de ícono o emoji para mostrar en el frontend. |

### `transfer_groups`

Agrupador que vincula movimientos espejo para evitar contar dos veces transferencias internas o pagos de tarjeta.

| Campo | Tipo | Restricciones / Default | Descripción |
| :--- | :--- | :--- | :--- |
| `id` | `UUID` | PK | Identificador del grupo de transferencia. |
| `user_id` | `UUID` | FK → `users.id`, NOT NULL | Dueño del movimiento agrupado. |
| `group_type` | `VARCHAR` | NOT NULL | `'internal_transfer'` (entre cuentas propias) o `'card_payment'` (pago de tarjeta desde cuenta). |
| `notes` | `VARCHAR` | Nullable | Nota opcional (ej. `"Pago tarjeta noviembre"`). |
| `created_at` | `TIMESTAMPTZ` | Default `NOW()` | Fecha de creación del vínculo. |

### `transactions`

Tabla central donde se registran todos los movimientos financieros.

| Campo | Tipo | Restricciones / Default | Descripción |
| :--- | :--- | :--- | :--- |
| `id` | `UUID` | PK | Identificador del movimiento. |
| `user_id` | `UUID` | FK → `users.id`, NOT NULL | Dueño del movimiento. |
| `account_id` | `UUID` | FK → `financial_accounts.id`, Nullable | Cuenta afectada (si aplica). |
| `card_id` | `UUID` | FK → `payment_cards.id`, Nullable | Tarjeta afectada (si aplica). |
| `category_id` | `UUID` | FK → `categories.id`, Nullable | Categoría asignada manualmente o por IA. |
| `import_id` | `UUID` | FK → `statement_imports.id`, Nullable | Lote PDF de origen (`NULL` si fue ingreso manual). |
| `transfer_group_id` | `UUID` | FK → `transfer_groups.id`, Nullable | Si tiene valor, excluye el movimiento del cálculo de gasto real. |
| `transaction_date` | `DATE` | NOT NULL | Fecha efectiva del movimiento. |
| `reference_number` | `VARCHAR(64)` | Nullable | Número de documento o comprobante del banco (`N.DOC.` o `Nº VALE`) para distinguir movimientos repetidos el mismo día. |
| `description` | `VARCHAR` | NOT NULL | Descripción limpia y anonimizada del comercio o concepto. |
| `amount` | `NUMERIC(14, 2)` | NOT NULL | Monto siempre positivo; la dirección del flujo la define `transaction_type`. |
| `currency` | `CHAR(3)` | Default `'USD'` | Moneda del movimiento. |
| `transaction_type` | `VARCHAR` | NOT NULL | `'income'`, `'expense'`, `'card_purchase'`, `'internal_transfer'`, `'card_payment'`, `'interest'`, `'fee'`, `'tax'`, `'refund'`. |
| `installment_current` | `SMALLINT` | Nullable | Número de cuota actual en consumos diferidos de tarjeta de crédito. |
| `installment_total` | `SMALLINT` | Nullable | Total de cuotas del consumo diferido (ej. `3` de `12`). |
| `source` | `VARCHAR` | NOT NULL | Origen del registro: `'pdf_import'` o `'manual'`. |
| `fingerprint_hash` | `VARCHAR(64)` | NOT NULL | Huella única (`fecha + monto + descripción + reference_number + cuenta/tarjeta`) para deduplicación. |
| `notes` | `TEXT` | Nullable | Comentario personal opcional. |
| `created_at` | `TIMESTAMPTZ` | Default `NOW()` | Fecha y hora de inserción en base de datos. |

---

## Bloque 3: Presupuestos y Objetivos Financieros

### `budgets`

Límites de gasto mensuales por categoría.

| Campo | Tipo | Restricciones / Default | Descripción |
| :--- | :--- | :--- | :--- |
| `id` | `UUID` | PK | Identificador del presupuesto. |
| `user_id` | `UUID` | FK → `users.id`, NOT NULL | Dueño del presupuesto. |
| `category_id` | `UUID` | FK → `categories.id`, NOT NULL | Categoría controlada (ej. `Restaurantes`). |
| `month_year` | `CHAR(7)` | NOT NULL | Mes al que aplica en formato `YYYY-MM` (ej. `'2026-11'`). |
| `limit_amount` | `NUMERIC(14, 2)` | NOT NULL | Tope máximo de gasto permitido para ese mes. |

* **Restricción única:** `(user_id, category_id, month_year)` para evitar presupuestos duplicados en la misma categoría y mes.

### `financial_goals`

Metas de ahorro con fechas límite y prioridades.

| Campo | Tipo | Restricciones / Default | Descripción |
| :--- | :--- | :--- | :--- |
| `id` | `UUID` | PK | Identificador de la meta. |
| `user_id` | `UUID` | FK → `users.id`, NOT NULL | Dueño de la meta. |
| `linked_account_id` | `UUID` | FK → `financial_accounts.id`, Nullable | Cuenta dedicada a la meta (opcional). |
| `name` | `VARCHAR` | NOT NULL | Nombre de la meta (ej. `"Fondo de Emergencia"`). |
| `description` | `TEXT` | Nullable | Detalle o motivación de la meta. |
| `target_amount` | `NUMERIC(14, 2)` | NOT NULL | Monto total objetivo. |
| `current_amount` | `NUMERIC(14, 2)` | Default `0.00` | Monto acumulado hasta la fecha. |
| `deadline` | `DATE` | NOT NULL | Fecha límite estimada. |
| `priority` | `VARCHAR` | NOT NULL | Prioridad para el simulador: `'high'`, `'medium'`, `'low'`. |
| `status` | `VARCHAR` | Default `'active'` | Estado actual: `'active'`, `'completed'`, `'paused'`. |
| `created_at` | `TIMESTAMPTZ` | Default `NOW()` | Fecha de creación. |

### `goal_contributions`

Historial de aportes realizados a una meta financiera.

| Campo | Tipo | Restricciones / Default | Descripción |
| :--- | :--- | :--- | :--- |
| `id` | `UUID` | PK | Identificador del aporte. |
| `goal_id` | `UUID` | FK → `financial_goals.id`, NOT NULL | Meta a la que se abona el monto. |
| `transaction_id` | `UUID` | FK → `transactions.id`, Nullable | Movimiento bancario asociado si proviene de una transferencia real (`NULL` si es asignación virtual). |
| `amount` | `NUMERIC(14, 2)` | NOT NULL | Monto aportado. |
| `contribution_date` | `DATE` | NOT NULL | Fecha del aporte. |
| `notes` | `VARCHAR` | Nullable | Comentario opcional (ej. `"Ahorro quincena"`). |

---

## Bloque 4: Auditoría

### `transaction_audit`

Registro histórico de correcciones o recategorizaciones manuales sobre los movimientos.

| Campo | Tipo | Restricciones / Default | Descripción |
| :--- | :--- | :--- | :--- |
| `id` | `UUID` | PK | Identificador del evento de auditoría. |
| `transaction_id` | `UUID` | FK → `transactions.id`, NOT NULL | Movimiento modificado. |
| `user_id` | `UUID` | FK → `users.id`, NOT NULL | Usuario que realizó el cambio. |
| `field_changed` | `VARCHAR` | NOT NULL | Campo editado (ej. `'category_id'`, `'amount'`). |
| `old_value` | `TEXT` | Nullable | Valor anterior antes del cambio. |
| `new_value` | `TEXT` | Nullable | Valor nuevo después del cambio. |
| `changed_at` | `TIMESTAMPTZ` | Default `NOW()` | Fecha y hora de la modificación. |

---

## Notas de extracción y normalización desde PDFs (Frontend Angular)

Estas reglas se aplican en el navegador antes de enviar los movimientos al backend:

1. **Anonimización de PII:** Eliminar nombres, cédula/RUC, direcciones, correos, teléfonos y números completos de cuenta/tarjeta (incluidos celulares embebidos en descripciones como `RETSINTJ 099XXXXXXX`).
2. **Inferencia de año en fechas:** Los movimientos de Banco Pichincha (`09-nov.`) y Titanium Visa (`06/11`) omiten el año; debe inferirse a partir de `period_start` / `period_end` cuidando el cruce diciembre–enero.
3. **Normalización numérica:** Convertir ambos formatos (`214.30` en Pichincha y `3.000,00` / `507,87` en Titanium) a decimales estándar con punto antes de enviar al backend.
4. **Exclusión de tablas duplicadas o informativas:** Ignorar páginas publicitarias, tarifarios, simuladores de pago mínimo y la sección *Consumo en el exterior* de Titanium (ya incluida en el detalle principal de consumos).

---

## Diagrama Visual de Relaciones

```text
users
 ├──< banks
 │     ├──< financial_accounts >──┐
 │     └──< payment_cards ────────┼── (linked_account_id)
 │                                │
 ├──< statement_imports ──────────┤
 ├──< categories (self-ref)       │
 ├──< transfer_groups             │
 ├──< transactions ───────────────┴──> (account / card / category / import / transfer_group)
 │     └──< transaction_audit
 ├──< budgets ───────────────────────> (category)
 └──< financial_goals ───────────────> (linked_account_id)
       └──< goal_contributions ──────> (transaction_id)
```