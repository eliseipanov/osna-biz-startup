# Sprint 22.7: Fix Export Logic and Full Category Context

**Objective:** Resolve the 500 error in export and ensure that filtered results include all associated categories for each product.

## Task 1: Shared Admin Instance (admin/extensions.py)
- Move the `admin = Admin(...)` definition from `app.py` to `extensions.py`.
- This ensures `routes.py` can access `admin._views` without circular imports.

## Task 2: Admin Initialization (admin/app.py)
- Import `admin` from `extensions.py`.
- Initialize it using `admin.init_app(app)`.
- Re-register all views: `admin.add_view(UserView(User, db.session))`, etc.

## Task 3: Robust Export Logic (admin/routes.py)
- Import `db` and `admin` from `extensions.py`.
- In the `export_products` route:
  1. Find the `ProductView` instance within `admin._views`.
  2. Get the filtered query using the view's internal logic based on `request.args`.
  3. **CRITICAL:** Modify the query to use `.options(joinedload(Product.categories))`. This ensures the Excel manager sees ALL categories for each product.
  4. Execute the query to get ALL records (ignore pagination/limits).
  5. Pass the resulting list to `export_products_to_excel_sync`.

## Task 4: Code Hygiene
- Ensure no trailing system tags like `</content>` are added to any file.

## Definition of Done:
- "Export to Excel" button works without 500 errors.
- Filtered Excel file shows ALL categories for a product (e.g., "Beef, Actions") even if filtered only by "Beef".
- Export contains all matching rows, not just the first page.