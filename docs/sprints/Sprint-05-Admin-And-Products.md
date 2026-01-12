# Sprint-05-Admin-And-Products.md

## ℹ️ Status Update for Agent Kilo
The bot is now fully functional with SQLAlchemy 2.0 (async) and Aiogram 3.x. Routers are registered directly in `bot/main.py`. The database `osna_farm_db` is active.

## 🎯 Goal
Implement a Flask Admin panel to manage products and populate the database with Homeyer meat assortment.

## 🛠 Technical Specifications

### 1. Directory Structure
Create a new directory `admin/` for the Flask application.

### 2. Flask Admin Setup
- **File:** `admin/app.py`
- **Task:** - Create a Flask application.
  - Use `Flask-Admin` to create a web interface.
  - Setup a **Synchronous** SQLAlchemy engine for Flask (since Flask-Admin is sync). Use `from sqlalchemy import create_engine`.
  - Add views for models: `User`, `Product`, `Order`.
  - Use the `DATABASE_URL` from the root `.env` (convert `postgresql+asyncpg` to `postgresql` for the sync engine).

### 3. Database Seeding Script
- **File:** `scripts/seed_db.py`
- **Task:** Create a standalone script to insert initial products into the `products` table.
- **Assortment (Homeyer):**
  - "Rumpsteak (Яловичина)", price: 32.0, unit: "кг"
  - "Entrecôte (Яловичина)", price: 35.0, unit: "кг"
  - "Bratwurst (Ковбаски)", price: 12.5, unit: "кг"
  - "Schnitzel (Свинина)", price: 14.0, unit: "кг"

### 4. Requirements Update
- Ensure `Flask`, `Flask-Admin`, and `psycopg2-binary` are added to the list of required dependencies if needed.

## ✅ Definition of Done
- Provide the full code for `admin/app.py`.
- Provide the full code for `scripts/seed_db.py`.
- Provide instructions on how to run the Flask server.