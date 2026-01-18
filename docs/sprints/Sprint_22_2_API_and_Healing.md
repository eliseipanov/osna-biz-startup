# Sprint 22.2: Many-to-Many Fix and WebApp API Foundation

**Objective:** Fix crashes in Bot/Excel due to schema changes and implement JSON API for the future WebApp.

## Task 1: Fix Bot Store Logic (bot/handlers/store.py)
1. **Update Product Query:** In `show_category_products`, replace the check `.where(Product.category_id == category_id)` with a Many-to-Many compatible join.
   - Use: `.join(Product.categories).where(Category.id == category_id)`
2. **Localization:** Ensure category names and product details still use the `.value` of language preference.

## Task 2: Fix Excel Manager (core/utils/excel_manager.py)
1. **Update Export:** Since `p.category` is gone, use `", ".join([c.name for c in p.categories])` to list all categories of a product in the Excel sheet.
2. **Update Import:** Ensure that when importing, the system can handle multiple category names (if needed) or at least doesn't crash.

## Task 3: Create WebApp API (admin/routes.py)
1. **Fix Blueprint:** Remove the non-existent `admin_api.init_db(db)` call in `admin/app.py`. Instead, import `db` directly inside `admin/routes.py`.
2. **Implement API Endpoints (JSON):**
   - `GET /api/catalog/farms` -> returns list of active farms.
   - `GET /api/catalog/categories` -> returns categories.
   - `GET /api/catalog/products?category_id=X` -> returns products in JSON format for the WebApp.

## Task 4: Fix Admin Initialization (admin/app.py)
1. Remove the line `admin_api.init_db(db)`.
2. Ensure `admin_api` blueprint is registered correctly.

## Definition of Done:
- Bot's catalog works again (shows products from the Many-to-Many relationship).
- Excel export includes all categories for each product.
- API endpoints return valid JSON data (testable via browser/postman).