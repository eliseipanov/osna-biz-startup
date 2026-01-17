# Sprint 20: Financial Core & PayPal Simulation

**Context:** Transitioning to the "Saturday Offer" business model. We need a Wallet system and a way to simulate PayPal payments locally.

**Affected Files:** 
- `core/models.py` (Database schema)
- `admin/app.py` (Flask simulation endpoint)

## Task 1: Update Database Schema
1. **Modify `User` model** in `core/models.py`:
   - Add `balance = Column(Float, default=0.0)`.
2. **Add Enums** (using `enum.Enum` and `sqlalchemy.Enum`):
   - `TransactionType`: `DEPOSIT`, `PAYMENT`, `REFUND`.
   - `TransactionStatus`: `PENDING`, `COMPLETED`, `FAILED`.
3. **Create `Transaction` model**:
   - Fields: `id` (PK), `user_id` (FK to users), `amount` (Float), `type` (Enum TransactionType), `status` (Enum TransactionStatus), `external_id` (String, for PayPal ID), `created_at` (DateTime).
   - Establish relationship: `User.transactions <-> Transaction.user`.

## Task 2: Implement PayPal Simulation Endpoint
1. **In `admin/app.py`**, add a new POST route `/webhook/paypal/simulate`:
   - It must accept JSON: `{"user_id": int, "amount": float, "paypal_id": string}`.
   - Logic: 
     - Find user by ID.
     - Create a new `Transaction` with status `COMPLETED` and type `DEPOSIT`.
     - Update `User.balance` by adding the `amount`.
     - Commit changes to DB using `db.session`.
     - Return JSON success with `new_balance`.

## Task 3: Database Migration
1. Generate an Alembic migration script: `alembic revision --autogenerate -m "Add wallet and transactions"`.
2. Apply the migration: `alembic upgrade head`.

## Definition of Done
- Models are updated and migrations applied.
- The simulation endpoint returns 200 OK and correctly updates the user's balance in the PostgreSQL database.