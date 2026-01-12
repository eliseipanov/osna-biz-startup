# Sprint 09 (Full): Farms Infrastructure & Data Integrity Fix

**Goal:** Implement producer management (Farms), upgrade product tracking, and fix the seeding/localization issues.

## 1. Database Model Updates (`core/models.py`)
- **New Model `Farm`:** - Fields: `id`, `name` (unique), `description_uk/de`, `location`, `contact_info`, `is_active`.
- **Update `Product` Model:**
    - `farm_id`: ForeignKey to `Farm.id` (nullable).
    - `sku`: String(50), Unique, Nullable.
    - `unit`: String(20), default='kg'.
    - `availability_status`: Enum (`IN_STOCK`, `OUT_OF_STOCK`, `ON_REQUEST`).
- **String Representation:** Update `Product.__str__` to return `f"{self.name_uk} ({self.farm.name if self.farm else 'No Farm'})"`.

## 2. Smart "Upsert" Seeding (`scripts/seed_db.py`)
**CRITICAL:** Do NOT overwrite existing manual translations.
- Refactor the script to check for existence before adding:
    - **Categories:** Check by `slug`. If exists, DO NOT update `name_uk` or `description_uk`.
    - **Products:** Check by `name_uk` or `sku`. If exists, SKIP.
    - **Farms:** Check by `name`.
- NEVER use `db.drop_all()` or `truncate`.

## 3. Admin UI Localization (`admin/app.py`)
- Use Ukrainian labels for all columns in `ProductView`, `CategoryView`, and `FarmView`.
- **Mappings:**
    - `name_uk` -> "Назва (Укр)"
    - `name_de` -> "Назва (Нім)"
    - `availability_status` -> "Статус наявності"
    - `farm` -> "Ферма/Виробник"
    - `unit` -> "Одиниця виміру"
    - `sku` -> "Артикул (SKU)"
- Register `FarmView` in the Admin panel.

## 4. Environment & Tools
- Add `openpyxl` and `pandas` to `requirements.txt`.
- Create `core/utils/excel_manager.py` (placeholder) for future Excel tasks.