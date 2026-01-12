# Osna-biz-startup Project Summary - 2026-01-12

## 📌 Project Overview
- **Name:** Osna-biz-startup (Osnabrück Farm Connect)
- **Concept:** A delivery service for local farm products (meat, seasonal vegetables) via Telegram Bot and a simplified Web interface.
- **Target Audience:** Local residents, including elderly users ("grandmothers") who need a simple, accessible interface.
- **Language Priority:** **Ukrainian (Primary)**, German (Secondary).

## 🛠 Technology Stack
- **Backend:** Python 3.11+, SQLAlchemy 2.0 (Async), PostgreSQL.
- **Bot:** Aiogram 3.x.
- **Admin Panel:** Flask-Admin + Flask-Login.
- **Database Tools:** Alembic for migrations, `asyncpg` for database connection.
- **Environment:** WSL/Linux (Ubuntu).

## ✅ Current Implementation Status (Completed)

### 1. Infrastructure & Core Logic
- **Database Architecture:** Fully implemented async engine and session management.
- **Models:** `User`, `Category`, `Product`, `Order`, `StaticPage`, `Translation`, `GlobalSettings`, `Farm`.
- **Migrations:** Alembic is configured; all schema changes (up to Sprint 09) are applied.

### 2. Admin & Authentication
- **Dual-mode Authentication:** Supports login via `telegram_id` (for easy access/legacy) or `email`/`username`.
- **Security:** Hidden password hashes in UI; secure password handling on save.
- **Multilingual UI:** Admin views support editing `_de` and `_uk` fields for products, categories, and pages.
- **Navigation:** Added Logout functionality and custom 404 error page.
- **Farm Management:** CRUD interface for Farm entities in admin panel.

### 3. Telegram Bot (MVP)
- **User Registration:** Automatic creation/update of user profiles on `/start`.
- **Catalog Navigation:** Basic display of categories and products synced with the database.
- **Main Keyboard:** Catalog, Cart, Orders, and Profile buttons (UI only for some).

### 4. Sprint 09: Farms & Advanced Availability (Completed)
- **Farm Model:** Implemented separate entity for Producers with name, location, contact info, descriptions in UK/DE.
- **Product Metadata:** Added `farm_id` (FK to Farm), `sku` (unique article number), `unit` (kg, pcs, bundle), `availability_status` (Enum: IN_STOCK, OUT_OF_STOCK, ON_REQUEST).
- **Availability States:** Replaced boolean `is_available` with enum for better stock management.
- **Admin UI:** Updated Product view with farm dropdown, new fields; added Farm CRUD view.
- **Localization:** Added translation keys for new UI elements.

---

## ⏳ Planned & Pending Tasks (Priority Queue)

### 1. "Speedy Gonzales" Excel Integration
- **Export/Import:** Bulk update of products, prices, and stock via `.xlsx` files.
- **Mapping:** Smart matching by ID/SKU and Farm name.

### 2. Bot Handlers Completion
- **Cart Logic:** Add/Remove items, calculate totals.
- **Orders History:** View past orders and current statuses.
- **User Profile:** Manage preferences and contact details.

### 3. Web Frontend (The "Grandmother" Portal)
- Simplified registration and checkout form outside of Telegram.

---

## 📂 Architecture & File Paths
- **Virtual Env:** `/var/www/osna-biz-startup/.venv/bin/python`
- **Models:** `core/models.py`
- **Admin Setup:** `admin/app.py`
- **Migrations:** `migrations/versions/`

## ⚠️ Critical Development Constraints
1. **Migrations:** Never modify `models.py` without generating an Alembic migration.
2. **Sync/Async:** Use sync sessions for Flask-Admin and async sessions for the Bot.
3. **Language:** Ukrainian is mandatory; German is supplementary.
4. **Code Quality:** Avoid code fragments; always request/provide full updated files.