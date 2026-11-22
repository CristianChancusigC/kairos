# Modelo de Datos Inicial — Kairos (PostgreSQL)

## Reglas clave
### Bloque 1: Identidad y Productos Financieros
- `users`: Representa al usuario dentro de Kairos.
    - `id` (UUID, PK)
    - `external_auth_id` (VARCHAR, UNIQUE) — El identificador estable que viene del token JWT de Microsoft Entra External ID (no dependemos del email por si el usuario lo cambia).
    - `email` (VARCHAR, UNIQUE)
    - `full_name` (VARCHAR)
    - `base_currency` (CHAR(3), default 'USD')
    - `created_at` (TIMESTAMPTZ)

- `banks`: Entidades financieras (ej. Banco Pichincha).
    - `id` (UUID, PK)
    - `user_id` (UUID, FK → users.id)
    - `name` (VARCHAR) — Ej. "Banco Pichincha"
    - `country_code` (CHAR(2), default 'EC')

- `financial_accounts`: Cuentas bancarias (ahorro, corriente, ahorro programado).
    - `id` (UUID, PK)
    - `user_id` (UUID, FK → users.id)
    - `bank_id` (UUID, FK → banks.id)
    - `name` (VARCHAR) — Ej. "Cuenta Principal", "Fondo Emergencia"
    - `account_type` (VARCHAR) — 'savings', 'checking', 'scheduled_savings'
    - `masked_number` (VARCHAR) — Solo últimos 4 dígitos (ej. "****4821"), por privacidad.
    - `purpose` (VARCHAR, nullable) — Propósito de la cuenta.
    - `current_balance` (NUMERIC(14, 2), default 0.00)
    - `is_active` (BOOLEAN, default true)

- `payment_cards`: Tarjetas de crédito o débito asociadas.
    - `id` (UUID, PK)
    - `user_id` (UUID, FK → users.id)
    - `bank_id` (UUID, FK → banks.id)
    - `linked_account_id` (UUID, FK → financial_accounts.id, nullable) — Si es débito, apunta a su cuenta.
    - `name` (VARCHAR) — Ej. "Visa Titanium Pichincha"
    - `card_type` (VARCHAR) — 'credit', 'debit'
    - `masked_number` (VARCHAR) — Ej. "****9012"
    - `credit_limit` (NUMERIC(14, 2), nullable)
    - `cutoff_day` (SMALLINT, nullable) — Día de corte (1–31)
    - `payment_due_day` (SMALLINT, nullable) — Día máximo de pago

### Bloque 2: Importaciones, Movimientos y Conciliación
- `statement_imports`: Trazabilidad de cada PDF procesado localmente.
    - `id` (UUID, PK)
    - `user_id` (UUID, FK → users.id)
    - `account_id` (UUID, FK → financial_accounts.id, nullable)
    - `card_id` (UUID, FK → payment_cards.id, nullable)
    - `file_hash` (VARCHAR(64)) — Hash SHA-256 calculado en Angular para evitar importar exactamente el mismo PDF dos veces.
    - `statement_period` (VARCHAR) — Ej. "2026-10"
    - `records_imported` (INT)
    - `status` (VARCHAR) — 'completed', 'partial', 'failed'
    - `imported_at` (TIMESTAMPTZ)

- `categories`: Categorías y subcategorías (soporta jerarquía apuntándose a sí misma).
    - `id` (UUID, PK)
    - `user_id` (UUID, FK → users.id, nullable) — NULL si es categoría base del sistema, o con user_id si es personalizada.
    - `parent_id` (UUID, FK → categories.id, nullable) — Permite subcategorías (ej. Alimentación → Supermercado).
    - `name` (VARCHAR)
    - `icon` (VARCHAR, nullable)

- `transfer_groups`: El pegamento que evita contar dos veces una transferencia interna o el pago de una tarjeta.
    - `id` (UUID, PK)
    - `user_id` (UUID, FK → users.id)
    - `group_type` (VARCHAR) — 'internal_transfer' (entre cuentas propias) o 'card_payment' (pago de tarjeta desde cuenta).
    - `notes` (VARCHAR, nullable)
    - `created_at` (TIMESTAMPTZ)

- `transactions`: La tabla central donde viven todos los movimientos.
    - `id` (UUID, PK)
    - `user_id` (UUID, FK → users.id)
    - `account_id` (UUID, FK → financial_accounts.id, nullable)
    - `card_id` (UUID, FK → payment_cards.id, nullable)
    - `category_id` (UUID, FK → categories.id, nullable)
    - `import_id` (UUID, FK → statement_imports.id, nullable) — NULL si fue registro manual.
    - `transfer_group_id` (UUID, FK → transfer_groups.id, nullable) — Si tiene valor, no suma como gasto real en los reportes.
    - `transaction_date` (DATE)
    - `description` (VARCHAR) — Descripción ya anonimizada.
    - `amount` (NUMERIC(14, 2)) — Siempre positivo; el signo financiero lo define transaction_type.
    - `currency` (CHAR(3), default 'USD')
    - `transaction_type` (VARCHAR) — 'income', 'expense', 'card_purchase', 'internal_transfer', 'card_payment', 'interest', 'fee', 'refund'
    - `source` (VARCHAR) — 'pdf_import', 'manual'
    - `fingerprint_hash` (VARCHAR(64)) — Huella única (fecha + monto + descripción + cuenta) para detectar movimientos duplicados.
    - `notes` (TEXT, nullable)
    - `created_at` (TIMESTAMPTZ)

### Bloque 3: Presupuestos y Objetivos Financieros
- budgets: Límites mensuales por categoría.
    - `id` (UUID, PK)
    - `user_id` (UUID, FK → users.id)
    - `category_id` (UUID, FK → categories.id)
    - `month_year` (CHAR(7)) — Formato '2026-11'
    - `limit_amount` (NUMERIC(14, 2))

Restricción única: (user_id, category_id, month_year) para no tener dos presupuestos distintos en la misma categoría y mes.

- `financial_goals`: Metas de ahorro con prioridades.
    - `id` (UUID, PK)
    - `user_id` (UUID, FK → users.id)
    - `linked_account_id` (UUID, FK → financial_accounts.id, nullable) — Opcional si la meta tiene cuenta dedicada.
    - `name` (VARCHAR) — Ej. "Fondo de Emergencia"
    - `description` (TEXT, nullable)
    - `target_amount` (NUMERIC(14, 2))
    - `current_amount` (NUMERIC(14, 2), default 0.00)
    - `deadline` (DATE)
    - `priority` (VARCHAR) — 'high', 'medium', 'low'
    - `status` (VARCHAR) — 'active', 'completed', 'paused'
    - `created_at` (TIMESTAMPTZ)

- goal_contributions: Historial de cada aporte a una meta.
    - `id` (UUID, PK)
    - `goal_id` (UUID, FK → financial_goals.id)
    - `transaction_id` (UUID, FK → transactions.id, nullable) — Puede vincularse a una transferencia real o ser una asignación virtual.
    - `amount` (NUMERIC(14, 2))
    - `contribution_date` (DATE)
    - `notes` (VARCHAR, nullable)

### Bloque 4: Auditoría
- `transaction_audit`: Registro histórico de correcciones o recategorizaciones.
    - `id` (UUID, PK)
    - `transaction_id` (UUID, FK → transactions.id)
    - `user_id` (UUID, FK → users.id)
    - `field_changed` (VARCHAR) — Ej. 'category_id', 'amount'
    - `old_value` (TEXT, nullable)
    - `new_value` (TEXT, nullable)
    - `changed_at` (TIMESTAMPTZ)


## Diagrama Visual de Relaciones
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