# Sprint 02: Database Migrations with Alembic

## 🎯 Goal
Set up Alembic to manage database schema migrations and create the initial tables in PostgreSQL.

## 🛠 Technical Specifications
1. **Initialize Alembic:**
   - Run `alembic init migrations` in the root directory.
2. **Configure Alembic:**
   - In `alembic.ini`, ensure it's configured to use variables from `.env` or set up `env.py`.
   - In `migrations/env.py`:
     - Import `Base` from `core.database`.
     - Set `target_metadata = Base.metadata`.
     - Ensure the connection uses the asynchronous driver (`asyncpg`).
3. **Generate Initial Migration:**
   - Create the first migration script: `alembic revision --autogenerate -m "Initial migration"`.
4. **Apply Migration:**
   - Run `alembic upgrade head` to create tables in the local `osna_farm_db`.

## ✅ Definition of Done
- `migrations/` directory exists in the repository.
- Tables `users`, `products`, and `orders` are successfully created in the PostgreSQL database.
- A confirmation script or command output showing the successful migration.