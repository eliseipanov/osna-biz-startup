# Sprint 09: Farms Infrastructure & Product Metadata

**Goal:** Implement producer management (Farms) and upgrade product tracking (SKU, Units, Statuses).

## 1. Database Model Updates (`core/models.py`)

### A. New Model: `Farm`
Create a `Farm` model to track producers:
- `id`: Integer, Primary Key.
- `name`: String(100), Unique, Mandatory.
- `description_uk / description_de`: Text, Optional.
- `location`: String(255), Optional (for logistics).
- `contact_info`: String(255), Optional.
- `is_active`: Boolean, default=True.

### B. Upgrade `Product` Model
Add the following fields:
- `farm_id`: ForeignKey to `Farm.id`, Nullable (for now).
- `sku`: String(50), Unique, Nullable (Internal article number).
- `unit`: String(20), default='kg' (options: kg, pcs, bundle).
- `availability_status`: Enum field (`IN_STOCK`, `OUT_OF_STOCK`, `ON_REQUEST`). 
  *Note: Replace or deprecate the old `is_available` boolean.*

## 2. Admin UI Updates (`admin/app.py`)
- **Register FarmView:** Create a standard CRUD view for the `Farm` model.
- **Update ProductView:** - Add a dropdown to select a **Farm**.
    - Add fields for **SKU**, **Unit**, and **Availability Status**.
    - Ensure `Product.__str__` returns `f"{self.name_uk} ({self.farm.name if self.farm else 'No Farm'})"`.

## 3. Migration & Seeding
- Generate an Alembic migration for all schema changes.
- Ensure the `seed_db.py` script (if applicable) is updated or handle existing data safely.

## 4. Localization
- Add translation keys for new UI elements: "Producer/Farm", "Unit", "Availability", "On Request".