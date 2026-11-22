# Modelo de Datos Inicial — Kairos (PostgreSQL)

## Reglas clave
- **Dinero:** Siempre `NUMERIC(14, 2)` (nunca `FLOAT`).
- **Aislamiento:** Toda entidad de usuario lleva `user_id` y se filtra por el usuario autenticado.
- **IDs:** `UUID` para evitar identificadores secuenciales predecibles.
- **Fechas:** `DATE` para fechas de movimiento/meta; `TIMESTAMPTZ` para auditoría/creación.

## Tablas principales (MVP)
1. `users`: `id` (UUID, PK), `external_auth_id` (VARCHAR, UNIQUE), `email` (VARCHAR, UNIQUE), `full_name` (VARCHAR), `base_currency` (CHAR(3), default `'USD'`), `created_at` (TIMESTAMPTZ).
2. `banks`: `id` (UUID, PK), `user_id` (UUID, FK -> `users.id`), `name` (VARCHAR), `country_code` (CHAR(2), default `'EC'`).
3. `financial_accounts`: `id` (UUID, PK), `user_id` (UUID, FK -> `users.id`), `bank_id` (UUID, FK -> `banks.id`), `name` (VARCHAR), `account_type` (VARCHAR: `'savings'`, `'checking'`, `'scheduled_savings'`), `masked_number` (VARCHAR), `purpose` (VARCHAR, nullable), `current_balance` (NUMERIC(14, 2)), `is_active` (BOOLEAN).
4. `payment_cards`: `id` (UUID, PK), `user_id` (UUID, FK -> `users.id`), `bank_id` (UUID, FK -> `banks.id`), `linked_account_id` (UUID, FK -> `financial_accounts.id`, nullable), `name` (VARCHAR), `card_type` (VARCHAR: `'credit'`, `'debit'`), `masked_number` (VARCHAR), `credit_limit` (NUMERIC(14, 2), nullable), `cutoff_day` (SMALLINT, nullable), `payment_due_day` (SMALLINT, nullable).
5. `statement_imports`: `id` (UUID, PK), `user_id` (UUID, FK -> `users.id`), `account_id` (UUID, FK -> `financial_accounts.id`, nullable), `card_id` (UUID, FK -> `payment_cards.id`, nullable), `file_hash` (VARCHAR(64)), `statement_period` (VARCHAR), `records_imported` (INT), `status` (VARCHAR), `imported_at` (TIMESTAMPTZ).
6. `categories`: `id` (UUID, PK), `user_id` (UUID, FK -> `users.id`, nullable), `parent_id` (UUID, FK -> `categories.id`, nullable), `name` (VARCHAR), `icon` (VARCHAR, nullable).
7. `transfer_groups`: `id` (UUID, PK), `user_id` (UUID, FK -> `users.id`), `group_type` (VARCHAR: `'internal_transfer'`, `'card_payment'`), `notes` (VARCHAR, nullable), `created_at` (TIMESTAMPTZ).
8. `transactions`: `id` (UUID, PK), `user_id` (UUID, FK -> `users.id`), `account_id` (UUID, FK -> `financial_accounts.id`, nullable), `card_id` (UUID, FK -> `payment_cards.id`, nullable), `category_id` (UUID, FK -> `categories.id`, nullable), `import_id` (UUID, FK -> `statement_imports.id`, nullable), `transfer_group_id` (UUID, FK -> `transfer_groups.id`, nullable), `transaction_date` (DATE), `description` (VARCHAR), `amount` (NUMERIC(14, 2)), `currency` (CHAR(3), default `'USD'`), `transaction_type` (VARCHAR), `source` (VARCHAR: `'pdf_import'`, `'manual'`), `fingerprint_hash` (VARCHAR(64)), `notes` (TEXT, nullable), `created_at` (TIMESTAMPTZ).
9. `budgets`: `id` (UUID, PK), `user_id` (UUID, FK -> `users.id`), `category_id` (UUID, FK -> `categories.id`), `month_year` (CHAR(7)), `limit_amount` (NUMERIC(14, 2)). Único en `(user_id, category_id, month_year)`.
10. `financial_goals`: `id` (UUID, PK), `user_id` (UUID, FK -> `users.id`), `linked_account_id` (UUID, FK -> `financial_accounts.id`, nullable), `name` (VARCHAR), `description` (TEXT, nullable), `target_amount` (NUMERIC(14, 2)), `current_amount` (NUMERIC(14, 2)), `deadline` (DATE), `priority` (VARCHAR: `'high'`, `'medium'`, `'low'`), `status` (VARCHAR), `created_at` (TIMESTAMPTZ).
11. `goal_contributions`: `id` (UUID, PK), `goal_id` (UUID, FK -> `financial_goals.id`), `transaction_id` (UUID, FK -> `transactions.id`, nullable), `amount` (NUMERIC(14, 2)), `contribution_date` (DATE), `notes` (VARCHAR, nullable).
12. `transaction_audit`: `id` (UUID, PK), `transaction_id` (UUID, FK -> `transactions.id`), `user_id` (UUID, FK -> `users.id`), `field_changed` (VARCHAR), `old_value` (TEXT, nullable), `new_value` (TEXT, nullable), `changed_at` (TIMESTAMPTZ).