# Sprint 22: Architectural Refactor and Many-to-Many Categories

**Objective:** Clean up the admin application structure and evolve the product-category relationship to support multiple categories per product.

## Task 1: Update Database Models (core/models.py)
1. **Define Junction Table:** Create a table named `product_categories_association` (Base.metadata).
   - Columns: `product_id` (Integer, ForeignKey("products.id"), primary_key=True) and `category_id` (Integer, ForeignKey("categories.id"), primary_key=True).
2. **Update `Product` model:**
   - REMOVE the `category_id` Column and its ForeignKey.
   - ADD `categories = relationship("Category", secondary="product_categories_association", back_populates="products")`.
3. **Update `Category` model:**
   - Ensure it has `products = relationship("Product", secondary="product_categories_association", back_populates="categories")`.
4. **Update `OrderItem` model:** 
   - Ensure it still points to the correct product (no changes needed, but double-check).

## Task 2: Split admin/app.py into Modules
1. **Create `admin/admin_views.py`**:
   - Move all `ModelView` classes (`SecureModelView`, `UserView`, `ProductView`, `FarmView`, `CategoryView`, `TransactionView`) to this file.
   - Move `LoginForm` to this file.
   - Ensure all necessary imports (Flask-Admin, core.models, etc.) are included.
2. **Create `admin/routes.py`**:
   - Create a Flask Blueprint named `admin_api`.
   - Move all custom routes to this blueprint: `/login`, `/admin/logout`, `/admin/export_products`, `/admin/import_products`, and `/webhook/paypal/simulate`.
   - Ensure the simulation route uses `db.session` correctly within the blueprint context.
3. **Update `admin/app.py`**:
   - This file should now only handle: Flask app initialization, `db` init, `login_manager` setup, registering the `admin_api` blueprint, and registering the Admin views from `admin_views.py`.

## Task 3: Database Migration
1. Run `alembic revision --autogenerate -m "Refactor to many-to-many categories"`.
2. Run `alembic upgrade head`.

## Technical Constraints:
- Use EXACT naming: `product_categories_association` for the table.
- Relationship names: `categories` in Product, `products` in Category.
- Use existing instances: `db` from SQLAlchemy, `admin` from Flask-Admin.
- DO NOT change the logic of any handler, only relocate the code.

## Definition of Done:
- The server starts without errors.
- Admin panel correctly shows checkboxes or a multi-select field for categories in the Product edit page.
- A single product can be assigned to multiple categories.
- PayPal simulation endpoint still works at the same URL.