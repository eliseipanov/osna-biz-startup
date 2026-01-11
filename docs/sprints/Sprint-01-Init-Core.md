

```markdown
# Sprint 01: Project Initialization & Core Database Layer

## 🎯 Goal
Initialize the project structure, set up asynchronous database connectivity using SQLAlchemy 2.0, and define the primary data models.

## 📂 Targeted Structure
```text
osna-biz-startup/
├── core/
│   ├── database.py     # Connection logic
│   └── models.py       # Data Schema
├── .env                # Database URL configuration
└── requirements.txt    # Project dependencies

```

## 🛠 Technical Specifications

### 1. Database Connection (`core/database.py`)

* Use `sqlalchemy.ext.asyncio` for asynchronous operations.
* Implement `create_async_engine` using the `DATABASE_URL` from the `.env` file.
* Define an `async_sessionmaker` with `AsyncSession` class.
* Provide a `Base` class using `DeclarativeBase`.
* Create a helper function `get_session()` for session dependency injection.

### 2. Data Models (`core/models.py`)

Define the following SQLAlchemy models:

* **User**:
* `id` (PK), `tg_id` (BigInt, unique, index), `full_name`, `phone`, `address` (Text), `is_trusted` (Boolean, default=False), `created_at`.


* **Product**:
* `id` (PK), `name`, `price` (Float), `unit` (String, default='kg'), `is_available` (Boolean), `description`.


* **Order**:
* `id` (PK), `user_id` (FK to users), `status` (Enum/String: pending, confirmed, shipping, done), `total_price`, `delivery_slot`, `comment`, `created_at`.
* Define relationship back to `User`.



## ✅ Definition of Done

* Files `core/database.py` and `core/models.py` are created with valid Python code.
* No code fragments; provide complete files only.
* Code must be compatible with `asyncpg` driver.
